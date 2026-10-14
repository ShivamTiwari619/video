# Render the sizzle. Run from 2_usp_film/.
#   python3 rend_sizzle.py qa OUTDIR t1 t2 ...   -> one JPEG per time
#   python3 rend_sizzle.py A B                   -> frames A..B-1 at 90 samples/s into sizzle_frames/ (skips existing)
import sys, os, asyncio, pathlib
from playwright.async_api import async_playwright
URL = (pathlib.Path(__file__).resolve().parent / 'sizzle' / 'index.html').as_uri() + '?render'
FPS = 90; OUT = 'sizzle_frames'
async def run(times, out):
    os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--allow-file-access-from-files'], executable_path=os.environ.get('CHROME') or None); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.evaluate('window.ready')
        for name, t in times:
            await pg.evaluate(f'seek({t})'); await pg.screenshot(path=f'{out}/{name}.jpg', type='jpeg', quality=92)
        await b.close()
        if errs: print('ERR', errs[:3])
if __name__ == '__main__':
    if sys.argv[1] == 'qa': asyncio.run(run([(f'{float(x):06.2f}', float(x)) for x in sys.argv[3:]], sys.argv[2]))
    else:
        a, b = int(sys.argv[1]), int(sys.argv[2])
        todo = [(f'{i:05d}', i / FPS) for i in range(a, b) if not os.path.exists(f'{OUT}/{i:05d}.jpg')]
        if todo: asyncio.run(run(todo, OUT))
