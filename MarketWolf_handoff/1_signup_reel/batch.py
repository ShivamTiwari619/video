import sys, asyncio, os
from render import run
fps=60; a,b=int(sys.argv[1]),int(sys.argv[2])
todo=[(f'{i:05d}', i/fps) for i in range(a,b) if not os.path.exists(f"{os.environ.get('OUTDIR','frames')}/{i:05d}.jpg")]
if todo: asyncio.run(run(todo, os.environ.get('OUTDIR','frames')))
