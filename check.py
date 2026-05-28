import requests
import os
import hashlib
import time
from bs4 import BeautifulSoup

CHECK_URL   = "https://www.europesegoudstandaard.be/nl/gold-rush-1"
PLACEHOLDER = "De laatste hint komt hier te staan"
NTFY_TOPIC  = os.environ.get("NTFY_TOPIC", "goldrush-reis-2026")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0",
    "Accept-Language": "nl-BE,nl;q=0.9",
}

def fetch():
    # Timestamp parametresi ile CDN cache'ini atla
    url = f"{CHECK_URL}?_={int(time.time())}"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def get_main_h2(soup):
    for h2 in soup.find_all("h2"):
        text = h2.get_text(strip=True)
        if text and text.lower() not in ["kruimelpad", ""]:
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

def load_state():
    try:
        with open("last_state.txt") as f:
            lines = f.read().strip().splitlines()
            return lines[0] if lines else None, lines[1] if len(lines) > 1 else None
    except FileNotFoundError:
        return None, None

def save_state(page_hash, h2_text):
    with open("last_state.txt", "w") as f:
        f.write(f"{page_hash}\n{h2_text}")

# --- KONTROL ---
soup      = fetch()
page_text = soup.get_text(separator=" ", strip=True)
h2_text   = get_main_h2(soup)
page_hash = hashlib.md5(page_text.encode()).hexdigest()
prev_hash, prev_h2 = load_state()

placeholder_gone = PLACEHOLDER not in page_text
h2_changed = (
    prev_h2 is not None and
    h2_text != prev_h2 and
    PLACEHOLDER not in h2_text
)

print(f"Placeholder var: {not placeholder_gone}")
print(f"H2 simdi   : {h2_text[:80]}")
print(f"H2 onceki  : {str(prev_h2)[:80]}")
print(f"Hash simdi : {page_hash[:8]}...")
print(f"Hash onceki: {str(prev_hash)[:8]}...")

if placeholder_gone or h2_changed:
    reason = "Placeholder kaldi" if placeholder_gone else "H2 degisti"
    print(f"SON IPUCU CANLI! ({reason})")
    notify(
        "GOLD RUSH - SON IPUCU YAYINDA!",
        f"{reason}\nH2: {h2_text[:200]}\n\nHemen git: {CHECK_URL}"
    )
else:
    print("Degisiklik yok, bekleniyor.")

save_state(page_hash, h2_text)


