---
name: winning-ad-finder
description: Finds video ads that are probably working for restaurants and food brands, using the free Meta Ad Library, and builds a short "swipe file" of likely winners to study. Use when the user asks to find winning ads, research competitors' Facebook or Instagram ads, see what ads restaurants are running, or build ad inspiration for a food business.
---

# Winning ad finder

The Meta Ad Library (https://www.facebook.com/ads/library) shows every ad running on Facebook and Instagram. It never shows results, so you can't see clicks or sales. Two signals stand in for "this ad is working":

1. **Reach.** Sort by impressions. The ads Meta shows most are the ones the advertiser keeps paying to show.
2. **Staying power.** Advertisers turn off ads that lose money, so an ad still running after 30+ days has probably earned its keep.

**Old age alone is a trap.** Many small businesses boost one post and forget it for years. In a study of 1,944 food ads, the oldest "winners" had been running 6 years with almost no reach. Always combine age with reach.

## Steps (the user does the clicking; you guide and record)

Have the user open the Ad Library in their own browser. Automated scraping is against Meta's terms, so don't write or run a scraper. Then:

1. Set **Country** to their market and **Ad category** to "All ads".
2. Search a keyword, not a brand: their cuisine ("sichuan", "ramen", "tacos"), "restaurant", "[city] restaurant", their signature dish, and 2-3 competitors by name.
3. Open **Filters**: Active status = Active ads; Media type = Videos.
4. Open **Sort** and choose **Impressions (high to low)**.
5. For each of the top ~25 results, note:
   - the "Started running on" date
   - whether it says "N ads use this creative and text" (N of 3 or more means the advertiser is scaling it)
   - the Library ID, so it can be found again.
6. Keep an ad as a **likely winner** when:
   - it is in the top 25 by impressions AND has run 30+ days, OR
   - it has 3+ copies AND has run 21+ days.
7. Collect 15-30 likely winners across 3-5 searches. Have the user save each video with the Library's own download option, or screen-record it on a phone.

## The swipe file

Make a table, one row per winner:

| Library ID | Advertiser | Started | Days | Copies | Search | Format (montage / talking / creator / reactions / offer) | First 3 seconds in one line |

Then hand the saved videos to the **ad-teardown** skill to measure them and compare them with the benchmarks.

## What to tell the user

- These are signals, not proof. A single ad in the list proves nothing; a pattern across 15+ ads is worth copying.
- Copy patterns (hook type, pacing, structure), never someone's footage, music or wording.
- The only real scoreboard is their own ads. Run 3-5 versions at a small daily budget for a week and keep what wins.
