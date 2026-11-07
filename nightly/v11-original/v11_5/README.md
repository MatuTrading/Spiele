# ODIN Private Markets Tycoon V11.5 – Simplification candidate

Base: verified original-based V11.4 under ../source/ and ../v11_4/part_022.txt, both unchanged.

Build: python nightly/v11-original/v11_5/assemble.py. The result is a single offline HTML (around 9.4 MB) generated from verified V11.4 plus upgrade.js.

Changes:
- One clear contextual next-step sentence replaces generic decorative copy in the main decision header.
- More intuitive labels for calling LP capital and distributing proceeds.
- Completed four-stage tutorial disappears automatically, freeing visual space.
- Mobile keyboard focus rings, minimum action target sizes and reduced-motion safeguard.

QA: python nightly/v11-original/v11_5/qa_smoke.py tests four Chromium viewports, real navigation, payout alerts, contextual hint, capital labels and tutorial completion. Results must be verified in CI before declaring V11.5 stable. V11.4 remains fallback until green.
