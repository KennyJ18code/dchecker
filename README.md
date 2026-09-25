# D-Checker Cycle Viewer

Daikin D-Checker CSV logs on a live refrigerant-circuit diagram, with playback, trend pinning, targets and diagnostic signatures. Runs entirely in the browser; no data leaves the device.

- `index.html` — the app (built from `template.html` + `sample.csv`)
- `template.html` — source; `__SAMPLE_CSV__` is replaced by the demo log at build
- `sw.js`, `manifest.webmanifest`, `icons/` — installable web app (Add to Home Screen)

Build: replace `__SAMPLE_CSV__` in `template.html` with the contents of `sample.csv` and write `index.html`.
