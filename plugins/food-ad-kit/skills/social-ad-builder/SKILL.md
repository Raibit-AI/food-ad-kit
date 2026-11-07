---
name: social-ad-builder
description: Assembles finished vertical social video ads from clips plus a simple JSON shot list. It outputs a 9:16 master for Reels, Stories and TikTok plus a 4:5 feed cut, with brand-color dish labels, the brand on frame 0, hard cuts, a matched color grade, clean designed sound, safe loudness and an end card. It uses free ffmpeg only. Use when the user wants to edit, cut, assemble or render a short ad, Reel or TikTok from food or product clips, or make several ad variations to A/B test.
---

# Social ad builder

`scripts/build_ad.py` turns a shot list into two finished files. It needs only ffmpeg and ffprobe (free). Every default was earned in a scored iteration loop and blind A/B reviews:

- **Hard cuts.** Fades flash black at every cut.
- **Dish labels on a solid pill** in the brand color. Thin text over busy food is unreadable.
- **The brand line on frame 0.** Most people watch muted.
- **A 4% zoom punch** as each food shot lands.
- **Light sharpening plus one warm grade**, so AI clips and phone footage look like one camera.
- **No audio taken from the clips**, because AI video models add their own music. Sound is real room ambience if you have it, plus a soft sizzle under food.
- **Loudness at -14 LUFS with a limiter**, so the true peak stays under 0 dB and nothing distorts on phone speakers.
- **Text inside the 4:5 safe area** (y about 390 on 1920), so one master crops cleanly to the feed.

## Shot list

```json
{
 "out": "out/my-ad",
 "brand_color": "#A3192B",
 "brand_line": "Your Restaurant · Your Town",
 "ambience": "room-recording.mov",
 "shots": [
  {"file": "clips/noodle-lift.mp4", "start": 3.0, "dur": 2.0, "label": "Dan Dan Noodles"},
  {"file": "clips/mapo.mp4", "start": 0.8, "dur": 1.5, "label": "Mapo Tofu"},
  {"file": "clips/mapo-scoop.mp4", "start": 3.3, "dur": 1.5},
  {"file": "clips/dining-room.mp4", "start": 0, "dur": 1.0, "label": "Your Restaurant", "subline": "Your Town", "food": false}
 ],
 "endcard": {"bg": "#F3ECE0", "logo": "logo.png", "dur": 2.0,
  "lines": [{"text": "Your Town", "size": 58, "color": "#8B1E1E"},
            {"text": "Order pickup or reserve a table", "size": 56},
            {"text": "yoursite.com", "size": 84, "color": "#8B1E1E", "bold": true}]}
}
```

Run `python3 scripts/build_ad.py shotlist.json`. It writes `out/my-ad-9x16.mp4` and `out/my-ad-4x5.mp4`.

Shot fields:
- `start` and `dur` are in seconds inside the clip.
- `"food": false` turns off the zoom punch and sizzle (for room shots).
- `"keep_label": true` carries a label across two shots without re-animating it.
- `"subline"` adds a smaller line under the label.
- `"label_size"` sets the label size (default 78 px). Put `\n` in a label for two lines. Labels and end-card lines **shrink automatically to fit** the frame width.
- Text can contain quotes, colons, commas and `%`. Emoji will not render in the label fonts, so leave them out.
- If a clip is shorter than the requested `dur`, the builder uses what exists and prints a note. Check those notes: a hook that ends early freezes on its last frame.

## Pacing rules from winning ads (see the ad-teardown benchmarks)

- **Length:** a wordless food montage wins at **12-20 s**. Talking or story ads run longer.
- **Shot length:** a cut about every **1.8 s**, with the **first cut by about 2 s**. Shot lengths on a 0.5 s grid let any 120 BPM music track land on the cuts.
- **Order:** open on motion with a hand in frame. Run the food unbroken. Keep any empty-room shot to about 1 s, near the end.
- **Ending:** the best food shot, or a simple card with plain action words.
- **Music:** add it in the platform's own licensed library at upload. Don't bake in a song you don't have rights to.

## Making A/B variants

Change **one thing per variant** (the hook shot, the hook line, the length, or the dish set) so the winner explains itself. Copy the shot list, edit one field, build again.
