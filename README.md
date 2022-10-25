# Игра Сапёр


## ![flake8 test](https://github.com/Prrromanssss/LyceumYandex_django/actions/workflows/python-package.yml/badge.svg)


В этом проекте я написал известную игру - Сапёр.

[Подробнее об игре Сапёр](https://ru.wikipedia.org/wiki/%D0%A1%D0%B0%D0%BF%D1%91%D1%80_(%D0%B8%D0%B3%D1%80%D0%B0))
***
## Установка 
* склонировать проект из гитхаба
```commandline
git clone https://github.com/Prrromanssss/Minesweeper_GUI
```
* поставить виртуальное окружение
### Mac OS / Linux
```commandline
python -m venv venv
source venv/bin/activate
```
### Windows
```commandline
python -m venv venv
.\venv\Scripts\activate
```
## Запуск
```commandline
python -m main.py
```

### Все библиотеки в этом проекте встроены.

## Правила
Данный проект повторяет все правила, которые есть в официальной игре(Подробнее: [тут](https://ru.wikipedia.org/wiki/%D0%A1%D0%B0%D0%BF%D1%91%D1%80_(%D0%B8%D0%B3%D1%80%D0%B0)))

## Управление
* __Открытие кнопки__:
Для того чтобы открыть какую-то клетку, необходимо нажать на неё левой кнопкой мыши.
* __Поставить или убрать флаг__: 1) Способ - нажать правой кнопкой мыши на клетку, 2) Способ - с помощью клавиши Tab и Shift+Tab перемешать курсор вперед и назад соответственно. На выбранную кнопку навести данный курсор и нажать Enter.

## Настройки
У данного файла есть меню, где можно выбрать одну из трех настроек.
* __Играть__ - перезапустить игру
* __Настройки__ - настроить количество строк, колонок, мин
* __Выход__ - выйти из игры

![Иллюстрация проекта](https://github.com/Prrromanssss/Minesweeper_GUI/raw/main/media/game_in_process_image.png)
***
