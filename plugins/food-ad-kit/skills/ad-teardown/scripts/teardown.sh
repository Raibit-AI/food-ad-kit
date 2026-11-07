#!/usr/bin/env bash
# teardown.sh <video> <out_dir> : hook strip (0-3 s), 16-frame sheet, metrics.json, optional transcript. Needs ffmpeg.
set -euo pipefail
v="$1"; o="${2:-teardown_$(basename "${v%.*}")}"; mkdir -p "$o"
command -v ffmpeg >/dev/null || { echo "ffmpeg is required (free): https://ffmpeg.org/download.html"; exit 1; }
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
cuts=$(ffmpeg -nostdin -i "$v" -vf "select='gt(scene,0.32)',showinfo" -an -f null - 2>&1 | grep -o "pts_time:[0-9.]*" | cut -d: -f2 | tr '\n' ' ' || true)
ts="drawtext=text='%{pts\:hms}':fontcolor=yellow:fontsize=14:x=3:y=3"
ffmpeg -nostdin -loglevel error -y -i "$v" -t 3.5 -vf "fps=2,scale=240:-2,$ts,tile=7x1" -frames:v 1 "$o/hook.jpg" \
  || ffmpeg -nostdin -loglevel error -y -i "$v" -t 3.5 -vf "fps=2,scale=240:-2,tile=7x1" -frames:v 1 "$o/hook.jpg"
step=$(awk -v d="$d" 'BEGIN{print d/16}')
ffmpeg -nostdin -loglevel error -y -i "$v" -vf "fps=1/$step,scale=200:-2,$ts,tile=8x2" -frames:v 1 "$o/sheet.jpg" \
  || ffmpeg -nostdin -loglevel error -y -i "$v" -vf "fps=1/$step,scale=200:-2,tile=8x2" -frames:v 1 "$o/sheet.jpg"
python3 - "$d" "$cuts" > "$o/metrics.json" <<'PY'
import json, sys
d = float(sys.argv[1]); c = [float(x) for x in sys.argv[2].split()]
print(json.dumps({"duration": round(d, 1), "cuts": len(c), "cuts_per_min": round(len(c) / d * 60, 1),
                  "avg_shot": round(d / (len(c) + 1), 2), "first_cut": c[0] if c else None}))
PY
has_audio=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$v" | head -1)
if [ -n "$has_audio" ] && command -v whisper-cli >/dev/null && [ -n "${WHISPER_MODEL:-}" ]; then
  ffmpeg -nostdin -loglevel error -y -i "$v" -ar 16000 -ac 1 -t 90 "$o/a.wav"
  whisper-cli -m "$WHISPER_MODEL" -f "$o/a.wav" -nt 2>/dev/null | tr -s ' \n' ' ' > "$o/transcript.txt"; rm -f "$o/a.wav"
fi
cat "$o/metrics.json"; echo; echo "wrote $o/hook.jpg $o/sheet.jpg"
