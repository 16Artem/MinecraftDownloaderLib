import requests
import json
import os
import re
from urllib.request import urlretrieve


def get_forge_versions_data():
    base_url = "https://files.minecraftforge.net"
    maven_metadata_url = f"{base_url}/net/minecraftforge/forge/maven-metadata.json"
    promos_url = f"{base_url}/net/minecraftforge/forge/promotions_slim.json"

    try:
        response = requests.get(maven_metadata_url)
        response.raise_for_status()
        versions_data = response.json()

        response = requests.get(promos_url)
        response.raise_for_status()
        promos_data = response.json()

        return {
            'versions': versions_data,
            'promos': promos_data['promos']
        }
    except requests.RequestException as e:
        raise Exception(f"Ошибка при получении данных Forge: {e}")


def save_versions_to_file(data, filename="minecraft_forge_versions.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Данные сохранены в {filename}")


def load_versions_from_file(filename="minecraft_forge_versions.json"):
    if os.path.exists(filename):
        with open(filename) as f:
            return json.load(f)
    return None


def _version_key(version):
    cleaned = re.sub(r'[^0-9.-]', '', version)
    parts = []
    for part in cleaned.split('.'):
        if '-' in part:
            part = part.split('-')[0]
        if part.isdigit():
            parts.append(int(part))
        else:
            parts.append(0)
    return parts


def get_minecraft_versions(data):
    mc_versions = set()
    if 'promos' in data:
        for promo_key in data['promos'].keys():
            mc_version = promo_key.split('-')[0]
            mc_versions.add(mc_version)
    return sorted(mc_versions, key=_version_key, reverse=True)


def get_forge_versions_for_mc(data, mc_version):
    forge_versions = []
    if 'promos' in data:
        for promo_key, forge_version in data['promos'].items():
            if promo_key.startswith(mc_version):
                forge_versions.append({
                    'mc_version': mc_version,
                    'forge_version': forge_version,
                    'promo_key': promo_key,
                    'is_recommended': 'recommended' in promo_key,
                    'is_latest': 'latest' in promo_key
                })
    # Сортируем версии Forge
    forge_versions.sort(key=lambda x: _version_key(x['forge_version']), reverse=True)
    return forge_versions


def download_forge_installer(mc_version, forge_version, output_dir="downloads"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_url = "https://files.minecraftforge.net"
    filename = f"forge-{mc_version}-{forge_version}-installer.jar"
    filepath = os.path.join(output_dir, filename)

    download_urls = [
        f"{base_url}/net/minecraftforge/forge/{mc_version}-{forge_version}/{filename}",
        f"https://maven.minecraftforge.net/net/minecraftforge/forge/{mc_version}-{forge_version}/{filename}"
    ]

    for url in download_urls:
        try:
            print(f"Попытка скачивания с {url}...")
            urlretrieve(url, filepath)
            print(f"Файл сохранен как {filepath}")
            return filepath
        except Exception as e:
            print(f"Ошибка при скачивании с {url}: {e}")

    raise Exception("Не удалось скачать Forge с известных зеркал")


def download_recommended_forge(mc_version, output_dir="downloads"):
    data = get_forge_versions_data()
    promo_key = f"{mc_version}-recommended"

    if promo_key not in data['promos']:
        promo_key = f"{mc_version}-latest"
        if promo_key not in data['promos']:
            raise ValueError(f"Не найдена рекомендованная или последняя версия Forge для {mc_version}")

    forge_version = data['promos'][promo_key]
    return download_forge_installer(mc_version, forge_version, output_dir)