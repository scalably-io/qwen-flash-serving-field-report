"""Render a recorded startup recipe for a new isolated root. Never launches it."""
import argparse, json, shlex
from pathlib import Path

def render(recipe, bench_root, cuda_root):
    def replace(value):
        if isinstance(value,dict):return {k:replace(v) for k,v in value.items()}
        if isinstance(value,list):return [replace(v) for v in value]
        if isinstance(value,str):return value.replace('<BENCH_ROOT>',str(bench_root)).replace('<CUDA_ROOT>',str(cuda_root))
        return value
    r=replace(json.loads(Path(recipe).read_text()))
    assert isinstance(r.get('command'),list) and all(isinstance(x,str) for x in r['command'])
    assert not any('<BENCH_ROOT>' in x or '<CUDA_ROOT>' in x for x in r['command'])
    return r

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('recipe',type=Path);p.add_argument('--bench-root',required=True,type=Path);p.add_argument('--cuda-root',default='/usr/local/cuda-12.8',type=Path)
    a=p.parse_args();r=render(a.recipe,a.bench_root,a.cuda_root)
    print('# Recorded command, rendered only. No process started or paths/builds validated.')
    print('cd '+shlex.quote(r['cwd']))
    for k,v in r.get('environment',{}).items():print('export '+k+'='+shlex.quote(v))
    print(shlex.join(r['command']))
