import base64
from pathlib import Path
'''
This module contains utility functions used across the app, such as:
- get_base64_image: Reads an image file and returns its base64-encoded string representation,
 which is useful for embedding images directly in CSS or HTML.
'''
def get_base64_image(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
