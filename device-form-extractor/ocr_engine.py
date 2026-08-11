import base64
import json
import re
import requests

from config import OLLAMA_HOST, OLLAMA_MODEL
from schema import EXTRACTION_PROMPT


def _image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _clean_json_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```json", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^```", "", text).strip()
    text = re.sub(r"```$", "", text).strip()

    # If model added extra text before/after the JSON object, extract just the {...}
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        text = match.group(0)

    return text


def extract_from_image(image_path: str) -> dict:
    """
    Sends image to local Ollama vision model, returns parsed dict.
    Raises ValueError if request fails or output isn't valid JSON.
    """
    img_b64 = _image_to_base64(image_path)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": EXTRACTION_PROMPT,
        "images": [img_b64],
        "stream": False,
        "options": {
            "num_ctx": 16384
        }
    }

    resp = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=300)

    if resp.status_code != 200:
        raise ValueError(f"Ollama error {resp.status_code}: {resp.text}")

    raw_response = resp.json().get("response", "")
    cleaned = _clean_json_text(raw_response)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError(f"Model did not return valid JSON:\n{raw_response}")

    return data