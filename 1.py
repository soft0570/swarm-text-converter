import re

def extract_event(text):
    # 1) いちばん安定する取り方:
    #    " から 「この https://」の直前までを取る
    match = re.search(r'"([\s\S]*?)この\s+https?://', text)
    if not match:
        return ""

    event_block = match.group(1)

    # 改行を整理して、空行を除外
    lines = [
        line.strip()
        for line in event_block.splitlines()
        if line.strip()
    ]

    # 2行まで使う
    return " ".join(lines[:2]).strip()


def extract_location_text(text):
    # 場所行はだいたい単独行で
    # (会場 住所, 区, 都道府県, 郵便番号, JP)
    # の形なので、「行頭の ( 〜 行末の )」を丸ごと取る
    match = re.search(r'^\((.+)\)\s*$', text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_url(text):
    # まずは share/checkin を優先
    match = re.search(
        r'https?://(?:app\.foursquare\.com|(?:www\.)?swarmapp\.com)/share/checkin/\S+',
        text
    )
    if not match:
        return ""

    url = match.group(0)

    # app.foursquare.com → swarmapp.com
    # lang=ja → lang=en
    url = url.replace("app.foursquare.com", "swarmapp.com")
    url = url.replace("www.swarmapp.com", "swarmapp.com")
    url = url.replace("lang=ja", "lang=en")

    return url


def extract_venue(location_text):
    if not location_text:
        return ""

    # 最初のカンマより前だけ見る
    before_first_comma = location_text.split(",")[0].strip()

    # 住所っぽい部分の前を会場名とみなす
    # 例:
    #   六行会ホール 北品川2-32-3
    #   明治神宮野球場 霞ヶ丘町3-1
    #   AKB48劇場 外神田4-3-3 (@ ドン・キホーテ 秋葉原店 8F)
    match = re.match(r'^(.*?)(?:\s+[^\s]*\d.*)?$', before_first_comma)
    if match:
        return match.group(1).strip()

    return before_first_comma


def convert(text):
    event = extract_event(text)
    location_text = extract_location_text(text)
    url = extract_url(text)

    venue = extract_venue(location_text)

    parts = [p.strip() for p in location_text.split(",")]
    ward = parts[1] if len(parts) > 1 else ""
    prefecture = parts[2] if len(parts) > 2 else ""

    if event:
        return f"{event} (@ {venue} in {ward}, {prefecture}) {url}".strip()
    else:
        return f"I'm at {venue} in {ward}, {prefecture} {url}".strip()