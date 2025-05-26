import asyncio
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

app = FastAPI()

async def scrape_zillow(url: str):
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url, timeout=15000)  # 15 sec timeout
            await page.wait_for_load_state('networkidle', timeout=15000)

            # Example: Extract property title
            title = await page.locator('h1[data-testid="home-details-summary-headline"]').text_content()

            # Example: Extract price
            price = await page.locator('span[data-testid="price"]').text_content()

            # Example: Extract address
            address = await page.locator('h1[data-testid="home-details-summary-headline"]').text_content()

            # Close browser
            await browser.close()

            return {
                "title": title.strip() if title else None,
                "price": price.strip() if price else None,
                "address": address.strip() if address else None,
                "url": url
            }
        except PlaywrightTimeoutError:
            raise HTTPException(status_code=504, detail="Timeout while loading Zillow page")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error scraping Zillow: {str(e)}")


@app.get("/scrape")
async def scrape(url: str = Query(..., description="Zillow property URL to scrape")):
    # Basic validation for URL domain
    if "zillow.com" not in url:
        raise HTTPException(status_code=400, detail="Only Zillow URLs are supported.")
    data = await scrape_zillow(url)
    return JSONResponse(content=data)