import os
from Vanila_version_manager.Vanila_version_manager import (
    get_versions_data as get_vanilla_versions,
    save_versions_to_file as save_vanilla_versions,
    load_versions_from_file as load_vanilla_versions,
    search_versions as search_vanilla_versions,
    download_version as download_vanilla
)
from Fabric_version_manager.Fabric_version_manager import (
    get_fabric_versions_data as get_fabric_versions,
    save_versions_to_file as save_fabric_versions,
    load_versions_from_file as load_fabric_versions,
    search_versions as search_fabric_versions,
    download_fabric
)
from Forge_version_manager.Forge_version_manager import (
    get_forge_versions_data,
    save_versions_to_file as save_forge_versions,
    load_versions_from_file as load_forge_versions,
    get_minecraft_versions,
    get_forge_versions_for_mc,
    download_forge_installer,
    download_recommended_forge
)


class MinecraftVersionManager:
    def __init__(self):
        self.default_output_dir = "downloads"

    def get_versions(self, modloader: str):
        if modloader == 'vanilla':
            return get_vanilla_versions()
        elif modloader == 'fabric':
            return get_fabric_versions()
        elif modloader == 'forge':
            return get_forge_versions_data()
        else:
            raise ValueError("Неизвестный модлоадер. Допустимые значения: 'vanilla', 'fabric', 'forge'")

    def save_versions(self, modloader: str, filename: str = None):
        data = self.get_versions(modloader)
        if modloader == 'vanilla':
            filename = filename or "minecraft_vanila_versions.json"
            save_vanilla_versions(data, filename)
        elif modloader == 'fabric':
            filename = filename or "minecraft_fabric_versions.json"
            save_fabric_versions(data, filename)
        elif modloader == 'forge':
            filename = filename or "minecraft_forge_versions.json"
            save_forge_versions(data, filename)
        else:
            raise ValueError("Неизвестный модлоадер")

    def load_versions(self, modloader: str, filename: str = None):
        if modloader == 'vanilla':
            filename = filename or "minecraft_vanila_versions.json"
            return load_vanilla_versions(filename)
        elif modloader == 'fabric':
            filename = filename or "minecraft_fabric_versions.json"
            return load_fabric_versions(filename)
        elif modloader == 'forge':
            filename = filename or "minecraft_forge_versions.json"
            return load_forge_versions(filename)
        else:
            raise ValueError("Неизвестный модлоадер")

    def search_versions(self, modloader: str, keyword: str, **kwargs):
        if modloader == 'vanilla':
            data = self.load_versions(modloader) or self.get_versions(modloader)
            return search_vanilla_versions(data, keyword)
        elif modloader == 'fabric':
            data = self.load_versions(modloader) or self.get_versions(modloader)
            search_type = kwargs.get('search_type', 'game')
            return search_fabric_versions(data, keyword, search_type)
        elif modloader == 'forge':
            data = self.load_versions(modloader) or self.get_versions(modloader)
            mc_versions = get_minecraft_versions(data)
            if keyword.lower() in [v.lower() for v in mc_versions]:
                return get_forge_versions_for_mc(data, keyword)
            return []
        else:
            raise ValueError("Неизвестный модлоадер")

    def download_version(self, modloader: str, version: str, **kwargs):
        output_dir = kwargs.get('output_dir', self.default_output_dir)

        if modloader == 'vanilla':
            versions = self.search_versions(modloader, version)
            if not versions:
                raise ValueError(f"Версия {version} не найдена")
            return download_vanilla(versions[0]['url'], output_dir)

        elif modloader == 'fabric':
            loader_version = kwargs.get('loader_version')
            if not loader_version:
                fabric_data = self.get_versions('fabric')
                for loader in fabric_data['loader']:
                    if loader.get('stable', True):
                        loader_version = loader['version']
                        break
                if not loader_version:
                    raise ValueError("Не удалось найти стабильную версию Fabric Loader")

            installer_version = kwargs.get('installer_version', 'latest')
            return download_fabric(version, loader_version, installer_version, output_dir)

        elif modloader == 'forge':
            forge_version = kwargs.get('forge_version')
            if forge_version:
                return download_forge_installer(version, forge_version, output_dir)
            else:
                return download_recommended_forge(version, output_dir)

        else:
            raise ValueError("Неизвестный модлоадер")


def print_versions(versions):
    if not versions:
        print("Версии не найдены")
        return

    if isinstance(versions[0], dict):
        # Для Fabric и Forge
        for i, ver in enumerate(versions, 1):
            print(f"{i}. {ver.get('version', ver.get('mc_version', 'N/A'))}")
            for k, v in ver.items():
                if k not in ['version', 'mc_version']:
                    print(f"   {k}: {v}")
            print()
    else:
        for i, ver in enumerate(versions, 1):
            print(f"{i}. {ver}")
