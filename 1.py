import re

def convert(text):
    event_match = re.search(r'"([^"]+)"', text, re.DOTALL)
    location_match = re.search(r'\(([^)]+)\)', text)
    url_match = re.search(r'https?://\S+', text)

    location_text = location_match.group(1) if location_match else ""
    url = url_match.group(0) if url_match else ""

    # URL変換
    url = url.replace("app.foursquare.com", "swarmapp.com").replace("lang=ja", "lang=en")

    venue = location_text.split()[0]
    parts = location_text.split(',')
    ward = parts[1].strip() if len(parts) > 1 else ""
    prefecture = parts[2].strip() if len(parts) > 2 else ""

    if event_match:
        event = event_match.group(1).replace("\n", " ").strip()
        return f"{event} (@ {venue} in {ward}, {prefecture}) {url}"
    else:
        return f"I'm at {venue} in {ward}, {prefecture} {url}"