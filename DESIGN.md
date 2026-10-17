---
name: Arknights Tier List VN
description: Bảng xếp hạng operator Arknights bản tiếng Việt, giao diện kiểu terminal tác chiến.
colors:
  rhodes-blue: "#0098dc"
  field-ink: "#111111"
  ivory-ground: "#efefea"
  panel-white: "#ffffff"
  panel-recess: "#f6f6f2"
  hairline: "#d6d6cf"
  muted-text: "#5c5c57"
  stripe-gray: "#d6d6ce"
  link-blue: "#0b5cad"
  rarity-6: "#e8650a"
  rarity-5: "#a88700"
  rarity-4: "#9333ea"
  tooltip-slate: "#2b2f36"
  night-ground: "#0f1013"
  night-panel: "#17181c"
  night-recess: "#1f2126"
  night-line: "#2e3138"
  night-ink: "#ecebe4"
  night-muted: "#a6a59d"
  night-link: "#7cc4ff"
  night-rarity-6: "#ff8a3d"
  night-rarity-5: "#f0c419"
  night-rarity-4: "#c084fc"
typography:
  display:
    fontFamily: "Be Vietnam Pro, system-ui, sans-serif"
    fontSize: "clamp(40px, 7vw, 96px)"
    fontWeight: 900
    lineHeight: 0.95
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Chakra Petch, ui-monospace, monospace"
    fontSize: "26px"
    fontWeight: 700
    lineHeight: 1.2
  title:
    fontFamily: "Chakra Petch, ui-monospace, monospace"
    fontSize: "20px"
    fontWeight: 700
    letterSpacing: "0.04em"
  body:
    fontFamily: "Be Vietnam Pro, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Chakra Petch, ui-monospace, monospace"
    fontSize: "12px"
    fontWeight: 600
    letterSpacing: "0.12em"
  tier-mark:
    fontFamily: "Chakra Petch, ui-monospace, monospace"
    fontSize: "34px"
    fontWeight: 700
rounded:
  none: "0px"
  avatar: "50%"
spacing:
  xs: "4px"
  sm: "6px"
  md: "10px"
  lg: "14px"
  xl: "24px"
  gutter-mobile: "16px"
components:
  chip:
    backgroundColor: "{colors.panel-white}"
    textColor: "{colors.muted-text}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 14px"
    height: "44px"
  chip-active:
    backgroundColor: "{colors.field-ink}"
    textColor: "{colors.rhodes-blue}"
  nav-tab-active:
    backgroundColor: "{colors.rhodes-blue}"
    textColor: "{colors.field-ink}"
    typography: "{typography.label}"
  input-search:
    backgroundColor: "{colors.panel-white}"
    textColor: "{colors.field-ink}"
    rounded: "{rounded.none}"
    padding: "11px 14px 11px 40px"
  operator-card:
    backgroundColor: "rarity gradient (--b6 … --b1) over {colors.panel-recess}"
    textColor: "{colors.field-ink}"
    rounded: "{rounded.none}"
    padding: "5px 12px 5px 5px"
  stamp:
    textColor: "{colors.muted-text}"
    typography: "{typography.label}"
  fab:
    backgroundColor: "{colors.field-ink}"
    textColor: "{colors.rhodes-blue}"
    height: "48px"
    padding: "0 18px"
  card:
    backgroundColor: "{colors.panel-white}"
    rounded: "{rounded.none}"
    padding: "24px"
---

# Design System: Arknights Tier List VN

## Overview

**Creative North Star: "Field Terminal"**

The site reads like a Rhodes Island tactical terminal in the visual language of Arknights: Endfield. Ivory paper sits on a faint 48px blueprint grid. Ink-black frames hold Arknights-blue signals. Labels look like HUD readouts in a squared techno face, wrapped in `[ ]` brackets. Diagonal hatching marks anything that is a classification, such as tier labels, the modal header and the art frame. A giant striped ghost word anchors the hero and names the current tab (TIER, NEW, FAC, LOG, INFO). Each operator is an entry in a field manual, so information is dense, framed and scannable.

The system is hard-edged and flat. It has no radii except the circular avatar. Depth comes from offset solid "print" shadows in Arknights blue or ink, never from blur. Dark mode flips the paper to near-black graphite and keeps the Arknights blue as the one constant signal.

Motion is part of the identity, but it only happens on entry or in answer to the reader: a staggered rise on tier rows at first paint (filtering re-renders instantly), wipe reveals on the hero and tier labels, the stripe sweep over the art frame when a dossier opens, and a hover on operator cards. Nothing loops forever: no drifting background, scan bars, typewriter or decoding text, or spinning rings. That chrome made a lookup tool read as a cyberpunk template. All motion switches off under `prefers-reduced-motion`.

