import os, pathlib, urllib.request

ROOT = pathlib.Path(__file__).parent
DL_DIR = ROOT / "downloads"
DL_DIR.mkdir(parents=True, exist_ok=True)

def ensure_file(url: str, local_name: str) -> str:
    local_path = DL_DIR / local_name
    if not local_path.exists():
        urllib.request.urlretrieve(url, local_path)
    return str(local_path)

def get_env_flag(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1","true","yes","y"}

def get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default)
