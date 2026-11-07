---
name: ad-teardown
description: Breaks a video ad down the way a creative director would. It measures length, cut speed and first cut; pulls frame strips of the first 3 seconds and of the whole ad; transcribes the speech; tags the hook, format, people, text, offer and ending; and scores it against benchmarks from winning food ads. Use when the user asks to analyze, break down, tear down, critique or compare a video ad, Reel or TikTok, especially for a restaurant or food brand.
---

# Ad teardown

## 1. Measure (free, local)

Run the bundled script on each video. It needs ffmpeg; whisper.cpp (`whisper-cli`) is optional, for transcripts.

```bash
bash scripts/teardown.sh path/to/ad.mp4 out_dir/
```

It writes:
- `hook.jpg`: frames every 0.5 s from 0 to 3 s.
- `sheet.jpg`: 16 frames across the whole ad.
- `metrics.json`: duration, cuts, cuts_per_min, avg_shot, first_cut.
- `transcript.txt`: only if whisper-cli is installed. Set `WHISPER_MODEL` to the model's path.

## 2. Look and tag

Read `hook.jpg` and `sheet.jpg`. Ignore the yellow timestamps; they are not part of the ad. Fill in this record, judging only what you can see or read:

```json
{
 "format": "food_montage | owner_or_staff_talking | creator_or_influencer | customer_reactions | offer_graphic | kitchen_process | mixed",
 "frame0": "what is literally in the first frame",
 "hook_type": "food_motion | food_still | face_talking | text_headline | offer | person_eating | process_cooking | other",
 "hook_text": "on-screen words in the first 3 s, or null",
 "motion_in_first_second": true,
 "hands_in_frame": "none | some | most",
 "people": "none | staff_or_chef | owner | customers | creator",
 "speech": "none | voiceover | on_camera_talking",
 "onscreen_text": "none | dish_labels | headline | offer | captions | mixed",
 "offer": "the deal in words, or null",
 "brand_shown_by_sec": 0.0,
 "ending": "logo_card | offer_card | food_shot | person_talking | abrupt | other",
 "cta_words": "exact call to action, or null",
 "visual_style": "phone_native_raw | polished_studio | mixed"
}
```

## 3. Compare with the benchmarks

Open [benchmarks.md](benchmarks.md) and report the ad against it. Pass or miss on each line, with the gap in numbers. For example: "first cut at 4.1 s against a 1.9 s benchmark", or "no hand in frame, while 79% of winners have one".

## 4. Report

Keep it short and plain:
1. **Verdict in one line.**
2. **What it does that winners do.** Up to 3 points.
3. **The 3 biggest gaps**, each tied to a timestamp and a concrete fix.
4. **One thing worth stealing** from it, as a pattern rather than footage.

When the user gives several ads, add a summary table and the patterns shared by 3 or more of them.
