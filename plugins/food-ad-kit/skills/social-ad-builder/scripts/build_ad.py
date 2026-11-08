#!/usr/bin/env python3
"""build_ad.py: turn a JSON shot list into a finished vertical social ad (9:16 master + 4:5 feed cut).

Every default here was earned in a scored iteration loop plus blind A/B reviews:
  hard cuts (fades flash black) - dish labels on a solid brand-color pill - brand line on frame 0 -
  4% zoom punch as each food shot lands - light sharpen + one warm grade so mixed sources match -
  NO audio from AI clips (they carry made-up music) - real room ambience + a soft sizzle under food -
  loudness -14 LUFS with a limiter (true peak stays under 0 dB) - text kept inside the 4:5 safe area.

Usage:  python3 build_ad.py shotlist.json
Needs:  ffmpeg + ffprobe on PATH (free). Nothing else.
"""
import json, os, shutil, subprocess, sys, tempfile

FF, FP = shutil.which("ffmpeg"), shutil.which("ffprobe")
if not FF or not FP:
    sys.exit("ffmpeg and ffprobe are required (free): https://ffmpeg.org/download.html")

def find_font(bold):
    cands = (["/System/Library/Fonts/Supplemental/Georgia Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
              "C:/Windows/Fonts/georgiab.ttf"] if bold else
             ["/System/Library/Fonts/Supplemental/Georgia.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
              "C:/Windows/Fonts/georgia.ttf"])
    return next((c for c in cands if os.path.exists(c)), None)

def ff(*a):
    subprocess.run([FF, "-nostdin", "-loglevel", "error", "-y", *a], check=True)

def dur(f):
    return float(subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout)

def esc(t):
    """Make text safe inside an ffmpeg drawtext value."""
    return t.replace("\\", "\\\\").replace("'", "\u2019").replace(":", "\\:")

def fit(text, want, max_w=980):
    """Largest font size <= want whose longest line fits max_w px (serif bold averages ~0.56 em per character)."""
    longest = max((len(l) for l in text.split("\n")), default=1)
    return max(28, min(int(want), int(max_w / (0.56 * max(longest, 1)))))

def ffpath(p):
    return p.replace("\\", "/").replace(":", "\\:")

def hexcol(c):
    return "0x" + c.lstrip("#")

