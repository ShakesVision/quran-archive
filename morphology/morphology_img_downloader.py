import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://corpus.quran.com/wordimage?id={}"
OUTPUT_DIR = "images"
START_ID = 1
END_ID = 77429
MAX_WORKERS = 20

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Use a session for connection pooling (important for speed)
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=MAX_WORKERS,
                                         pool_maxsize=MAX_WORKERS)
session.mount("http://", adapter)
session.mount("https://", adapter)


def download_image(image_id):
    url = BASE_URL.format(image_id)
    try:
        response = session.get(url, timeout=10)
        if response.status_code == 200 and response.content:
            file_path = os.path.join(OUTPUT_DIR, f"{image_id}.png")
            with open(file_path, "wb") as f:
                f.write(response.content)
            return f"✓ {image_id}"
        return f"Skipped {image_id}"
    except Exception as e:
        return f"Error {image_id}: {e}"


def main():
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(download_image, i)
                   for i in range(START_ID, END_ID + 1)]

        for future in as_completed(futures):
            print(future.result())


if __name__ == "__main__":
    main()