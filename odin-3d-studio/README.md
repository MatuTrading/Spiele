# ODIN 3D Studio · Blender Pipeline

A branch-isolated, zero-paid-API Blender 3D pipeline intended for GitHub-hosted Ubuntu runners. **It is not a ChatGPT-to-Blender MCP connection.** ChatGPT authors small text manifests and scripts through the GitHub connector. GitHub Actions does the expensive generation and exposes GLB/PNG artifacts.

## Current scope

- `jobs/example_character.json`: stylized Viking archer with procedural torso, skin, armor, hair, hands, bow and arrow, one rig, six skeletal clips (Idle, Walk, Run, Attack, Hit, Death).
- `jobs/example_world.json`: primitive Viking camp with longhouses, trees, palisade, ground and campfire; no character animations.
- `scripts/build_asset.py`: headless Blender generator, GLB exporter, Cycles CPU preview renderer. Does not call paid services.
- `scripts/validate_assets.py`: verifies glTF 2 binary container sizes, meshes, skeleton and expected animation names, and 4+ real PNG previews. This is not equivalent to testing interactive WebGL playback or verifying beauty/physical realism.
- `viewer/index.html`: mobile-friendly Three.js viewer with local GLB import, orbit camera, animation picker and playback speed; requires network for CDN modules. It does not upload the file.

## How to run from normal ChatGPT

1. Request a new job in this conversation. ChatGPT makes a new JSON manifest or controlled Python change on `odin/blender-pipeline` using GitHub write permissions.
2. `push` workflow `.github/workflows/odin-blender.yml` runs only on this branch and only for `odin-3d-studio/**` or itself. **Note:** GitHub's own Actions policy and availability can block runs; this is distinct from repository write permission.
3. Open `https://github.com/MatuTrading/Spiele/actions/workflows/odin-blender.yml` and select the latest run for `odin/blender-pipeline`.
4. Download the `odin-blender-<run>` ZIP from the run's Artifacts section (requires GitHub login in some cases).
5. Extract `.glb` and `preview_*.png`. Open `viewer/index.html`, choose the GLB file, and check animations.
6. Share the run URL and/or screenshots with ChatGPT so visual issues can be analyzed. ChatGPT should only claim visual tests if it actually saw rendered images.

### Rerun without editing files

On GitHub Actions select **Run workflow**, choose branch `odin/blender-pipeline` and `example_character.json` or `example_world.json`. The push trigger also works if branch policy allows it. `workflow_dispatch` might need workflow registered on the default branch; use a push to the feature branch as fallback.

## Security and limits

- Workflow accepts only two whitelisted input files; no free-form code execution from a JSON field.
- Read-only `GITHUB_TOKEN` and no access to repository secrets.
- Capped sample counts and render size, `timeout-minutes: 35`.
- Large binaries are produced inside runner and stored as temporary Artifacts, not committed to repo.
- Public repository Actions are generally free for standard hosted runners within GitHub's terms; storage/retention, rate limits and availability still apply.
- Blender installed from Ubuntu 24.04's repositories (version printed in run log, not pinned to exact build). For strict bit-reproducibility, pin/download verified Blender binary in future.
- Generated archer is a **procedural proof of concept**, not yet production-grade art. Bow-string deformation, foot contact, arrow release, and true deformation-based skin weights need additional artistic iteration.
- No deployment or merge to `main` is performed.