**Key Characteristics:**
- Arknights blue (#0098dc) on ink (#111) is the one signal pair. Everything else is neutral or a data color.
- Square corners everywhere. Only avatars are round.
- Offset hard shadows (3–10px, no blur) instead of soft elevation.
- Chakra Petch in uppercase with wide tracking for every label, tab, stat and heading. Be Vietnam Pro for reading text.
- A vertical left rail for navigation on desktop, which becomes a top bar on mobile.
- Hatching (−45° stripes) and `[ ]` brackets as the recurring HUD ornaments.

## Colors

An industrial two-tone of Arknights blue and ink on warm ivory paper, with data colors reserved for rarity and tier.

### Primary
- **Rhodes Blue** (rhodes-blue): the one accent. It marks the active nav tab, selection highlight, link underlines, search focus shadow, offset shadows on hover and dialogs, keyword highlights in skill text, range-grid cells, the footer band and the "MỚI" tag. On ink it becomes the text color, as in chips, tags and table headers.
- **Field Ink** (field-ink): frames, borders that carry meaning, active chips, the rail's active bar, the trait block background and the sticky controls' 2px rule. In dark mode it becomes Night Ink (#ecebe4). Filled-ink elements then switch to pure #000 behind the blue (`.dk` overrides).

### Neutral
- **Ivory Ground** (ivory-ground): page background, under a 48px grid of `rgba(0,0,0,.035)` lines.
- **Panel White** (panel-white): cards, tier rows, inputs, dialog.
- **Panel Recess** (panel-recess): operator cards at rest, talent blocks and the art frame. A step below Panel White.
- **Hairline** (hairline): 1px structural borders that carry no emphasis.
- **Muted Text** (muted-text): meta lines, labels, inactive tabs.
- **Stripe Gray** (stripe-gray): fill for the hatched ghost hero word.
- **Tooltip Slate** (tooltip-slate): glossary tooltip background in both themes, with #e9ebf2 text and an blue left edge.
- **Night set** (night-*): the dark-theme overrides for the same roles.

### Data colors
- **Rarity** (rarity-6 orange, rarity-5 gold, rarity-4 violet): only on the star glyphs (and the left edge of faction-list tiles). Each has a brighter dark-mode variant.
- **Tier ramp** (defined in JS as `TC`, not in CSS): a hue walk from hot to cool. EX uses a gradient (#ffe066→#ff3d6e). S+ #ff4d6d, S #ff7a45, S- #ffa94d, A+ #ffd43b, A #e3e86a, A- #b5e36a, B+ #69db7c, B #38d9a9, B- #3bc9db, C+ #4dabf7, C #748ffc, C- #9775fa, D #da77f2, F #868e96. Tier labels always sit on their tier color with near-black text (#0b0b0b) and a hatch overlay.

### Named Rules
**The One Signal Rule.** Arknights blue is the only accent. Never add a second brand hue. New emphasis is blue-on-ink or ink-on-blue. The blue (#0098dc) is the signature cyan-blue of the original Arknights UI. It replaced the acid yellow, which fought the gold 6★ cards.

**The Data-Only Color Rule.** Rarity and tier hues encode game data and never decorate chrome. A colored element should always answer "which rarity?" or "which tier?".

## Typography

**Display Font:** Be Vietnam Pro (with system-ui, sans-serif)
**Body Font:** Be Vietnam Pro, 400–900
**Label/Mono Font:** Chakra Petch (with ui-monospace, monospace), 500–700

**Character:** Be Vietnam Pro carries Vietnamese diacritics cleanly from body text up to 900-weight display. Chakra Petch's squared terminals supply the HUD voice. Its job is labeling and numbers, not long reading.

### Hierarchy
- **Display** (900, clamp(40px, 7vw, 96px), 0.95): page H1, in uppercase with tight tracking. Its last word sits on an blue block with an 8px ink offset shadow. The H1 changes with the tab (e.g. "Bảng xếp hạng / Operator", "Lịch sử / thay đổi"). The update stamp ("Cập nhật … · Server Global") sits under the H1 as a muted label with a small blue square; there is no eyebrow above the heading. The hero ghost word uses the same face at clamp(120px, 22vw, 360px), hatched and outlined.
- **Headline** (Chakra Petch 700, 26px): the operator name in the modal, uppercase, in `[ ]`.
- **Title** (Chakra Petch 700, 20px, 0.04em): card headings, uppercase, in `[ ]`. Section dividers use 14px with 0.14em tracking and a diamond marker.
- **Body** (Be Vietnam Pro 400, 15px, 1.6): notes, descriptions and skill text (14px in dense blocks). Note bodies use `pre-line` to keep the authors' line breaks.
- **Label** (Chakra Petch 600, 12px, 0.08–0.2em, uppercase): tabs, chips, stat captions, meta lines, tags and `dt` keys.
- **Tier mark** (Chakra Petch 700, 34px on desktop, 22px on mobile and in the matrix): the tier letter.

**Fluid scale:** every font size is set in `rem`, and the root size scales with the viewport (`clamp(16px, 14.5px + .4vw, 18px)`). Phones get the px values listed here, and wide screens get up to 12.5% more. New font sizes must use `rem` (px ÷ 16).

### Named Rules
**The 12px Floor Rule.** No text below 12px. Small labels are forced to 12px.

**The Mono-Is-Metadata Rule.** Chakra Petch is for labels, numbers and headings. Body text, notes and translated descriptions stay in Be Vietnam Pro.

## Layout

- **Desktop:** a fixed 76px vertical rail on the left with the logo, vertical-text tabs and the theme toggle. Content sits in a centered wrap up to 1400px wide with 24px gutters.
- **Mobile (≤760px):** the rail becomes a 56px top bar with horizontal scrolling tabs. Gutters drop to 16px. Filters collapse behind a floating "LỌC" button into a bottom sheet (max 75vh). Operator cards go two per row. Tier labels narrow to 56px.
- **Tier rows:** a 96px label column next to wrapping operator cards with a 6px gap and 12px padding. The matrix view is a horizontally scrolling table with a 1100px minimum width.
- **Controls:** sticky under the top edge on desktop with a translucent blurred ground and a 2px ink bottom rule. Static on mobile.
- **Rhythm:** spacing comes in 4 / 6 / 10 / 14 / 24px steps. Cards use 24px padding. The About grid uses auto-fill columns with a 320px minimum.
- **Modal:** width min(1040px, 100% − 32px), max height 85vh. The profile is a two-column grid (1fr + 340px) that stacks below 760px with the art first.

## Elevation & Depth

Flat by default. Depth is printed, not lit: solid offset shadows with zero blur in Arknights blue or ink. They appear on interaction (hover, focus) or to mark the one foreground object (dialog, FAB).

### Shadow Vocabulary
- **Hover lift** (`box-shadow: 3px 3px 0 var(--accent)` plus `translate(-2px,-2px)`): operator cards on hover.
- **Focus print** (`box-shadow: 4px 4px 0 var(--accent)`): the search input on focus.
- **Floating control** (`box-shadow: 4px 4px 0 var(--accent)`): FAB and back-to-top.
- **Headline block** (`box-shadow: 8px 8px 0 var(--ink)`): the blue word in the H1.
- **Dialog** (`box-shadow: 10px 10px 0 var(--accent)`): the operator modal.
- **Ambient exceptions** (blurred): the glossary tooltip (`0 10px 30px rgba(0,0,0,.35)`) and the mobile filter sheet (`0 -12px 40px rgba(0,0,0,.25)`). These are the only soft shadows because they float above content.

### Named Rules
**The Print Shadow Rule.** Shadows are solid offsets with no blur, always down and to the right. Blur is allowed only for overlays that float over content.

## Shapes

Every surface has square corners (0 radius), including inputs, dialogs, chips and buttons. The only exception is the circular avatar. Angular form shows up through clip-paths and rotations: the logo tile has a cut bottom-right corner, and timeline and section markers are 45° diamonds. Cards get a 24px ink corner bracket at the top left. Borders follow a two-tier logic: a 1px hairline for structure, and 1–2px ink when an element is framed, active or hovered.

## Components

### Buttons and Chips
- **Character:** terse HUD toggles.
- **Shape:** square, at least 44px tall, 0 14px padding, Chakra Petch 12px uppercase.
- **Default:** panel white with a hairline border and muted text. On hover the border and text turn ink.
- **Active (`aria-pressed`):** an ink fill with blue text.
- **Focus:** a 2px ink outline with a 2px offset.
- **Close button (modal):** an ink square with an blue ✕, at least 44×44px.
- **FAB / Back to top:** an ink square, 48px tall, with blue text and an blue print shadow.

### Inputs
- **Search:** panel white, 1px ink border, square, with an icon inset at 14px on the left. On focus it shows an blue print shadow and no outline ring.

### Navigation
- **Desktop rail:** tabs with vertical text (rotated 180°), Chakra Petch 12px uppercase in muted text. The active tab is filled blue with a 4px ink bar on its left. A 3×120px blue stripe tops the rail's right edge.
- **Mobile:** horizontal tabs. The active bar moves to the bottom (3px).

### Tier Row (signature)
A panel with a hatched tier-color label cell (the tier letter only; descriptors would add judgments the source does not make) and wrapping operator cards. The row's border turns ink on hover and the hatch slides.

### Tier jump bar
It sits right above the board and sticks to the top edge (under the 56px top bar on mobile) while you scroll the tier list. It holds one 44px square button per tier that has operators, filled with that tier's color, with the tier letter in Chakra Petch. Pressing a button scrolls to that row. The bar is hidden in the matrix view and when only one tier is left after filtering. Inside each row, the tier letter is sticky just below the bar, so a long row never loses its label.

### History and back
Each tab change, opened dossier and faction jump is one browser history step. The browser or phone Back button closes a dossier, returns from a faction to the dossier that linked to it, and walks back through tabs. Closing a dossier with ✕, Esc or the backdrop also steps back. ←/→ inside a dossier replaces the current step rather than stacking new ones. When a faction is opened from a dossier, a sticky ink button with blue text, "← Quay lại hồ sơ <name>", sits at the top of the faction tab.

### Search shortcut
Pressing `/` focuses the search field, unless you are typing elsewhere or a dossier is open. On desktop a small `/` key hint sits in the field and hides on focus.

### Operator Card (signature)
A tile filled with its rarity gradient (6★ gold, 5★ pale yellow, 4★ lilac, defined as `--b6` … `--b1` with dark-mode variants; text stays #111 on it). It has a 42px round avatar, a bold name with an `IS` tag for Integrated Strategies entries, and a mono meta line with stars and class/subclass icons. The general-mode twin carries no tag. On hover the card lifts by −2px with a blue print shadow. A near-black (#0b0b0b) panel fills it from the right edge to the left (a `clip-path` wipe, .38s), covering the avatar, name, stars and icons. The panel shows the operator's face: the avatar image, scaled to about ¾ of the card width, anchored right and fading into black on the left. Behind the face sits the operator name in 900-weight uppercase, outlined at 22% white with no fill. It is allowed to run off the card and to be covered by the face. Cards without an image skip the effect. The gradient is a deliberate exception to Panel Recess: it answers "which rarity?" at a glance.

### Cards / Containers
- **Corner Style:** square, with a 24px ink L-bracket at the top left.
- **Background:** panel white, 1px hairline border, 24px padding.
- **Headings:** Chakra Petch uppercase in `[ ]`.

### Operator Dialog
An ink frame with an blue print shadow. The sticky header has hatching, a 76px avatar and the name in `[ ]`. The Trait block is ink with keywords on blue. The stats grid is a 4-column ink-ruled table (2 columns on mobile). Skills are rows with a 56px icon. Talents have a 4px ink left rule. The range grid uses 16px cells: blue for range, ink for the operator.

### Update feed (Mới)
Grouped by update, newest first. Each group has a Chakra Petch heading ("Tháng 10/2026") with the event name as a muted label beside it, then a grid of cards: avatar, name, stars and class, the tier badge, the translated note (omitted when the source has none) and a "Xem hồ sơ operator" chip. A badge takes the color of the tier it names ("Lên EX" → EX). A badge with no tier ("Không đổi") is ink with blue text.

### Mobile filter sheet
It opens over a 45% black scrim. Tapping the scrim, pressing Esc or tapping ĐÓNG closes it. When tabs are cut off at the right edge, the mobile tab bar fades out there.

### Timeline (Lịch sử)
A 2px ink spine with blue diamond nodes and dates as ink tags with blue text.

### Glossary Tooltip
A slate panel with light text, a 4px blue left edge and a Chakra Petch term heading. Triggered by underlined keywords that are focusable.

## Do's and Don'ts

### Do:
- **Do** use Arknights blue (#0098dc) only as signal: active state, focus, highlight, print shadow.
- **Do** keep every corner square. Only avatars are round.
- **Do** set labels, tabs, numbers and headings in Chakra Petch uppercase with 0.08–0.2em tracking, and wrap card and modal titles in `[ ]`.
- **Do** use solid offset shadows (3–10px, no blur) for interaction and foreground emphasis.
- **Do** define every new color as a `:root` token with a dark-mode override in both the `prefers-color-scheme` block and the `[data-theme=dark]` block.
- **Do** keep touch targets at 44px or more and text at 12px or more.
- **Do** keep the existing motion vocabulary (rise, wipe, pop, fade on `--ease: cubic-bezier(.22,1,.36,1)`), only on entry or interaction, and switch it all off under `prefers-reduced-motion`.

### Don't:
- **Don't** introduce rounded corners, pill shapes or a second accent hue.
- **Don't** use blurred drop shadows on in-flow surfaces. Blur is for floating overlays only.
- **Don't** use rarity or tier colors for decoration or UI chrome.
- **Don't** set body text or translated notes in Chakra Petch.
- **Don't** put light text on Arknights blue. Text on blue is always #111, including the footer in dark mode.
- **Don't** add infinite loops, decoding text, scan bars or other fake-HUD motion. Owner-requested exceptions: the slow blue background scan band (`body:after`, 9s). The one exception, kept at the owner's request: the blue H1 word types and deletes itself in a loop, with a blinking cursor; the h1 carries an aria-label with the full title.
- **Don't** put an eyebrow or kicker label above a heading.
