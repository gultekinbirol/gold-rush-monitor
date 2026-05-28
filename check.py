import requests
import os
import hashlib
import sys
from bs4 import BeautifulSoup

CHECK_URL   = "https://www.europesegoudstandaard.be/nl/gold-rush-1"
PLACEHOLDER = "De laatste hint komt hier te staan"
NTFY_TOPIC  = os.environ.get("NTFY_TOPIC", "goldrush-reis-2026")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Accept-Language": "nl-BE,nl;q=0.9",
}

def fetch():
    resp = requests.get(CHECK_URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def get_hint_h2(soup):
    for h2 in soup.find_all("h2"):
        text = h2.get_text(strip=True)
        if text and text != "Kruimelpad":
            return text
    return ""

def notify(title, message):
    resp = requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=message.encode("utf-8"),
        headers={
            "Title": title,
            "Priority": "urgent",
            "Tags": "rotating_light,trophy",
            "Click": CHECK_URL,
        },
        timeout=10,
    )
    print(f"ntfy status: {resp.status_code}")

def load_hash():
    try:
        with open("last_hash.txt") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_hash(h):
    with open("last_hash.txt", "w") as f:
        f.write(h)

# Her calistirmada test bildirimi gonder
notify("Gold Rush Monitor TEST", f"GitHub Actions calisiyor! URL: {CHECK_URL}")

soup = fetch()
h2_text = get_hint_h2(soup)
page_text = soup.get_text(separator=" ", strip=True)
current_hash = hashlib.md5(page_text.encode()).hexdigest()
previous_hash = load_hash()

hint_live = PLACEHOLDER not in page_text

print(f"Placeholder aktif: {not hint_live}")
print(f"H2 icerigi: {h2_text[:80]}")
print(f"Hash: {current_hash[:8]}... | Onceki: {str(previous_hash)[:8]}...")

if hint_live:
    print("SON IPUCU CANLI!")
    notify(
        "GOLD RUSH - SON IPUCU YAYINDA!",
        f"Son ipucu: {h2_text[:200]}\n\nHemen git: {CHECK_URL}"
    )

save_hash(current_hash)
