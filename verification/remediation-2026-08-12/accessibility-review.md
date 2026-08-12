# Accessibility review — TestForge

Receipt: `TESTFORGE-A11Y-0c93516-ff21cef0-20260812`

- Bound commit: `0c935166bc35baafb39108dd888812e64023c0aa`
- Bound fingerprint: `ff21cef0cb1e7155769a9a4a06688b2b240eb2662c0dc6ca92c1cfb57d71fee7`
- Result: `PASS — STATIC AND SOURCE REVIEW`; deployed-candidate browser and assistive-technology behavior is NOT TESTED because the candidate is not published

## Checks and evidence

- Language and structure: `lang=en`, one page-level H1, ordered H2/H3 hierarchy, `header`, labeled `nav`, `main`, sections, and footer.
- Keyboard path: visible-on-focus skip links on index and 404; native anchors; horizontally scrollable narrow navigation; focusable evidence-table wrapper.
- Images: final Pages hero declares 1200×800 intrinsic dimensions and meaningful alternative text. Decorative brand mark is hidden from assistive technology.
- Motion: no scripted animation; `prefers-reduced-motion` disables smooth scrolling.
- Reflow: grids collapse at 58rem and 40rem; mobile navigation remains present and horizontally scrollable instead of disappearing.
- Table: native table headings plus a labeled, focusable overflow wrapper.
- Contrast calculations (WCAG relative luminance): `#8f1111/#f9fbfb` 8.962:1; `#5b0808/#f9fbfb` 13.634:1; `#59686f/#edf1f2` 5.081:1; `#a8b6bd/#010203` 9.978:1; `#ff7777/#010203` 8.066:1; dark focus `#ffd166/#010203` 14.401:1; light focus `#6b4c00/#f9fbfb` 7.604:1 and `#6b4c00/#edf1f2` 6.945:1.
- Recovery: custom 404 keeps navigation, a clear error statement, and routes back to start or troubleshooting.

## Limitations

No claim is made for screen-reader output, browser accessibility-tree behavior, zoom/reflow in a deployed browser, or live keyboard traversal. Those require the final candidate to be published and directly exercised; they remain part of the publication blocker.

Any governed-file change invalidates this receipt.
