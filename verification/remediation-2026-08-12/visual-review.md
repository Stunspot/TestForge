# Visual asset review — TestForge

Receipt: `TESTFORGE-VISUAL-441a22b-20260812`

All three final files were reopened at original detail and their actual pixels were inspected.

| Role | File | Dimensions | SHA-256 | Pixel verdict |
|---|---|---:|---|---|
| README hero | `assets/testforge-readme-hero.png` | 1600×640 | `6891298c9e6d0cea15e72a249ecaba2d6546dbe841578b239ad19dc0d2b09a03` | PASS — wide evidence-forging bench, clear left-to-right hierarchy, focused crack/failure detail, strong cyan/red TestForge identity, no text, blank field, accidental transparency, or crop-critical edge content |
| Pages hero | `docs/assets/testforge-hero.png` | 1200×800 | `f639f84c2c597053ca04c010be36201c46011596dfbeec9b7ca4e76e38a68bf8` | PASS — distinct vertical three-lane inspection machine, two cyan accept lanes and one red reject lane, centered for the site column, no embedded text or incoherent artifact |
| Social card | `assets/testforge-social-preview.png` | 1280×640 | `9eb81f699f7b8bfdfa4b6ec41cee2883563d1d8de79bed2298167b90c212ec12` | PASS — exact visible title `TESTFORGE` and line `SOFTWARE VERIFICATION THAT ARGUES BACK.` are crisp, high-contrast, and safely inset; the anvil/evidence-tree composition remains identifiable under likely social crop |

The files are distinct compositions and aspect ratios (2.5:1, 1.5:1, 2:1), not duplicated crops. README and Pages source wiring are correct. Pages Open Graph/Twitter wiring uses the social card. GitHub’s configured repository Open Graph bytes match the same social-card SHA-256.

Any governed-file change invalidates this receipt.
