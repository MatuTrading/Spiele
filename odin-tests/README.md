# Odin Tests

Browser smoke tests for HTML5/Three.js games. Run `python -m http.server 8000` at repository root, then `python odin-tests/smoke.py http://127.0.0.1:8000/index.html`.

Tests check mobile/desktop viewport, JS errors, canvas, WebGL and screenshots. They do not prove animation or gameplay correctness. Browser policies may block navigation.
