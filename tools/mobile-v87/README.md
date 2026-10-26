# Mobile Saga V87

This builds a separate candidate from the supplied V86 Meine-Spielwelt HTML. It does not replace the repository's live index.html. Original embedded world, figures, animations and music are preserved.

Install the pinned dependencies in an isolated runtime directory using this directory's package.json. Then, from the repository root:

```bash
python3 tools/mobile-v87/build_mobile.py /absolute/path/source-v86.html /absolute/path/candidate/index.html
node tools/mobile-v87/bundle.cjs /absolute/path/candidate/index.html /absolute/path/runtime
node tools/mobile-v87/test_mobile.cjs /absolute/path/candidate/index.html /absolute/path/mobile-evidence /absolute/path/runtime
node tools/mobile-v87/test_battle.cjs /absolute/path/candidate/index.html /absolute/path/battle-evidence /absolute/path/runtime
```

The bundler embeds Three.js and its required addons so the delivered single HTML can start without a CDN. Read build.json for the source and candidate SHA-256. The bundler must run once after each fresh build.

## Scenarios

The touch test covers building/upgrading, cancelling a sale, relocation, checkpoint reload, wave start, actual pause, menu pause preservation, 360px/412px portrait, landscape and desktop bounds, camera drag/pinch without unintended building, and a separate offline file startup.

The combat scenario explicitly starts from a saved-game fixture at completed wave 4 with 650 gold. It builds three upgraded classes through the real UI, tests wave 5 archetypes and frost, samples spacing, relocates an archer through a live wave and checks termination. It is not evidence of a naturally completed campaign or Android GPU speed. Inspect the screenshots yourself; state assertions alone do not certify animation quality.

Use a permitted browser/runtime. Do not change host security or network settings to overcome a startup error. Check the actual phone before making performance claims.
