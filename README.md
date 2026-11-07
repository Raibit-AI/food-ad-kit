# Food Ad Kit

Five free skills for Claude that take a restaurant from "we should run ads" to a finished, tested Reel.

They were built while making real ads for a real Sichuan restaurant. Along the way we studied 60 winning food ads from Meta's Ad Library to learn what actually holds a thumb. Every rule in here was earned by a scored test, not borrowed from a blog post.

| Skill | What it does |
|---|---|
| **winning-ad-finder** | Uses the free Meta Ad Library to find ads that are probably working (reach plus staying power), and builds a swipe file. |
| **ad-teardown** | Measures any video ad (length, cut speed, first cut), pulls frame strips, transcribes it, tags the hook and format, and scores it against the winners. |
| **food-shot-director** | Turns a menu photo into a "hand in frame" AI food shot (chopsticks lifting noodles, a sauce pour) with any image-to-video model, plus a checklist to reject the takes that lie about the food. |
| **social-ad-builder** | Builds a finished 9:16 Reel and a 4:5 feed cut from clips plus a short shot list: brand-color labels, clean sound, safe loudness. Uses ffmpeg only. |
| **blind-ad-review** | Improves the ad by blind A/B reviews against the winner benchmarks, and knows when to stop and let real viewers decide. |

## What 60 winning food ads have in common

From restaurant ads that were top 25 by reach and still running after 30+ days:
- **79%** have something moving in the first second.
- **79%** have a hand in the shot.
- **71%** have nobody talking.
- **64%** look phone-made, not studio-made.
- Wordless food montages run a median **16 seconds**, with a cut about every **1.8 seconds**.

The full table is in `plugins/food-ad-kit/skills/ad-teardown/benchmarks.md`.

## Install

**Claude Code**

```
/plugin marketplace add Raibit-AI/food-ad-kit
/plugin install food-ad-kit@raibit
```

To get updates later, run `/plugin marketplace update`.

**Claude app or claude.ai:** download a skill zip from the [Releases page](https://github.com/Raibit-AI/food-ad-kit/releases), then upload it under Settings, Capabilities, Skills. Custom skills need a plan with code execution turned on.

**Requirements:** [ffmpeg](https://ffmpeg.org/download.html), which is free. [whisper.cpp](https://github.com/ggml-org/whisper.cpp) is optional, for transcripts. Any image-to-video model works for the food shots.

## Ground rules baked in

- **Study patterns, never copy.** Don't take anyone's footage, music or wording.
- **No scraping.** You browse the Ad Library yourself; the skills do the analysis.
- **Honest food.** AI shots must show the real dish and portion. No invented garnish, no fake crowds.

## Made by

[Raibit](https://raibit.ai). We build AI systems for real businesses. If you want this run for your restaurant, say hi at travis@raibit.ai.

MIT licensed. Use it, change it, share it.
