import os
from pathlib import Path

import requests
import typer
import yaml
from bs4 import BeautifulSoup


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
    images_url = [image["src"] for image in soup.find_all("img")]

    # Filter all images for the extension
    images_url = list(
        filter(
            lambda x: str(os.path.splitext(x)[-1]).lower()
            in config_images["extension"],
            images_url,
        )
    )

    # Download all images
    for image_url in images_url:
        os.system(f"wget -P {output_directory} http:{image_url}")


if __name__ == "__main__":
    typer.run(download_all_images_from_web_page)
