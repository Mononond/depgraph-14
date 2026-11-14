"""Получение прямых зависимостей пакета Cargo (этап 2).

Используются только стандартные средства Python: адреса берутся
из открытого API crates.io, запросы выполняются через urllib.
Менеджеры пакетов и сторонние библиотеки не задействованы.
"""

import json
import urllib.request

HTTP_TIMEOUT = 20
CRATES_API_BASE = "https://crates.io/api/v1"
USER_AGENT = "depgraph-24/1.0 (student project)"


def fetch_json(url, opener=None):
    """Скачать JSON по адресу и разобрать его в словарь."""
    if opener is not None:
        return opener(url)
    request = urllib.request.Request(url,
                                     headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request,
                                timeout=HTTP_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def latest_version(info):
    """Выбрать свежую не отозванную версию из ответа API."""
    for version in info.get("versions", []):
        if not version.get("yanked"):
            return version.get("num")
    return None


def direct_dependencies(package, repo_base=None, opener=None):
    """Вернуть прямые зависимости свежей версии пакета.

    Учитываются только обычные (не dev, не сборка) и не
    опциональные зависимости: именно они нужны пакету всегда.
    """
    base = (repo_base or CRATES_API_BASE).rstrip("/")
    info = fetch_json("%s/crates/%s" % (base, package), opener)
    version = latest_version(info)
    if not version:
        return []
    url = "%s/crates/%s/%s/dependencies" % (base, package, version)
    answer = fetch_json(url, opener)
    names = []
    for dep in answer.get("dependencies", []):
        if dep.get("kind") != "normal" or dep.get("optional"):
            continue
        crate_id = dep.get("crate_id")
        if crate_id and crate_id not in names:
            names.append(crate_id)
    return names
