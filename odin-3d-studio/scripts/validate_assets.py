#!/usr/bin/env python3
"""Dependency-free structural validator for ODIN-generated GLB files."""
import argparse
import json
import struct
from pathlib import Path


def inspect_glb(path):
    with path.open('rb') as stream:
        header = stream.read(12)
        if len(header) != 12:
            raise ValueError('GLB header truncated')
        magic, version, length = struct.unpack('<4sII', header)
        if magic != b'glTF' or version != 2 or length != path.stat().st_size:
            raise ValueError('Invalid GLB header, version or byte length')
        chunk = stream.read(8)
        if len(chunk) != 8:
            raise ValueError('Missing JSON chunk')
        json_length, json_type = struct.unpack('<I4s', chunk)
        if json_type != b'JSON' or json_length > 32_000_000:
            raise ValueError('Invalid JSON chunk')
        gltf = json.loads(stream.read(json_length))
        binary = stream.read(8)
        if len(binary) != 8:
            raise ValueError('Missing BIN chunk')
        bin_length, bin_type = struct.unpack('<I4s', binary)
        if bin_type != b'BIN' or bin_length < 1:
            raise ValueError('Invalid binary chunk')
        remaining = stream.read()
        if len(remaining) != bin_length:
            raise ValueError('BIN chunk truncated')
        if json_length + bin_length + 28 != length:
            raise ValueError('GLB chunk sizes do not match container')
    return gltf


def validate(output, job):
    job = json.loads(Path(job).read_text(encoding='utf8'))
    path = Path(output) / (job['job_id'] + '.glb')
    assert path.is_file(), f'GLB missing: {path}'
    gltf = inspect_glb(path)
    assert gltf.get('asset', {}).get('version') == '2.0', 'Not glTF 2.0'
    assert gltf.get('meshes'), 'No meshes exported'
    assert gltf.get('nodes'), 'No scene nodes'
    assert gltf.get('scenes'), 'No scene'
    anims = [a.get('name', '') for a in gltf.get('animations', [])]
    if job['kind'] == 'character':
        assert gltf.get('skins'), 'No skeleton/skin exported'
        expected = set(job['animations'])
        missing = expected.difference(anims)
        assert not missing, f'Missing animation clips: {sorted(missing)}; found {anims}'
        assert all(a.get('channels') for a in gltf['animations']), 'Empty animation clip'
    images = list(Path(output).glob('preview_*.png'))
    assert len(images) >= 4, f'Need four preview images; got {len(images)}'
    for im in images:
        with im.open('rb') as f:
            assert f.read(8) == b'\x89PNG\r\n\x1a\n', f'Invalid PNG {im}'
        assert im.stat().st_size > 5000, f'Empty render: {im}'
    report = {
        'status': 'PASS', 'job': job['job_id'], 'glb_bytes': path.stat().st_size,
        'meshes': len(gltf['meshes']), 'skins': len(gltf.get('skins', [])),
        'animations': anims, 'renders': [p.name for p in images],
        'limitation': 'Container structure validated; browser/WebGL playback requires separate test'
    }
    (Path(output) / 'validation.json').write_text(json.dumps(report, indent=2), encoding='utf8')
    print(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', default='output')
    ap.add_argument('--job', required=True)
    args = ap.parse_args()
    validate(args.output, args.job)
