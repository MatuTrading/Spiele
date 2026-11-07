import json
import unittest
from pathlib import Path

from scripts.validate_assets import inspect_glb

BASE = Path(__file__).parents[1]

class ManifestTests(unittest.TestCase):
    def test_example_manifests(self):
        for file in (BASE/'jobs').glob('*.json'):
            j=json.loads(file.read_text())
            self.assertEqual(j['schema_version'],1)
            self.assertIn(j['kind'],('character','world'))
            self.assertRegex(j['job_id'],r'^[a-z][a-z0-9-]{2,40}$')
            self.assertLessEqual(j['render_size'],1024)
            self.assertLessEqual(j['render_samples'],32)
            if j['kind']=='character': self.assertEqual(len(j['animations']),6)
    def test_invalid_glb_rejected(self):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.glb') as f:
            f.write(b'nope');f.flush()
            with self.assertRaises(ValueError): inspect_glb(Path(f.name))

if __name__ == '__main__':unittest.main()
