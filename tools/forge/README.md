# Odin Character Forge V15

`../../Odin_Character_Forge.html` is the standalone, offline-capable application. It bundles the original Three.js modules, ten KayKit characters and 132 animation clips from the user-provided V14. No account or network call is required for editing or exporting. The embedded JavaScript libraries are minified with esbuild for the published file; model and animation data are unchanged.

## Changes

- Persistent 3D viewport with independently scrolling editors, four touch navigation tabs and a landscape layout.
- Corrected directional-light shadow bias to remove visible self-shadow striping on faces and hair.
- Camera presets, turntable, grid toggle, PNG download and rendering quality controls.
- Searchable animation list, pause/resume, speed and pose scrubbing with the final frame kept within the selected clip.
- Bounded undo/redo history, local draft persistence and live character naming.
- JSON recipe validation before changing the figure; recipes restore all parts, colors and animation.
- Texture-aware part recoloring, instead of multiplying the original palette by the selected color.
- GLB export in bind pose with zero, one or all 132 clips; diagnostic reimport validates skinning and finite vertex positions.
- Preserved original assets and compatibility families. No generated vampire geometry, weapons or cloud AI service is claimed.

## Rebuild

The original V14 input is not duplicated in this repository. Its SHA-256 is:

`981907769a27ad1d6404b74a46130aeeff098311addd5ee878af21c27a527235`

Run `python3 tools/forge/build_v15.py /absolute/path/to/Odin_Character_Forge_V14_KayKit_Regler_Farben_Offline.html` from the repository root. The script preserves embedded assets and writes `Odin_Character_Forge.html`. For the smaller published file, then run `python3 tools/forge/minify_embedded.py Odin_Character_Forge.html /absolute/path/to/esbuild` (esbuild 0.25.12, ES2020 target; legal comments preserved).

## Repeat the browser checks

Install Playwright 1.62.1 and @sparticuz/chromium 153.0.0 in an isolated runtime outside this repository. Use the packaged browser and SwiftShader in a local application-test environment. The runner accepts an explicit browser path if the package's automatic extraction does not work on the host.

```bash
FORGE_RUNTIME=/absolute/path/runtime FORGE_CHROMIUM=/absolute/path/chromium \
  node tools/forge/test_forge.cjs Odin_Character_Forge.html /absolute/path/evidence
```

Tests use actual clicks, selections, keyboard range controls, file uploads/downloads, pointer dragging and touch events. Read-only diagnostics check the visible model. A separate viewer renders a downloaded GLB. JSON output records the source SHA-256, checks and errors; screenshots require human/agent visual review.

The generic tower-defense `test_game.cjs` protocol is incompatible with Character Forge; this dedicated runner tests the Forge itself.

Software-rendered Chromium and emulated touch do not establish physical Android performance. Sampled animation poses do not prove that every frame of every possible mixed character is artistically correct. The GLB output is not a direct integration into the tower-defense game.
