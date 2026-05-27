import requests
import os
import hashlib
from bs4 import BeautifulSoup

CHECK_URL   = "https://www.europesegoudstandaard.be/nl/gold-rush-1"
PLACEHOLDER = "De laatste hint komt hier te staan"
NTFY_TOPIC  = os.environ.get("NTFY_TOPIC", "goldrush-reis-2026")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Accept-Language": "nl-BE,nl;q=0.9",
}

def fetch():
    resp = requests.get(CHECK_URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def notify(message):
    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=message.encode("utf-8"),
        headers={
            "Title": "GOLD RUSH - SON IPUCU YAYINDA!",
            "Priority": "urgent",
            "Tags": "rotating_light,trophy",
            "Click": CHECK_URL,
        },
        timeout=10,
    )

def load_hash():
    try:
        with open("last_hash.txt") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_hash(h):
    with open("last_hash.txt", "w") as f:
        f.write(h)

text = fetch()
current_hash = hashlib.md5(text.encode()).hexdigest()
previous_hash = load_hash()

hint_live = PLACEHOLDER not in text

print(f"Placeholder aktif: {not hint_live}")
print(f"Hash: {current_hash[:8]}... | Onceki: {str(previous_hash)[:8]}...")

if hint_live:
    print("SON IPUCU CANLI! Bildirim gonderiliyor...")
    notify(f"Son ipucu yayinlandi! Hemen git: {CHECK_URL}")
elif previous_hash and current_hash != previous_hash:
    print("Sayfa degisti ama placeholder hala var.")

save_hash(current_hash)
