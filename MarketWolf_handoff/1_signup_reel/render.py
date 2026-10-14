import sys, asyncio, os
from playwright.async_api import async_playwright
async def run(times, outdir, prefix='f', fmt='jpeg'):
    os.makedirs(outdir, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width':1080,'height':1920})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file:///home/claude/moxie/reel/index.html?render&mode='+os.environ.get('MODE','A'))
        await pg.evaluate('window.ready')
        for name,t in times:
            await pg.evaluate(f'renderAt({t})')
            if fmt=='jpeg': await pg.screenshot(path=f'{outdir}/{name}.jpg', type='jpeg', quality=93)
            else: await pg.screenshot(path=f'{outdir}/{name}.png')
        await b.close()
        if errs: print('ERRORS', errs[:3])
if __name__=='__main__':
    ts=[float(x) for x in sys.argv[2:]]
    asyncio.run(run([(f'{t:06.2f}',t) for t in ts], sys.argv[1]))
