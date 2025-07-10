import requests
import json
import os
from urllib.request import urlretrieve


def get_fabric_versions_data():
    url = "https://meta.fabricmc.net/v2/versions"
    response = requests.get(url)
    response.raise_for_status()
    return {
        'game': requests.get("https://meta.fabricmc.net/v2/versions/game").json(),
        'loader': requests.get("https://meta.fabricmc.net/v2/versions/loader").json(),
        'installer': requests.get("https://meta.fabricmc.net/v2/versions/installer").json()
    }


def save_versions_to_file(data, filename="minecraft_fabric_versions.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Данные сохранены в {filename}")


def load_versions_from_file(filename="minecraft_fabric_versions.json"):
    if os.path.exists(filename):
        with open(filename) as f:
            return json.load(f)
    return None


def search_versions(data, keyword, search_type='game'):
    results = []
    for item in data[search_type]:
        version_str = item['version'] if search_type == 'game' else item['version']
        if keyword.lower() in version_str.lower():
            results.append({
                'type': search_type,
                'version': version_str,
                'stable': item.get('stable', True)
            })
    return results


def download_fabric(version, loader_version, installer_version="latest", output_dir="downloads"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if installer_version == "latest":
        installer_data = requests.get("https://meta.fabricmc.net/v2/versions/installer").json()
        installer_version = installer_data[0]['version']

    filename = f"fabric-loader-{loader_version}-{version}.jar"
    filepath = os.path.join(output_dir, filename)
    download_url = f"https://meta.fabricmc.net/v2/versions/loader/{version}/{loader_version}/{installer_version}/server/jar"
    print(f"Скачивание Fabric {version} (loader: {loader_version}, installer: {installer_version})...")
    urlretrieve(download_url, filepath)
    print(f"Файл сохранен как {filepath}")
    return filepath


