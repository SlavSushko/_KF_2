# CLI-приложение на Python для визуализации графа зависимостей пакетов в формате Ubuntu (apt). Прототип позволяет:
- Считывать конфигурацию из JSON-файла.
- Извлекать информацию о прямых зависимостях заданного пакета из репозитория (локального файла или URL).
- Выводить прямые зависимости пакета в консоль.

## Функции и настройки

### Функции
1.  Приложение принимает путь к JSON-файлу конфигурации через аргумент командной строки `--config`.

2. Поддерживает работу с репозиториями Ubuntu. Извлекает информацию о прямых зависимостях заданного пакета из поля `Depends`. Поддерживает два режима работы с репозиторием: через URL (`url`) или локальный файл (`file`).  Парсит зависимости.

3. Выводит список прямых зависимостей указанного пакета в консоль.

4. Проверяет наличие и корректность конфигурационного файла. Обрабатывает ошибки доступа к репозиторию (например, неверный URL, отсутствующий файл, неверный формат gzip). Проверяет наличие указанного пакета в репозитории.

### Настройки
Конфигурация задается в JSON-файле (по умолчанию `config.json`). Обязательные параметры:

- **`package_name`**: Имя анализируемого пакета.
- **`repo_url_or_path`**: URL-адрес репозитория или путь к локальному файлу `Packages`/`Packages.gz`.
- **`repo_mode`**: Режим работы с репозиторием (`url` или `file`).
- **`graph_file_name`**: Имя файла для будущего графа зависимостей.
- **`ascii_tree_mode`**: Режим вывода зависимостей в формате ASCII-дерева.
- **`filter_substring`**: Подстрока для фильтрации пакетов (строка, может быть пустой).

Пример конфигурационного файла:
```json
{
    "package_name": "curl",
    "repo_url_or_path": "http://archive.ubuntu.com/ubuntu/dists/jammy/main/binary-amd64/Packages.gz",
    "repo_mode": "url",
    "graph_file_name": "graph.png",
    "ascii_tree_mode": true,
    "filter_substring": ""
}
```

### Запуск приложения
```bash
python dependency_visualizer.py --config config.json
```
## Пример использования

1. Создать файл `config.json`:
   ```json
   {
       "package_name": "curl",
       "repo_url_or_path": "http://archive.ubuntu.com/ubuntu/dists/jammy/main/binary-amd64/Packages.gz",
       "repo_mode": "url",
       "graph_file_name": "graph.png",
       "ascii_tree_mode": true,
       "filter_substring": ""
   }
   ```
2. Запустить:
   ```bash
   python dependency_visualizer.py --config config.json
   ```
3. Ожидаемый вывод:
   ```
   Direct dependencies of 'curl':
   ca-certificates
   libc6
   libcurl4
   ```
