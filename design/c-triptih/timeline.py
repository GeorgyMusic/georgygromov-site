# -*- coding: utf-8 -*-
"""События для нотной ленты. Перенесены из версии v2 (агент, ноябрь 2026) без изменений."""

KINDS = {
    "concert": "сольный концерт",
    "duo":     "фортепианный дуэт",
    "lecture": "лекция и конференция",
    "master":  "мастер-класс",
}

TIMELINE = [
    ("2022-04-20", "lecture", "Выступление для Федерации профессиональных менторов и коучей", "Москва"),
    ("2022-11-20", "duo",     "Дуэтный вечер: Брух, Дебюсси, Сен-Санс, Бузони, Брамс", "Piano Salon Christophori, Берлин"),
    ("2022-12-09", "concert", "Сольный вечер: Бах, Шопен, Чайковский", "Piano Salon Christophori, Берлин"),
    ("2023-02-03", "lecture", "International Conference for Performance Development Experts: оркестр как система", "Каир"),
    ("2023-09-11", "lecture", "«Стили управления на примере выдающихся дирижёров» для KPMG", "онлайн"),
    ("2024-05-29", "concert", "Сольный вечер", "Piano Salon Christophori, Берлин"),
    ("2024-07-14", "concert", "Французская программа", "Piano Salon Christophori, Берлин"),
    ("2024-09-18", "concert", "Сольный вечер", "Piano Salon Christophori, Берлин"),
    ("2024-09-30", "duo",     "Дуэтный вечер", "Piano Salon Christophori, Берлин"),
    ("2024-11-17", "concert", "Сольный вечер", "Piano Salon Christophori, Берлин"),
    ("2024-12-12", "duo",     "Дуэтный вечер", "Piano Salon Christophori, Берлин"),
    ("2025-02-02", "master",  "Мастер-класс «Спиральная динамика», программа Executive MBA", "Школа управления СКОЛКОВО"),
    ("2025-02-28", "duo",     "Дуэтный вечер: Брух, Дебюсси, Сен-Санс, Бузони, Брамс", "Piano Salon Christophori, Берлин"),
    ("2025-04-29", "concert", "Сольный вечер", "Piano Salon Christophori, Берлин"),
    ("2025-05-29", "concert", "Шуберт, Рахманинов", "Piano Salon Christophori, Берлин"),
    ("2025-06-11", "master",  "Metodi di coaching nell'educazione musicale", "Conservatorio Mascagni, Ливорно"),
    ("2025-07-29", "lecture", "Интервью: чему дирижирование учит управлению командами", "Школа управления СКОЛКОВО"),
    ("2025-09-10", "lecture", "Выступление для Roche", "онлайн"),
    ("2025-09-16", "concert", "Hommage à Lipatti: Бах, Шопен, Шуберт", "Piano Salon Christophori, Берлин"),
    ("2025-09-27", "concert", "«Три гения. Три друга. Три пути»", "Люнебург"),
    ("2025-10-30", "lecture", "Executive Coaching and Mentoring Day", "Школа управления СКОЛКОВО"),
    ("2025-12-07", "duo",     "Дуэтный вечер", "Piano Salon Christophori, Берлин"),
    ("2026-01-25", "duo",     "Дуэтный вечер: Брух, Дебюсси, Сен-Санс, Бузони, Брамс", "Piano Salon Christophori, Берлин"),
    ("2026-03-01", "concert", "Моцарт, Барток, Шуман", "Piano Salon Christophori, Берлин"),
    ("2026-03-22", "concert", "Сольный вечер", "Piano Salon Christophori, Берлин"),
    ("2026-04-17", "duo",     "Шуман, Розенблат, Моцарт - Бузони, Равель", "Piano Salon Christophori, Берлин"),
    ("2026-04-21", "master",  "«Стили управления: теория и практика дирижёра» для компании «Контур»", "онлайн"),
    ("2026-05-21", "master",  "The Heartbeat of Coaching: спиральная динамика и работа с живым оркестром", "Скопье"),
    ("2026-05-26", "master",  "Мастер-класс «Tchaikovsky», Advanced professional training for conductors", "UdK Berlin"),
    ("2026-06-28", "concert", "Шопен: десять мазурок и Вторая соната · Шуман: Карнавал", "Piano Salon Christophori, Берлин"),
    ("2026-09-11", "duo",     "Брамс, Мийо, Дебюсси", "Piano Salon Christophori, Берлин"),
    ("2026-09-20", "master",  "«Как слушать музыку. Как писать музыку» для ProStereo", "онлайн"),
    ("2026-12-13", "duo",     "«Щелкунчик» Чайковского - Громова · «Золушка» Прокофьева - Плетнёва", "Piano Salon Christophori, Берлин"),
]

MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня",
          "июля", "августа", "сентября", "октября", "ноября", "декабря"]

def human(iso):
    y, m, d = map(int, iso.split('-'))
    return f"{d} {MONTHS[m-1]} {y}"
