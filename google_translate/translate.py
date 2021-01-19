from playwright import async_playwright
from sanic import Sanic
from sanic import response

app = Sanic(name='Translate application')

#test with: curl 'http://localhost:5000/translate?sl=nl&tl=en&translate=auto'

@app.route("/translate")
async def doTranslate(request):
    async with async_playwright() as p:
        sl = request.args.get('sl')
        tl = request.args.get('tl')
        translate = request.args.get('translate')
        browser = await p.chromium.launch() # headless=False
        context = await browser.newContext()
        page = await context.newPage()
        await page.goto('https://translate.google.com/?sl='+sl+'&tl='+tl+'&op=translate')
        textarea = await page.waitForSelector('//textarea')
        await textarea.fill(translate)
        waitforthis = await page.waitForSelector('div.Dwvecf',state='attached')
        result = await page.querySelector('span.VIiyi >> ../span/span/span')
        textresult = await result.textContent()
        await browser.close()
        return response.json({'translation':textresult})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
