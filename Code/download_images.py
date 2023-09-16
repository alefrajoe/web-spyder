import os
from io import BytesIO
from pathlib import Path

import requests
import typer
import yaml
from bs4 import BeautifulSoup
from PIL import Image


def download_all_images_from_web_page(
    url: str, config: str, output_directory: str = "WebImages"
):
    # Create the output directory
    os.makedirs(output_directory, exist_ok=True)

    # Open config file
    with open(config, "r") as f:
        config_images = yaml.safe_load(f)

    # Read the web page
    html_doc = requests.get(url=url)

    # Make a soup with bs4
    soup = BeautifulSoup(html_doc.text, "html.parser")

    # Looping over all images
    images_url = [
        "http:" + image["src"]
        for image in soup.find_all("img", {"src": True})
        if image["src"].startswith("//")
    ]

    # Filter all images for the extension
    images_url = list(
        filter(
            # Filter files according to their extension
            lambda x: str(os.path.splitext(x)[-1]).lower()
            in config_images["extension"],
            images_url,
        )
    )

    # Download all images
    for image_url in images_url:
        # First download the raw content of the image
        image_raw = requests.get(image_url)
        # Covert bytes to pixels
        image = Image.open(BytesIO(image_raw.content))
        # Take width and height
        width, height = image.size
        # If image dimensions respect constraints, download the image
        if (
            config_images["size"]["min_width"]
            <= width
            < config_images["size"]["max_width"]
        ) and (
            config_images["size"]["min_height"]
            <= height
            < config_images["size"]["max_height"]
        ):
            os.system(f"wget -P {output_directory} {image_url}")


if __name__ == "__main__":
    typer.run(download_all_images_from_web_page)
