"""Check the reviewed aggregate CSV. No packages, network or GPU required."""
import csv, math, sys
from pathlib import Path

def verify(path):
    rows = list(csv.DictReader(Path(path).open()))
    expected = {'Frozen EXL': 2, 'Tuned EXL': 2, 'Strata serial': 2,
                'NInfer-ext': 1, 'Stock llama.cpp': 1, 'BeeLlama': 1}
    assert len(rows) == 9, 'Expected nine completed rows'
    seen = set()
    for r in rows:
        key = (r['profile'], r['mode'])
        assert key not in seen, f'Duplicate row: {key}'
        seen.add(key)
        assert r['profile'] in expected and r['mode'] in ('cold', 'warm')
        assert r['mode'] == 'cold' or expected[r['profile']] == 2
        output = int(r['output_tokens'])
        wall = float(r['wall_seconds'])
        assert output == 8192 and math.isfinite(wall) and wall > 0
        assert math.isclose(float(r['wall_tok_s']), output / wall, rel_tol=1e-10)
        reserve = 8 if r['profile'] == 'Strata serial' else (2 if r['profile'] in ('Stock llama.cpp', 'BeeLlama') else 0)
        assert int(r['prompt_tokens']) + output + reserve <= 262144
        assert int(r['gpus']) == (1 if r['profile'] == 'NInfer-ext' else 2)
        assert 0 < float(r['ttft_seconds']) < wall
    for profile, count in expected.items():
        assert sum(r['profile'] == profile for r in rows) == count
    return len(rows)

if __name__ == '__main__':
    count = verify(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name('full-window.csv'))
    print(f'PASS: {count} completed rows, wall arithmetic, native token budgets and GPU counts')