def main(cfg_path):
    cfg = json.load(open(cfg_path, encoding="utf-8-sig"))
    base = os.path.dirname(os.path.abspath(cfg_path))
    P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    W, H = 1080, 1920
    bold = ffpath(cfg.get("font_bold") or find_font(True) or sys.exit("set font_bold in the shot list"))
    reg = ffpath(cfg.get("font_regular") or find_font(False) or bold)
    pill = hexcol(cfg.get("brand_color", "#A3192B"))
    ly = int(cfg.get("label_y", 390))           # 390 on 1920 sits inside the 4:5 crop and clear of the Reels top bar
    out = P(cfg.get("out", "ad")) ; os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="build_ad_")
    parts = []
    for i, s in enumerate(cfg["shots"]):
        f, st, d = P(s["file"]), float(s.get("start", 0)), float(s["dur"])
        if not os.path.exists(f):
            sys.exit(f"shot {i + 1}: file not found: {f}")
        avail = dur(f) - st
        if avail <= 0.1:
            sys.exit(f"shot {i + 1}: start {st}s is past the end of {os.path.basename(f)}")
        if d > avail:
            print(f"note: shot {i + 1} asks for {d}s but {os.path.basename(f)} has {avail:.2f}s after start; using {avail:.2f}s")
            d = round(avail - 0.05, 2)
        food = s.get("food", True)
        lab, keep = s.get("label", ""), s.get("keep_label", False)    # keep_label: label continues from the previous shot, no re-animation
        v = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1,"
        if food:   # 4% zoom punch as the shot lands
            v += (f"scale=w='2*trunc({W//2}*(1.04-0.04*min(1,t/0.35)))':h='2*trunc({H//2}*(1.04-0.04*min(1,t/0.35)))'"
                  f":eval=frame:flags=lanczos,crop={W}:{H},")
        v += "unsharp=5:5:0.7:5:5:0.0,eq=saturation=1.10:contrast=1.04:gamma_r=1.02:gamma_b=0.97,vignette=angle=PI/5"
        if lab:
            size = fit(lab, s.get("label_size", 78))
            y = str(ly) if keep else f"'{ly}+20*max(0,1-t/0.25)'"
            alpha = "" if keep else ":alpha='if(lt(t,0.2),t/0.2,1)'"
            v += (f",drawtext=expansion=none:fontfile='{bold}':text='{esc(lab)}':fontcolor=white:fontsize={size}:x=(w-tw)/2:y={y}"
                  f":line_spacing=14:box=1:boxcolor={pill}@0.88:boxborderw=24:shadowcolor=black@0.6:shadowx=2:shadowy=2{alpha}")
        if i == 0 and cfg.get("brand_line"):   # brand on frame 0, on a near-solid plate
            v += (f",drawtext=expansion=none:fontfile='{bold}':text='{esc(cfg['brand_line'])}':fontcolor=white:fontsize=58:x=(w-tw)/2"
                  f":y={ly + 115}:box=1:boxcolor=black@0.80:boxborderw=18")
        if s.get("subline"):
            sub_y = ly + 110 + (lab.count("\n") * int(fit(lab, s.get("label_size", 78)) * 1.2) if lab else 0)
            v += (f",drawtext=expansion=none:fontfile='{reg}':text='{esc(s['subline'])}':fontcolor=white:fontsize=52:x=(w-tw)/2:y={sub_y}"
                  f":shadowcolor=black@0.9:shadowx=3:shadowy=3:alpha='if(lt(t,0.3),0,min(1,(t-0.3)/0.2))'")
        v += "[v]"
        # audio: never the clip's own track (AI video models add their own music); a soft sizzle under food, silence otherwise
        a = (f"[2:a]highpass=f=2200,lowpass=f=9000,volume=0.08,afade=t=in:d=0.25,afade=t=out:st={max(d-0.3, 0)}:d=0.3[a]"
             if food and cfg.get("sizzle", True) else "[1:a]anull[a]")
        o = f"{tmp}/{i:02d}.mp4"
        ff("-ss", str(st), "-t", str(d), "-i", f, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
           "-f", "lavfi", "-t", str(d), "-i", "anoisesrc=c=pink:r=48000:a=0.8,aformat=channel_layouts=stereo",
           "-filter_complex", f"{v};{a}", "-map", "[v]", "-map", "[a]", "-t", str(d),
           "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", "-ac", "2", o)
        parts.append(o)
    # end card
    ec = cfg.get("endcard")
    if ec:
        d = float(ec.get("dur", 2.0)); o = f"{tmp}/99.mp4"
        ins = ["-f", "lavfi", "-i", f"color={hexcol(ec.get('bg', '#F3ECE0'))}:s={W}x{H}:r=30:d={d}"]
        chain = []
        if ec.get("logo"):
            ins += ["-i", P(ec["logo"])]
            pre = f"[1]scale=-2:{int(ec.get('logo_h', 620))}[l];[0][l]overlay=(W-w)/2:{int(ec.get('logo_y', 520))}"
        else:
            pre = "[0]null"
        y = int(ec.get("text_y", 1185))
        for ln in ec.get("lines", []):
            font = bold if ln.get("bold") else reg
            chain.append(f"drawtext=expansion=none:fontfile='{font}':text='{esc(ln['text'])}':fontcolor={hexcol(ln.get('color', '#3A2E24'))}"
                         f":fontsize={fit(ln['text'], ln.get('size', 56))}:x=(w-tw)/2:y={y}")
            y += int(fit(ln['text'], ln.get('size', 56)) * 1.45)
        chain.append(f"zoompan=z='1+0.035*on/{int(d*30)}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={W}x{H}:fps=30")   # slow push-in
        fc = pre + "," + ",".join(chain) + "[v]"
        audio_idx = ins.count("-i")
        ff(*ins, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-filter_complex", fc,
           "-map", "[v]", "-map", f"{audio_idx}:a", "-t", str(d), "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-ar", "48000", "-ac", "2", o)
        parts.append(o)
    # join with a hard cut (normalize aspect flags first so concat accepts every part)
    n = len(parts); ins = sum((["-i", p] for p in parts), [])
    chain = "".join(f"[{k}:v]setsar=1[v{k}];" for k in range(n)) + "".join(f"[v{k}][{k}:a]" for k in range(n)) + f"concat=n={n}:v=1:a=1[v][a]"
    ff(*ins, "-filter_complex", chain, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-ar", "48000", f"{tmp}/joined.mp4")
    T = dur(f"{tmp}/joined.mp4")
    # final mix: optional real room recording under everything, then loudness + limiter
    if cfg.get("ambience"):
        fc = (f"[1:a]atrim=0:{T},asetpts=N/SR/TB,afade=t=in:d=0.3,afade=t=out:st={max(T-1, 0)}:d=1[r];"
              f"[0:a]aresample=48000[s];[r][s]amix=inputs=2:normalize=0:duration=first,"
              f"loudnorm=I=-14:TP=-1.5,aformat=sample_rates=48000:sample_fmts=fltp:channel_layouts=stereo,alimiter=limit=0.74:level=false[a]")
        ins = ["-i", f"{tmp}/joined.mp4", "-stream_loop", "-1", "-i", P(cfg["ambience"])]
    else:
        fc = "[0:a]loudnorm=I=-14:TP=-1.5,aformat=sample_rates=48000:sample_fmts=fltp:channel_layouts=stereo,alimiter=limit=0.74:level=false[a]"
        ins = ["-i", f"{tmp}/joined.mp4"]
    m = f"{out}-9x16.mp4"
    ff(*ins, "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-t", str(T), "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
       "-movflags", "+faststart", m)
    ff("-i", m, "-vf", f"crop={W}:1350:0:250", "-c:v", "libx264", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "copy",
       "-movflags", "+faststart", f"{out}-4x5.mp4")
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"{m} ({T:.1f} s) and {out}-4x5.mp4")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
