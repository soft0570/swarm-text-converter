import re
import requests
from bs4 import BeautifulSoup

def extract_details_from_url(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        og_title = soup.find('meta', property='og:title')
        
        if og_title and og_title.get('content'):
            title_text = og_title['content']
            # "I'm at 明治神宮野球場 in 新宿区, 東京都" 形式のパース
            match = re.search(r"I'm at ([^in]+)\s+in\s+([^,]+),\s*(.+)", title_text)
            if match:
                return match.group(1).strip(), match.group(2).strip(), match.group(3).strip()
    except Exception as e:
        print(f"Fetch Error: {e}")
    return "", "", ""

def convert(text):
    event = extract_event(text)
    location_text = extract_location_text(text)
    url = extract_url(text)

    # 従来のテキストパース処理
    if location_text:
        venue = extract_venue(location_text)
        parts = [p.strip() for p in location_text.split(",")]
        ward = parts[1] if len(parts) > 1 else ""
        prefecture = parts[2] if len(parts) > 2 else ""

        if event:
            return f"{event} (@ {venue} in {ward}, {prefecture}) {url}".strip()
        else:
            return f"I'm at {venue} in {ward}, {prefecture} {url}".strip()
            
    # URLのみの場合のフォールバック処理
    elif url:
        venue, ward, prefecture = extract_details_from_url(url)
        if venue:
            return f"I'm at {venue} in {ward}, {prefecture} {url}".strip()

    return "解析できませんでした"