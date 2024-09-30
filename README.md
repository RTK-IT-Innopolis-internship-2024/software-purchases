![Windows Build](https://github.com/RTK-IT-Innopolis-internship-2024/software-purchases/actions/workflows/windows-build.yml/badge.svg?branch=main)
![Ubuntu Build](https://github.com/RTK-IT-Innopolis-internship-2024/software-purchases/actions/workflows/ubuntu-build.yml/badge.svg?branch=main)
![macOS Build](https://github.com/RTK-IT-Innopolis-internship-2024/software-purchases/actions/workflows/macos-build.yml/badge.svg?branch=main)
![GitHub Releases](https://img.shields.io/github/v/release/RTK-IT-Innopolis-internship-2024/software-purchases)
![Release Date](https://img.shields.io/github/release-date/RTK-IT-Innopolis-internship-2024/software-purchases)
![GitHub Last Commit](https://img.shields.io/github/last-commit/RTK-IT-Innopolis-internship-2024/software-purchases)


# 1. Инструкция для пользователя:

## Как выглядит приложение:

![App main window](https://github.com/RTK-IT-Innopolis-internship-2024/software-purchases/blob/main/docs/app-main-window.png)

## Релиз приложения состоит из архива со следующим содержимым:

├── 📁 Apps-Purchases-<your_platform_name>-latest/  
│ ├── 📁 orders/  
│ │ ├── 📁 final_reports/  
│ │ │ └── 📄 Отчет о заявках за период - 2023 кв. 3 - 2024 кв. 3.xlsx  
│ │ ├── 📁 main_template/  
│ │ │ └── 📄 Шаблон заявки с справочниками.xlsx  
│ │ ├── 📁 order_templates/  
│ │ │ ├── 📄 10.09.2024.xlsx  
│ │ │ └── 📄 файл 2.xlsx  
│ └── 🖥️ Apps-Purchases-<your_platform_name>-latest.exe

* В папке `final_reports` находится пример сгенерированного отчета и эта папка является папкой по умолчанию для генерации отчетов.
* В папке `main_template` находится основной шаблон с актуальными справочниками, предполагается что этот отчет отправляется сотрудникам для формирования
  заявок на ПО.
* В папке `order_templates` находятся примеры полученных заявок на основе основного шаблона.
* Файл exe - основной файл для запуска приложения.

## Как работать с приложением:

1. Скачиваем актуальный релиз под нужную платформу по ссылке с правой части экрана.
   ![Release image](https://github.com/RTK-IT-Innopolis-internship-2024/software-purchases/blob/main/docs/release.png)
2. Распаковываем архив в папку.
3. Актуализируем основной шаблон в папке `main_template`.
4. Отправляем этот шаблон сотрудникам для формирования заявок на ПО.
5. Проверяем заявки, чтобы они соответствовали общему формату шаблона и все значения в заявках, Наименование ПО соответствовали значениям из
   соответствующих справочников (Пример: класс ПО в справочнике Наименование ПО должен полностью соответствовать значению из справочника классов ПО
   минкомсвязи, либо значению из справочника с другими классами).
6. Загружаем полученные файлы заявок-шаблонов в папку `order_templates`.
7. Открываем приложение нажатием на exe файл, либо обновляем заявки в приложении по нажатию на кнопку обновления.
8. Проверяем, что все файлы загрузились, если это не так, то нужно перепроверить загруженные файлы.
9. Фильтруем заявки по датам, выбираем нужные заявки в левой части.
10. Нажатием на кнопку выгрузки в правой нижней части, формируем итоговый отчет за указанный период.

## Дополнительно:

Приложение так же позволяет просмотреть актуальные справочники.

# 2. Instructions for developers:

In this project, Python 3.11 was used.

## 2.1. Main instruction with uv tool (recommended)

In this project UV Project Manager was used, check its [documentation](https://docs.astral.sh/uv) and [source code](https://github.com/astral-sh/uv).

### Install uv

```
# On macOS and Linux.
$ curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows.
$ powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# With pip.
$ pip install uv
```

See the [installation documentation](https://docs.astral.sh/uv/getting-started/installation/) for details and alternative installation methods.

### Install and activate venv by [sync command](https://docs.astral.sh/uv/reference/cli/#uv-sync)

Install venv and sync dependencies

```shell
uv sync
```

Activate venv

```
# На Windows:
$ .venv\Scripts\activate

# На macOS и Linux:
$ source .venv/bin/activate
```

### Set up the git hook scripts by [pre-commit](https://pre-commit.com/#3-install-the-git-hook-scripts)

```shell
pre-commit install
```

### Open `./src` or `main.py` and just code it

### Open your app

```shell
uv run main.py
```

## 2.2. Alternative instruction with pip tool (not recommended)

### [Install python 3.11](https://docs.python.org/3.11/using/index.html)

### Install pip by this [documentation](https://pip.pypa.io/en/stable/installation/)

### Install venv

Create venv

```shell
python -m venv .venv
```

Activate venv

```
# На Windows:
$ .venv\Scripts\activate

# На macOS и Linux:
$ source .venv/bin/activate
```

After that install dependencies

```shell
pip install .
```

### Set up the git hook scripts by [pre-commit](https://pre-commit.com/#3-install-the-git-hook-scripts)

```shell
pre-commit install
```

### Open `./src` or `main.py` and just code it

### Open your app

```shell
python main.py
```
