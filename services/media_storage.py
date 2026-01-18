import os
import re
import base64
from uuid import uuid4
from typing import Tuple, Optional

MEDIA_ROOT = os.getenv("MEDIA_ROOT", "media")
MEDIA_URL = os.getenv("MEDIA_URL", "/media")

DATA_URL_RE = re.compile(r"^data:(image\/[a-zA-Z0-9.+-]+);base64,")

def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def decode_base64_image(b64: str) -> Tuple[bytes, str]:
    """
    Returns (bytes, ext). Supports plain base64 or data url.
    """
    b64 = (b64 or "").strip()
    if not b64:
        raise ValueError("Empty image")

    mime = None
    m = DATA_URL_RE.match(b64)
    if m:
        mime = m.group(1)
        b64 = DATA_URL_RE.sub("", b64)

    data = base64.b64decode(b64)

    # choose extension
    if mime == "image/png":
        ext = "png"
    elif mime in ("image/jpeg", "image/jpg"):
        ext = "jpg"
    elif mime == "image/webp":
        ext = "webp"
    else:
        # fallback (you can improve detection)
        ext = "png"

    return data, ext

def save_project_image(project_id: str, b64: str) -> Tuple[str, str]:
    """
    Returns (url, key).
    key is the relative path inside MEDIA_ROOT.
    """
    data, ext = decode_base64_image(b64)
    folder = os.path.join(MEDIA_ROOT, "projects", project_id)
    _ensure_dir(folder)

    filename = f"{uuid4().hex}.{ext}"
    key = os.path.join("projects", project_id, filename).replace("\\", "/")
    full_path = os.path.join(MEDIA_ROOT, key)

    with open(full_path, "wb") as f:
        f.write(data)

    url = f"{MEDIA_URL}/{key}"
    return url, key

def save_techno_image(techno_id: str, b64: str) -> Tuple[str, str]:
    """
    Returns (url, key).
    key is the relative path inside MEDIA_ROOT.
    """
    data, ext = decode_base64_image(b64)
    folder = os.path.join(MEDIA_ROOT, "technos", techno_id)
    _ensure_dir(folder)

    filename = f"{uuid4().hex}.{ext}"
    key = os.path.join("technos", techno_id, filename).replace("\\", "/")
    full_path = os.path.join(MEDIA_ROOT, key)

    with open(full_path, "wb") as f:
        f.write(data)

    url = f"{MEDIA_URL}/{key}"
    return url, key

def save_award_image(award_id: str, b64: str) -> Tuple[str, str]:
    """
    Returns (url, key).
    key is the relative path inside MEDIA_ROOT. 
    """
    data, ext = decode_base64_image(b64)
    folder = os.path.join(MEDIA_ROOT, "awards", award_id)
    _ensure_dir(folder)

    filename = f"{uuid4().hex}.{ext}"
    key = os.path.join("awards", award_id, filename).replace("\\", "/")
    full_path = os.path.join(MEDIA_ROOT, key)

    with open(full_path, "wb") as f:
        f.write(data)

    url = f"{MEDIA_URL}/{key}"
    return url, key

def delete_media_key(key: Optional[str]) -> None:
    if not key:
        return
    full_path = os.path.join(MEDIA_ROOT, key)
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
    except Exception:
        pass
