---
name: blind-ad-review
description: Improves a video ad through repeated blind A/B reviews. Two versions are shown as contact sheets to a fresh reviewer who doesn't know which is newer, and both are scored against benchmarks from winning food ads. The next version changes only what reviewers agree on, and the loop continues until the gains stop. Use when the user wants to improve, iterate, critique or A/B test an ad or Reel before spending money, or asks "which version is better".
---

# Blind ad review loop

Judging your own work saturates fast. In the loop this skill comes from, the maker's own checklist hit 29.5 out of 30 by the 15th version, while real gains kept coming. **Blind** reviews kept finding them.

## 1. Make the contact sheets

For each version, make one image with a frame every 0.5 s and its timestamp:

```bash
ffmpeg -i ad.mp4 -vf "fps=2,scale=180:320,drawtext=text='%{pts\:hms}':fontcolor=yellow:fontsize=16:x=4:y=4,tile=8x6" -frames:v 1 sheet.jpg
```

Name them neutrally (`A.jpg`, `B.jpg`) and randomize which is newer.

## 2. Run the review with a fresh reviewer

Use a new subagent or a new chat each time, so earlier context doesn't bias it. Brief it with:

> You are a performance-marketing creative director for restaurant ads on Facebook and Instagram Reels, which mostly run with the sound off. Here are two cuts as contact sheets, one frame every 0.5 s; the yellow timestamps are not part of the ad. (1) Which cut gets more budget, and why? Be willing to call it a tie. (2) Score each 1-10 on: thumb-stop in the first second, appetite appeal, clarity of who and where, pacing, ending. (3) The 3 highest-impact fixes for the better cut, each tied to a timestamp. Flag anything that looks AI-generated or off. (4) Against these benchmarks, list every line the better cut misses: [paste the table from benchmarks.md].

Step 4 is the upgrade over taste. "Distance from what winning ads do" can be measured. "Do I like it" can't.

## 3. Decide what to change (the rules that held up)

- **Act only where 2+ reviewers agree**, or where the fix is measurable (loudness, a missing brand, a late first cut). Reviewers contradict each other on taste; in our loop one asked for a hard cut to the end card and the next asked for a dissolve.
- **Change one thing per version**, and write down what changed and why.
- **A sideways move is not a win.** When a reviewer calls it close, keep both versions as a real A/B for the platform to decide (long against short, two hooks).
- **Re-test reviewer-driven changes with a new reviewer**, to make sure you're improving the ad and not just pleasing one critic.
- **Watch for regressions.** A new backdrop that makes the food look sparser loses: food first, variety second.

## 4. Know when to stop

Stop when two reviews in a row call it a near-tie and every remaining fix needs new footage (people, a new angle, a real shoot) or a decision from the owner (an offer, the hook wording). Then ship 3-5 variants that each differ in one thing, run them at a small daily budget for a week, and let real viewers pick. Feed the result back into this loop as the new baseline.

## Log template

| # | What changed | Why (who asked) | Reviewer verdict | Keep? |
|---|---|---|---|---|
