# Visual asset review — TestForge

Receipt: `TESTFORGE-VISUAL-0c93516-20260812`

All three final files were opened and their actual pixels inspected, not inferred from filenames or metadata.

| Role | File | Dimensions | SHA-256 | Pixel verdict |
|---|---|---:|---|---|
| README hero | `assets/testforge-readme-hero.png` | 1600×640 | `6891298c9e6d0cea15e72a249ecaba2d6546dbe841578b239ad19dc0d2b09a03` | PASS — wide evidence-forging bench, clear focal hierarchy, strong TestForge red/cyan identity, no embedded text, no accidental transparency or unusable crop |
| Pages hero | `docs/assets/testforge-hero.png` | 1200×800 | `f639f84c2c597053ca04c010be36201c46011596dfbeec9b7ca4e76e38a68bf8` | PASS — distinct vertical three-lane verification gate with a legible reject path; composed for the site column; no embedded text or incoherent artifacts |
| Social card | `assets/testforge-social-preview.png` | 1280×640 | `9eb81f699f7b8bfdfa4b6ec41cee2883563d1d8de79bed2298167b90c212ec12` | PASS — exact visible title `TESTFORGE` and identifying line `SOFTWARE VERIFICATION THAT ARGUES BACK.` remain clear in the safe center |

The files have different compositions and aspect ratios (2.5:1, 1.5:1, 2:1); neither generated hero is a crop or duplicate of the other or of the social card. README and Pages wiring pass locally. Pages Open Graph wiring points to the social card. GitHub repository Open Graph configuration is live and its downloaded bytes exactly match the reviewed social card SHA-256 `9eb81f699f7b8bfdfa4b6ec41cee2883563d1d8de79bed2298167b90c212ec12`.

Image generation mode: built-in image generation. README production prompt: a wide editorial evidence-forging bench where a verifier turns code, tests, logs, and risk cards into a sealed proof artifact, TestForge red/cyan/charcoal visual language, strong left-to-right composition, no words or logos. Pages production prompt: a precision three-lane verification gate with two cyan accepted evidence channels and one red rejected channel diverted to a separate tray, vertical site-hero composition, no words or logos.
