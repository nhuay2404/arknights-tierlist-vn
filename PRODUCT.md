# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Two audiences, weighted equally:

- Vietnamese players on the Global (English) client who are deciding which operators to pull, raise or upgrade and need the tier and the reasoning quickly.
- Newer Vietnamese players who struggle with English and need the tier list and the operator kits (Trait, E2 stats, M3 Skill, Talent, Range) explained in Vietnamese.

## Product Purpose

An unofficial Vietnamese edition of "An Arknights Operator Tier List" (AK Tier List). It includes the tier list, "Mới" (new additions), "Lịch sử" (change history) and translated per-operator details. The operator detail dialog shows the kit only (Trait, stats, Skill, Talent, Range); the authors' per-operator notes are kept in `data.js` but deliberately not shown there. Success means a Vietnamese reader understands where an operator sits and why, just as an English reader of the source would.

## Positioning

It is a faithful translation of an established community tier list, not an independent opinion. Game terms match the Global client 1:1 (see `TRANSLATION_GUIDE.md`), and a glossary tooltip explains them in place.

## Operating Context

- Most readers are on phones (mobile-first), often looking things up between game sessions.
- Readers search by operator name (including community nicknames such as SA2 or Kal2) and filter by rarity and class.
- Data comes from the AK Tier List Google Sheet (`data.js`) and from ArknightsAssets gamedata through `_build/` scripts (`details.js`). Untranslated new text falls back to English until `i18n/` catches up.

## Capabilities and Constraints

- Tabs: Xếp hạng (tier list), Mới, Lịch sử, Giới thiệu. Includes search, rarity, class and view filters, an operator detail dialog with a range grid, and glossary tooltips.
- Explanations live in place: glossary terms in kit text are underlined and open a tooltip, and class/subclass filter chips explain themselves on mouse hover or a ~450ms touch hold (subclass text = the in-game Trait from `details.js`; class text is hand-written).
- Some operators appear twice, as an IS (Integrated Strategies) and a general-mode entry. The data keeps `(IS)` / `(General)` in names; the UI shows the general variant as **OG**, as a tag right beside the operator name.
- Light and dark themes are both required.
- Mobile-first layout is required.
- The current stack is a static site (`index.html` plus data JS files, no build step). The user did not mark this as a hard constraint.

## Brand Commitments

- Voice follows `TRANSLATION_GUIDE.md`: natural Vietnamese written as a gamer would write it, friendly and direct, keeping the authors' humor. Game terms, class and archetype names, tiers (EX, S+ … F) and operator names stay in English.
- Fidelity comes first. Do not add, soften or sharpen the authors' judgments, and do not reword their notes for design convenience.

## Evidence on Hand

- Tier data and author notes: `data.js`. Translated operator details: `details.js` and `i18n/`. Glossary: `glossary.js`.
- Credits listed in `README.md`: the AK Tier List authors, ArknightsAssets/ArknightsGamedata and yuanyan3060/ArknightsGameResource (images). Arknights © Hypergryph / Yostar. This is a fan project.
- There are no testimonials, usage statistics or endorsements. Do not invent any.

## Product Principles

1. Translation fidelity beats everything else, and the source authors' verdicts are never altered.
2. One term, one spelling, matching the Global client.
3. Serve both the quick lookup and the learner: the tier is visible at a glance, and the explanation is one tap away.
4. Built for phones first. Desktop is the extension.
