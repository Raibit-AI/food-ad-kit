---
name: food-shot-director
description: Directs AI image-to-video food shots for restaurant ads (chopsticks lifting noodles, a spoon scooping, sauce poured, a piece lifted to the lens). It gives the prompt formula, which foods animate well and which morph, and a keep-or-reject checklist so the dish still looks like the real menu item. Works with any image-to-video model (Kling, Veo, Seedance, LTX, Runway). Use when the user wants to animate a food photo, make food B-roll or a hand-in-frame food shot, or turn menu photos into video ads.
---

# Food shot director

Winning restaurant ads put **motion in the first second (79%)** and **a hand in frame (79%)**. A still dish with a slow zoom is the weakest opener. The fix is a "hand-in-frame action shot", generated from a real photo of the dish.

## 1. Start from a real photo of the real dish

Use the restaurant's own photo, ideally placed on a still of their real table or room. This matters for three reasons:
- **The model reproduces what it's given**, so their plating and portion stay honest.
- **Use one clean frame per dish.** If the photo has a blurred fill or a padded border, the model drifts out of it by about second 3 and invents a new scene.
- **Clear stray objects first.** One image edit removing leftover plates from a backdrop saves rerolls.

## 2. The prompt formula

> **[Utensil]** enters from the top of the frame, **[one action]**, and slowly lifts **[the food]** toward the camera, **[one detail: steam, a drip, a glisten]**. Only the **[utensil]** moves; the **[bowl/plate]** stays in place.
> Then a style tail: *Close-up appetizing food commercial, cozy restaurant at night, shallow depth of field, realistic, steady camera. No people in the background. Sound: soft ambience, no music, no speech.*

Proven examples:
- Chopsticks lift glossy noodles out of the bowl, chili oil dripping.
- A white ceramic spoon dips in and lifts tofu cubes in red sauce, steam rising.
- A hand with a small spoon pours a stream of chili oil over the dumplings.
- Chopsticks pick up **one crispy golden-red fried chicken piece coated in chili flakes**. Name the texture and color exactly, or the model invents a pale blob.

## 3. What animates well and what morphs

| Works | Fails |
|---|---|
| Noodles, sauces, broth, pours, steam, drips | A single solid piece lifted alone (dumplings melt, chicken turns into batter) |
| One utensil, one action | Two actions in one prompt |
| Overhead or 45-degree angle | Wide room shots: strangers walk in |
| 5-second clips; use the best 1.5-2.5 s | Using the whole clip: the motion often reverses or a second spoon appears |

Expect about **1 keeper in 2 takes**. Generate 2 seeds per shot.

## 4. Keep-or-reject checklist (check frames at 0.5 s steps)

Reject the take if any of these happen:
- [ ] The food no longer looks like the real dish (wrong shape, color or portion).
- [ ] The lifted piece changes shape mid-air.
- [ ] A second utensil, hand or plate appears.
- [ ] A person walks through the background.
- [ ] The utensil is oversized, plastic-looking or melting.
- [ ] The motion reverses.

Then trim to the cleanest 1.5-2.5 seconds.

## 5. Two traps

- **Strip the clip's audio.** Most video models add their own music, and every cut then switches songs. Build the sound separately; the social-ad-builder skill does this.
- **Honesty.** The shot must show what the customer actually gets. Never add food, garnish or portion that isn't on the real plate, and never generate fake customers or crowds in a real restaurant's ad.
