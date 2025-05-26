from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from playwright.async_api import async_playwright
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

async def scrape_zillow(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        # Wait for content to load
        await page.wait_for_timeout(5000)

        # Extract some example data
        try:
            price = await page.locator('span[data-test="home-details-summary-headline"]').text_content()
        except Exception:
            price = None
        try:
            beds = await page.locator('span[data-test="beds"]').text_content()
        except Exception:
            beds = None
        try:
            baths = await page.locator('span[data-test="baths"]').text_content()
        except Exception:
            baths = None
        try:
            sqft = await page.locator('span[data-test="sqft"]').text_content()
        except Exception:
            sqft = None
        try:
            address = await page.locator('h1[data-test="home-details-summary-headline"]').text_content()
        except Exception:
            address = None

        await browser.close()

        return {
            "address": address,
            "price": price,
            "beds": beds,
            "baths": baths,
            "sqft": sqft,
            "platform": "Zillow",
            "source_url": url,
        }

@app.get("/scrape")
async def scrape(url: str):
    data = await scrape_zillow(url)
    return data