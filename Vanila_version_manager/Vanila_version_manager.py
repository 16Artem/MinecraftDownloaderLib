import requests
import json
import os
from urllib.request import urlretrieve


def get_versions_data():
    url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def save_versions_to_file(data, filename="minecraft_vanila_versions.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Данные сохранены в {filename}")


def load_versions_from_file(filename="minecraft_vanila_versions.json"):
    if os.path.exists(filename):
        with open(filename) as f:
            return json.load(f)
    return None


def search_versions(versions, keyword):
    results = []
    for version in versions['versions']:
        if keyword.lower() in version['id'].lower():
            results.append({
                'id': version['id'],
                'type': version['type'],
                'url': version['url']
            })
    return results


def download_version(version_url, output_dir="downloads"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    version_data = requests.get(version_url).json()
    client_url = version_data['downloads']['client']['url']
    filename = f"minecraft_vanila_-{version_data['id']}-client.jar"
    filepath = os.path.join(output_dir, filename)
    print(f"Скачивание {filename}...")
    urlretrieve(client_url, filepath)
    print(f"Файл сохранен как {filepath}")
    return filepath


