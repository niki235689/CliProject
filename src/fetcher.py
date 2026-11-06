"""Модуль для получения данных о зависимостях пакетов."""
import json
import urllib.request


def get_latest_version(pkg: str, base_url: str) -> str:
    """Получает номер актуальной версии пакета из crates.io."""
    url = f"{base_url}/api/v1/crates/{pkg}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("crate", {}).get("max_version", "")
    except Exception:
        return ""


def fetch_real(pkg: str, ver: str, base_url: str) -> list:
    """Получает прямые зависимости пакета через API crates.io."""
    target_ver = ver
    if not target_ver or target_ver == "*":
        target_ver = get_latest_version(pkg, base_url)

    if not target_ver:
        return []

    url = f"{base_url}/api/v1/crates/{pkg}/{target_ver}/dependencies"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode("utf-8"))
            deps = data.get("dependencies", [])
            # Оставляем только основные зависимости (исключаем dev-зависимости)
            res = [
                d["crate_id"] for d in deps
                if d.get("kind") == "normal"
            ]
            return res if res else [d["crate_id"] for d in deps[:3]]
    except Exception:
        return []


def fetch_test(pkg: str, filepath: str) -> list:
    """Читает зависимости из тестового JSON-файла."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get(pkg, [])
    except Exception:
        return []