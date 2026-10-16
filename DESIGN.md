---
name: Arknights Tier List VN
description: Bảng xếp hạng operator Arknights bản tiếng Việt, giao diện kiểu terminal tác chiến.
colors:
  acid-signal: "#fff200"
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
    textColor: "{colors.acid-signal}"
  nav-tab-active:
    backgroundColor: "{colors.acid-signal}"
    textColor: "{colors.field-ink}"
    typography: "{typography.label}"
  input-search:
    backgroundColor: "{colors.panel-white}"
    textColor: "{colors.field-ink}"
    rounded: "{rounded.none}"
    padding: "11px 14px 11px 40px"
  operator-card:
    backgroundColor: "{colors.panel-recess}"
    textColor: "{colors.field-ink}"
    rounded: "{rounded.none}"
    padding: "5px 12px 5px 5px"
  kicker:
    backgroundColor: "{colors.field-ink}"
    textColor: "{colors.acid-signal}"
    typography: "{typography.label}"
    padding: "6px 12px"
  fab:
    backgroundColor: "{colors.field-ink}"
    textColor: "{colors.acid-signal}"
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

The site reads like a Rhodes Island tactical terminal in the visual language of Arknights: Endfield. Ivory paper sits on a faint 48px blueprint grid. Ink-black frames hold acid-yellow signals. Labels look like HUD readouts in a squared techno face, wrapped in `[ ]` brackets. Diagonal hatching marks anything that is a classification, such as tier labels, the modal header and the art frame. A giant striped "TIER" ghost word anchors the hero. Each operator is an entry in a field manual, so information is dense, framed and scannable.

The system is hard-edged and flat. It has no radii except the circular avatar. Depth comes from offset solid "print" shadows in acid yellow or ink, never from blur. Dark mode flips the paper to near-black graphite and keeps the acid yellow as the one constant signal.

Motion is part of the identity and stays as it is: a staggered rise on tier rows, wipe reveals on the hero and tier labels, a slowly scrolling stripe behind the hero word, and a lift-and-offset hover on operator cards. All of it switches off under `prefers-reduced-motion`.

