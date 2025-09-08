import re
import requests
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime

BASE_URL = "https://www.redchip.com"
START_URL = "https://www.redchip.com/stocks/?market_cap_range=Under%2B%252450M"
OUTPUT_FILE = "redchip_disclosures_under_50M_with_dates.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

# Regex to capture Month Day followed by 'to' or 'through'
DATE_REGEX = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})\s+(?:to|through)\b",
    re.IGNORECASE
)

def get_stock_links(page_url):
    """Extract all stock detail page links from the stock table rows."""
    response = requests.get(page_url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    stock_links = []
    rows = soup.find_all("tr")

    for i, tr in enumerate(rows, start=1):
        link = tr.find("a", href=True)
        if link and "/stocks/" in link['href']:
            stock_links.append(link['href'])
        else:
            print(f"DEBUG: Skipping row {i}, no stock link")

    print(f"DEBUG: Found {len(stock_links)} stock links on {page_url}")
    return list(set(stock_links))

def extract_all_campaign_dates(disclosure_url):
    """Extract all campaign start dates from the disclosure section."""
    response = requests.get(disclosure_url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    dates = []
    paragraphs = soup.find_all("p")
    for p in paragraphs:
        text = p.get_text(separator=" ").strip()
        for match in DATE_REGEX.finditer(text):
            month, day = match.groups()
            # Attempt to find the year in the paragraph; fallback to current year if not found
            year_match = re.search(r"\b(20\d{2})\b", text)
            year = int(year_match.group(1)) if year_match else datetime.now().year
            try:
                date_obj = datetime.strptime(f"{month} {day} {year}", "%B %d %Y")
                dates.append(date_obj.strftime("%Y-%m-%d"))
            except ValueError:
                continue
    return dates

def crawl_all_stocks(start_url, max_pages=3):
    all_stock_links = set()

    for page_num in range(1, max_pages + 1):
        url = (
            f"{BASE_URL}/stocks/{page_num}?market_cap_range=Under%2B%252450M#tableSection"
            if page_num > 1
            else start_url
        )
        print(f"Fetching stock list page {page_num} ...")
        links = get_stock_links(url)
        all_stock_links.update(links)
        time.sleep(1)

    print(f"Total unique stocks found: {len(all_stock_links)}")

    ticker_configs = []
    for rel_link in sorted(all_stock_links):
        stock_url = rel_link if rel_link.startswith("http") else BASE_URL + rel_link
        ticker = stock_url.split("/")[-1]
        try:
            campaign_dates = extract_all_campaign_dates(stock_url)
            if campaign_dates:
                for date in campaign_dates:
                    ticker_configs.append((ticker, date))
                    print(f"{ticker}: Campaign Date {date}")
            else:
                print(f"{ticker}: No campaign dates found")
        except Exception as e:
            print(f"{ticker}: Error extracting campaign dates: {e}")
        time.sleep(1)

    # Save to CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "Campaign_Date"])
        writer.writerows(ticker_configs)

    print(f"\nResults saved to {OUTPUT_FILE}")
    return ticker_configs

if __name__ == "__main__":
    ticker_configs = crawl_all_stocks(START_URL, max_pages=60)
