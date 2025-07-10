# MinecraftDownloaderLib
```markdown
# Minecraft Version Manager

Утилита для управления версиями Minecraft (Vanilla, Fabric, Forge) с возможностью поиска и скачивания.

## Установка

1. Убедитесь, что у вас установлен Python 3.7 или новее
2. Установите необходимые зависимости:
```bash
pip install requests
```

## Использование

### Инициализация менеджера
```python
from main import MinecraftVersionManager
manager = MinecraftVersionManager()
```

### Получение списка версий
```python
# Для Vanilla
vanilla_versions = manager.get_versions('vanilla')

# Для Fabric
fabric_versions = manager.get_versions('fabric')

# Для Forge
forge_versions = manager.get_versions('forge')
```

### Сохранение версий в файл
```python
manager.save_versions('vanilla')  # Сохранит в minecraft_vanila_versions.json
manager.save_versions('fabric', "custom_fabric.json")  # С кастомным именем файла
```

### Загрузка версий из файла
```python
vanilla_data = manager.load_versions('vanilla')
```

### Поиск версий
```python
# Поиск Vanilla версий
found_vanilla = manager.search_versions('vanilla', '1.19')

# Поиск Fabric версий (можно искать по game/loader/installer)
found_fabric = manager.search_versions('fabric', '0.14', search_type='loader')

# Поиск Forge версий для конкретной версии MC
found_forge = manager.search_versions('forge', '1.18.2')
```

### Скачивание версий
```python
# Скачивание Vanilla
manager.download_version('vanilla', '1.19.4')

# Скачивание Fabric с указанием версии загрузчика
manager.download_version('fabric', '1.19.4', loader_version='0.14.21')

# Скачивание Forge (рекомендуемой версии)
manager.download_version('forge', '1.18.2')

# Скачивание конкретной версии Forge
manager.download_version('forge', '1.18.2', forge_version='40.2.0')

# Указание кастомной папки для скачивания
manager.download_version('vanilla', '1.20.1', output_dir='my_custom_folder')
```

## Примеры вывода

### Вывод списка версий
```python
from main import print_versions

# Для Vanilla
vanilla_data = manager.get_versions('vanilla')
print_versions(vanilla_data['versions'])

# Для Fabric
fabric_data = manager.get_versions('fabric')
print_versions(fabric_data['game'])  # Или 'loader', или 'installer'

# Для Forge
forge_data = manager.get_versions('forge')
mc_versions = manager.search_versions('forge', '1.18')
print_versions(mc_versions)
```

## Структура проекта

```
MinecraftVersionManager/
│
├── main.py                  # Основной класс менеджера
├── Vanila_version_manager/   # Модуль для работы с Vanilla
│   └── Vanila_version_manager.py
├── Fabric_version_manager/   # Модуль для работы с Fabric
│   └── Fabric_version_manager.py
├── Forge_version_manager/    # Модуль для работы с Forge
│   └── Forge_version_manager.py
└── downloads/                # Папка для скачанных файлов (создается автоматически)
```

## Особенности

1. **Автоматическое создание папки downloads** - если папка не существует, она будет создана автоматически
2. **Кеширование данных** - можно сохранять и загружать данные версий из JSON-файлов
3. **Гибкий поиск**:
   - Для Vanilla: поиск по ID версии
   - Для Fabric: поиск по game/loader/installer версиям
   - Для Forge: поиск по версии Minecraft
4. **Умное скачивание**:
   - Для Fabric автоматически выбирается стабильная версия загрузчика, если не указана
   - Для Forge можно скачать как рекомендованную версию, так и конкретную

## Обработка ошибок

При возникновении ошибок (неверный модлоадер, версия не найдена и т.д.) будут выбрасываться исключения с понятными сообщениями.