**Key Characteristics:**
- Acid yellow (#fff200) on ink (#111) is the one signal pair. Everything else is neutral or a data color.
- Square corners everywhere. Only avatars are round.
- Offset hard shadows (3–10px, no blur) instead of soft elevation.
- Chakra Petch in uppercase with wide tracking for every label, tab, stat and heading. Be Vietnam Pro for reading text.
- A vertical left rail for navigation on desktop, which becomes a top bar on mobile.
- Hatching (−45° stripes) and `[ ]` brackets as the recurring HUD ornaments.

## Colors

An industrial two-tone of acid yellow and ink on warm ivory paper, with data colors reserved for rarity and tier.

### Primary
- **Acid Signal** (acid-signal): the one accent. It marks the active nav tab, selection highlight, link underlines, search focus shadow, offset shadows on hover and dialogs, keyword highlights in skill text, range-grid cells, the footer band and the "MỚI" tag. On ink it becomes the text color, as in chips, kickers, tags and table headers.
- **Field Ink** (field-ink): frames, borders that carry meaning, active chips, the rail's active bar, the trait block background and the sticky controls' 2px rule. In dark mode it becomes Night Ink (#ecebe4). Filled-ink elements then switch to pure #000 behind the yellow (`.dk` overrides).

### Neutral
- **Ivory Ground** (ivory-ground): page background, under a 48px grid of `rgba(0,0,0,.035)` lines.
- **Panel White** (panel-white): cards, tier rows, inputs, dialog.
- **Panel Recess** (panel-recess): operator cards at rest, talent blocks and the art frame. A step below Panel White.
- **Hairline** (hairline): 1px structural borders that carry no emphasis.
- **Muted Text** (muted-text): meta lines, labels, inactive tabs.
- **Stripe Gray** (stripe-gray): fill for the hatched ghost hero word.
- **Tooltip Slate** (tooltip-slate): glossary tooltip background in both themes, with #e9ebf2 text and an acid left edge.
- **Night set** (night-*): the dark-theme overrides for the same roles.

### Data colors
- **Rarity** (rarity-6 orange, rarity-5 gold, rarity-4 violet): only on the avatar's dashed ring and the star glyphs. Each has a brighter dark-mode variant.
- **Tier ramp** (defined in JS as `TC`, not in CSS): a hue walk from hot to cool. EX uses a gradient (#ffe066→#ff3d6e). S+ #ff4d6d, S #ff7a45, S- #ffa94d, A+ #ffd43b, A #e3e86a, A- #b5e36a, B+ #69db7c, B #38d9a9, B- #3bc9db, C+ #4dabf7, C #748ffc, C- #9775fa, D #da77f2, F #868e96. Tier labels always sit on their tier color with near-black text (#0b0b0b) and a hatch overlay.

### Named Rules
**The One Signal Rule.** Acid yellow is the only accent. Never add a second brand hue. New emphasis is yellow-on-ink or ink-on-yellow.

**The Data-Only Color Rule.** Rarity and tier hues encode game data and never decorate chrome. A colored element should always answer "which rarity?" or "which tier?".

## Typography

**Display Font:** Be Vietnam Pro (with system-ui, sans-serif)
**Body Font:** Be Vietnam Pro, 400–900
**Label/Mono Font:** Chakra Petch (with ui-monospace, monospace), 500–700

**Character:** Be Vietnam Pro carries Vietnamese diacritics cleanly from body text up to 900-weight display. Chakra Petch's squared terminals supply the HUD voice. Its job is labeling and numbers, not long reading.

### Hierarchy
- **Display** (900, clamp(40px, 7vw, 96px), 0.95): page H1, in uppercase with tight tracking. Its last word sits on an acid block with an 8px ink offset shadow. The hero ghost "TIER" uses the same face at clamp(120px, 22vw, 360px), hatched and outlined.
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

Flat by default. Depth is printed, not lit: solid offset shadows with zero blur in acid yellow or ink. They appear on interaction (hover, focus) or to mark the one foreground object (dialog, FAB).

### Shadow Vocabulary
- **Hover lift** (`box-shadow: 3px 3px 0 var(--accent)` plus `translate(-2px,-2px)`): operator cards on hover.
- **Focus print** (`box-shadow: 4px 4px 0 var(--accent)`): the search input on focus.
- **Floating control** (`box-shadow: 4px 4px 0 var(--accent)`): FAB and back-to-top.
- **Headline block** (`box-shadow: 8px 8px 0 var(--ink)`): the acid word in the H1.
- **Dialog** (`box-shadow: 10px 10px 0 var(--accent)`): the operator modal.
- **Ambient exceptions** (blurred): the glossary tooltip (`0 10px 30px rgba(0,0,0,.35)`) and the mobile filter sheet (`0 -12px 40px rgba(0,0,0,.25)`). These are the only soft shadows because they float above content.

### Named Rules
**The Print Shadow Rule.** Shadows are solid offsets with no blur, always down and to the right. Blur is allowed only for overlays that float over content.

## Shapes

Every surface has square corners (0 radius), including inputs, dialogs, chips and buttons. The only exception is the circular avatar with its dashed rarity ring. Angular form shows up through clip-paths and rotations: the logo tile has a cut bottom-right corner, kickers carry a triangle pip, and timeline and section markers are 45° diamonds. Cards get a 24px ink corner bracket at the top left. Borders follow a two-tier logic: a 1px hairline for structure, and 1–2px ink when an element is framed, active or hovered.

## Components

### Buttons and Chips
- **Character:** terse HUD toggles.
- **Shape:** square, at least 44px tall, 0 14px padding, Chakra Petch 12px uppercase.
- **Default:** panel white with a hairline border and muted text. On hover the border and text turn ink.
- **Active (`aria-pressed`):** an ink fill with acid text.
- **Focus:** a 2px ink outline with a 2px offset.
- **Close button (modal):** an ink square with an acid ✕, at least 44×44px.
- **FAB / Back to top:** an ink square, 48px tall, with acid text and an acid print shadow.

### Inputs
- **Search:** panel white, 1px ink border, square, with an icon inset at 14px on the left. On focus it shows an acid print shadow and no outline ring.

### Navigation
- **Desktop rail:** tabs with vertical text (rotated 180°), Chakra Petch 12px uppercase in muted text. The active tab is filled acid with a 4px ink bar on its left. A 3×120px acid stripe tops the rail's right edge.
- **Mobile:** horizontal tabs. The active bar moves to the bottom (3px).

### Tier Row (signature)
A panel with a hatched tier-color label cell (letter plus a small descriptor such as "Đỉnh meta") and wrapping operator cards. The row's border turns ink on hover and the hatch slides.

### Operator Card (signature)
A recessed tile with a 42px round avatar (dashed rarity ring), a bold name, and a mono meta line with stars and tags. On hover it lifts by −2px with an acid print shadow and the portrait zooms to 1.12.

### Cards / Containers
- **Corner Style:** square, with a 24px ink L-bracket at the top left.
- **Background:** panel white, 1px hairline border, 24px padding.
- **Headings:** Chakra Petch uppercase in `[ ]`.

### Operator Dialog
An ink frame with an acid print shadow. The sticky header has hatching, a 76px avatar and the name in `[ ]`. The Trait block is ink with keywords on acid. The stats grid is a 4-column ink-ruled table (2 columns on mobile). Skills are rows with a 56px icon. Talents have a 4px ink left rule. The range grid uses 16px cells: acid for range, ink for the operator.

### Timeline (Lịch sử)
A 2px ink spine with acid diamond nodes and dates as ink tags with acid text.

### Glossary Tooltip
A slate panel with light text, a 4px acid left edge and a Chakra Petch term heading. Triggered by underlined keywords that are focusable.

## Do's and Don'ts

### Do:
- **Do** use acid yellow (#fff200) only as signal: active state, focus, highlight, print shadow.
- **Do** keep every corner square. Only avatars are round.
- **Do** set labels, tabs, numbers and headings in Chakra Petch uppercase with 0.08–0.2em tracking, and wrap card and modal titles in `[ ]`.
- **Do** use solid offset shadows (3–10px, no blur) for interaction and foreground emphasis.
- **Do** define every new color as a `:root` token with a dark-mode override in both the `prefers-color-scheme` block and the `[data-theme=dark]` block.
- **Do** keep touch targets at 44px or more and text at 12px or more.
- **Do** keep the existing motion vocabulary (rise, wipe, pop, fade on `--ease: cubic-bezier(.22,1,.36,1)`) and switch it all off under `prefers-reduced-motion`.

### Don't:
- **Don't** introduce rounded corners, pill shapes or a second accent hue.
- **Don't** use blurred drop shadows on in-flow surfaces. Blur is for floating overlays only.
- **Don't** use rarity or tier colors for decoration or UI chrome.
- **Don't** set body text or translated notes in Chakra Petch.
- **Don't** put light text on acid yellow. Text on acid is always #111.
