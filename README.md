# Пример написания плагинов для TestY

В данном примере написан плагин для импорта тест-сьютов и тест-кейсов из .xlsx файла формата:

|   |        A         |        B         |           C           | 
|:-:|:----------------:|:----------------:|:---------------------:|
| 1 | Имя Тест-Сьюта 1 | Имя Тест-Кейса 1 | Сценарий Тест-Кейса 1 |
| 2 |                  | Имя Тест-Кейса 2 | Сценарий Тест-Кейса 2 | 
| 3 |                  | Имя Тест-Кейса 3 | Сценарий Тест-Кейса 3 |
| 4 | Имя Тест-Сьюта 2 | Имя Тест-Кейса 4 | Сценарий Тест-Кейса 4 |
| 5 |                  | Имя Тест-Кейса 5 | Сценарий Тест-Кейса 5 |

В результате создастся два тест-сьюта, первый с тест-кейсами 1-3, второй c тест-кейсами 4-5

# Содеримое плагина

## Файл setup.py

setup.py — это основной скрипт в Python, который используется для распространения и установки модулей. Этот файл позволяет корректно установить Python пакет на другой компьютер или в другую среду разработки.

В функцию setup передаются следующие параметры:

1. name: имя плагина
2. version: версия плагина
3. description: описание плагина
4. packages: список путей ко всем вашим файлам python (используется функция find_packages)
5. install_requires: список имен и версий пакетов (точно как в файле requirements.txt)
6. include_package_data: указывает, включать ли данные пакета при установке плагина.
7. zip_safe: указывает, может ли плагин быть установлен и запущен в виде архива ZIP.

## Файл MANIFEST.in

Если в setup.py параметр include_package_data = True, то в данном файле следует указать какие файлы следует включить в сборку

## Директория plugin_example

### Директория templates

В данной директории находятся .html файлы, которые используются для серверного рендеринга (используя django templates)

Статические файлы (css, js, etc) следует помещать в директорию static

### Файл \_\_init\_\_.py

В данном файле находится код, который нужно выполнить при импортировании модулей из пакета, в нем следует импортировать 
класс, который задает конфигурацию плагина:

```python
from plugins import TestyPluginConfig
```

И создать собственный дочерний класс:

```python
class ExamplePluginConfig(TestyPluginConfig):
    name = 'plugin_example'
    verbose_name = 'Plugin example'
    description = 'It is very simple plugin example'
    version = '0.1'
    plugin_base_url = 'plugin-example'
    index_reverse_name = 'upload-file'


config = ExamplePluginConfig
```

Основные моменты при создании класса конфигурации:

1. name: имя плагина, **должно совпадать с названием директории**
2. plugin_base_url: задает эндпоинт в TestY, по которому будет доступен плагин (_https://testy.host/plugins/{plugin_base_url}/_)
3. index_reverse_name: reverse для главной страницы

## Директория xlsx_parser_lib

Здесь находятся основные файлы для обработки данных. 

**ВАЖНО:** используйте относительный импорт для модулей из плагина

## Файл views.py

Содержит view классы в которых содержатся методы плагина

**ВАЖНО:** используйте относительный импорт для модулей из плагина

**ВАЖНО:** Для функции reverse следует использовать шаблон:

```python
reverse("plugins:{plugin_name}:{path_name}")
```

Пример:

```python
# urls.py
urlpatterns = [path('', views.ProjectListView.as_view(), name='index')]
```
```python
# views.py
class UploadFileApiView(CreateAPIView):
    serializer_class = Serializer

    def create(self, request, *args, **kwargs):
        ...
        return redirect(reverse('plugins:plugin_example:index'))
```

## Файл urls

В данном файле регистрируются эндпоинты для методов плагина

Общая часть у всех эндпоинтов _/plugins/{plugin_base_url}/_

**ВАЖНО:** используйте относительный импорт для модулей из плагина

# Установка плагина

1. В файле testy/testy/settings/common.py добавьте имя вашего плагина в список:
```commandline
TESTY_PLUGINS = [
    ...
    'plugin_example',
    ...
]
```
2. В файл с зависимостями добавьте путь до вашего плагина (локально или в гите) для этого:
* Перейдите в директорию testy
* Добавьте путь в файл _requirements/requirements.in_
* Выполните команду
```commandline
pip-compile requirements/requirements.in
```
3. Запустите приложение в контейнере используя docker-compose 
