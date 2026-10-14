import sys, os, asyncio
from playwright.async_api import async_playwright
async def run(times,out):
    os.makedirs(out,exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--allow-file-access-from-files']); pg=await b.new_page(viewport={'width':1080,'height':1920})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/exit/film2/index.html?render'); await pg.evaluate('window.ready')
        for name,t in times:
            await pg.evaluate(f'seek({t})'); await pg.screenshot(path=f'{out}/{name}.jpg',type='jpeg',quality=92)
        await b.close()
        if errs: print('ERR',errs[:3])
if __name__=='__main__':
    if sys.argv[1]=='qa': ts=[float(x) for x in sys.argv[3:]]; asyncio.run(run([(f'{t:06.2f}',t) for t in ts],sys.argv[2]))
    else:
        a,b=int(sys.argv[1]),int(sys.argv[2]); fps=90
        todo=[(f'{i:05d}',i/fps) for i in range(a,b) if not os.path.exists(f'sub2/{i:05d}.jpg')]
        if todo: asyncio.run(run(todo,'sub2'))
