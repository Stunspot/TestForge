# TestForge site source

The static project site is published from this `docs/` directory.

## Source and evidence boundary

The site describes the public TestForge repository and the complete Augment, plugin, standalone-skill, and behavioral-evaluation materials retained here. Its product claims are derived from:

- `README.md`, `BUILD-WEEK.md`, and `JUDGE-QUICKSTART.md`;
- `testforge/skills/software-verification/SKILL.md`;
- `testforge/skills/verification-reviewer/SKILL.md`;
- the verification doctrine, schemas, examples, deterministic tools, release notes, custody record, and limitations;
- `tools/augment-evals/README.md` and the included evaluation contract, adapters, baselines, and regression machinery.

The page does not claim defect freedom, compliance certification, production access, release authority, universal host behavior, marketplace approval, or that structural validation proves software correctness or test quality.

## Files

- `index.html` — semantic single-page project overview;
- `style.css` — responsive presentation and accessibility treatment;
- `assets/testforge-hero.png` — generated 1600×900 raster hero artwork;
- `.nojekyll` — direct static-file serving marker.

## Deployment

`.github/workflows/deploy-pages.yml` uploads this directory with GitHub's official Pages Actions. Repository Pages must be configured to use **GitHub Actions** before the first deployment can publish.

## Review notes

The page uses one H1, semantic landmarks, a skip link, visible keyboard focus, descriptive links, meaningful alternative text, responsive layout, and reduced-motion handling. These checks support structural accessibility only; they are not a claim of formal accessibility conformance, browser coverage, test effectiveness, security, software correctness, or representative-user success.
