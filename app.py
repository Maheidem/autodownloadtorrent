import os
import time
import requests
import logging
from xml.etree import ElementTree

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

RSS_URL = "https://rss.torrentleech.org/a847b369927408ec7519"
OUTPUT_FOLDER = "downloaded_torrents/"
PING_INTERVAL = 600  # 10 minutes in seconds

def download_torrents_from_rss(rss_url):
    try:
        response = requests.get(rss_url)
        response.raise_for_status()

        tree = ElementTree.fromstring(response.content)
        items = tree.findall(".//item")

        for item in items:
            category = item.find("category").text
            title = item.find("title").text
            link = item.find("link").text
            
            if category == "BoxSets" and ("720p" in title or "1080p" in title):
                filename = link.split("/")[-1]
                filepath = os.path.join(OUTPUT_FOLDER, filename)

                # Check if the file already exists
                if not os.path.exists(filepath):
                    torrent_response = requests.get(link)
                    torrent_response.raise_for_status()

                    with open(filepath, 'wb') as file:
                        file.write(torrent_response.content)
                    logger.info(f"Downloaded: {filename}")
                else:
                    logger.warning(f"File {filename} already exists. Skipping download.")

    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    while True:
        download_torrents_from_rss(RSS_URL)
        time.sleep(PING_INTERVAL)