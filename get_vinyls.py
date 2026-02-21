import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

DISCOGS_TOKEN = os.getenv("DISCOGS_TOKEN")
DISCOGS_USERNAME = os.getenv("DISCOGS_USERNAME")
HEADERS = {
    "Authorization": f"Discogs token={DISCOGS_TOKEN}",
    "User-Agent": "VinylCollectionSite/1.0",
}

COVERS_DIR = Path("assets/vinyls-cover")
DATA_FILE = Path("data/vinyls.json")


def fetch_collection():
    releases = []
    url = f"https://api.discogs.com/users/{DISCOGS_USERNAME}/collection/folders/0/releases"
    params = {"per_page": 100, "page": 1}

    while url:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        releases.extend(data["releases"])
        url = data["pagination"]["urls"].get("next")
        params = {}  # next URL already includes pagination params

    return releases


def download_cover(image_url, filename):
    dest = COVERS_DIR / filename
    if dest.exists():
        return
    response = requests.get(image_url, headers=HEADERS)
    response.raise_for_status()
    dest.write_bytes(response.content)


def main():
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    print("Fetching collection from Discogs...")
    releases = fetch_collection()
    print(f"Found {len(releases)} records.")

    vinyls = []
    for release in releases:
        info = release["basic_information"]

        artist = info["artists"][0]["name"] if info["artists"] else "Unknown"
        label = info["labels"][0]["name"] if info["labels"] else "Unknown"
        year = info.get("year", "")
        title = info["title"]
        cover_url = info.get("cover_image", "")

        image_filename = None
        if cover_url:
            image_filename = f"{release['id']}.jpg"
            try:
                download_cover(cover_url, image_filename)
            except Exception as e:
                print(f"  Could not download cover for {title}: {e}")
                image_filename = None

        vinyls.append({
            "title": title,
            "artist": artist,
            "label": label,
            "year": year,
            "image": f"vinyls-cover/{image_filename}" if image_filename else None,
        })
        print(f"  {artist} — {title}")

    DATA_FILE.write_text(json.dumps(vinyls, indent=2, ensure_ascii=False))
    print(f"\nSaved {len(vinyls)} records to {DATA_FILE}")


if __name__ == "__main__":
    main()
