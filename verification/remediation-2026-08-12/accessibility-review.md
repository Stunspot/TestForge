# Accessibility review — TestForge

Receipt: `TESTFORGE-A11Y-441a22b-af19aa44-20260812`

- Bound commit: `441a22b8ac1f6fda9c4d7ba355f5cca19f365d1c`
- Bound fingerprint: `af19aa440e63bfd1d4fd8e4d9e6c516dabf03892747743b1de138600e191c7b3`
- Result: `PASS — STATIC/SOURCE REVIEW`; GUI browser and assistive-technology behavior remain `NOT TESTED`

## Checks and evidence

- `lang=en`, one page-level H1, ordered H2/H3 hierarchy, semantic header/nav/main/section/footer landmarks, labeled navigation, and a maintained 404 recovery journey.
- Skip links on index and 404; native anchors; visible `:focus-visible` outlines; mobile navigation remains present and horizontally scrollable; the overflow table wrapper is keyboard-focusable and labeled.
- The Pages hero has meaningful alt text and declared intrinsic dimensions. The brand glyph is correctly hidden from assistive technology.
- Responsive breakpoints at 76rem, 58rem, and 40rem; content grids collapse; no scripted animation; reduced-motion preference disables smooth scrolling.
- Native table headers are retained. Code and long status labels use wrapping/overflow controls rather than clipping.
- Measured WCAG relative-luminance contrast: `#8f1111/#f9fbfb` 8.962:1; `#5b0808/#f9fbfb` 13.634:1; `#59686f/#edf1f2` 5.081:1; `#a8b6bd/#010203` 9.978:1; `#ff7777/#010203` 8.066:1; dark focus 14.401:1; light focus 7.604:1 and 6.945:1.
- Hesperos accessible-Markdown lint: 46 documents clean; only the verbatim MIT license clause triggers the directional-word heuristic and is intentionally exempt.

## Explicit untested boundary

Screen-reader announcement, browser accessibility-tree behavior, live tab order, keyboard traversal, zoom/reflow in an actual browser, high-contrast mode, and representative disabled-user testing were not executed. Static source evidence does not establish formal accessibility conformance.

Any governed-file change invalidates this receipt.
