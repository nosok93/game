from lesson_base import lesson, theory, code, quiz, practice

LESSON = lesson(
    id=2,
    chapter="Курс молодого бойца",
    title="Анатомия .ini файла",
    subtitle="Ключи, значения и обязательный минимум",
    pages=[
        theory("Ключ и значение",
               "Каждая строка внутри секции — это пара **ключ: значение**.\n\n"
               "`maxHp: 200` — ключ `maxHp`, значение `200`\n"
               "`canAttack: true` — ключ `canAttack`, значение `true`\n\n"
               "Комментарии начинаются с `#` — игра их полностью игнорирует. "
               "Ими удобно помечать свои заметки."),
        theory("Обязательный минимум",
               "Чтобы игра загрузила юнит без ошибок, в файле **обязаны** быть:\n\n"
               "• `[core]` → `name`, `maxHp`, `price`, `mass`, `radius`\n"
               "• `[graphics]` → `image`\n"
               "• `[attack]` → `canAttack`, `canAttackFlyingUnits`, "
               "`canAttackLandUnits`, `canAttackUnderwaterUnits`\n"
               "• `[movement]` → `movementType`\n\n"
               "Забудешь хоть один ключ — игра выдаст ошибку при загрузке."),
        code("Минимальный рабочий юнит",
             "# Мой первый разведчик\n"
             "[core]\n"
             "name: scout\n"
             "displayText: Разведчик\n"
             "maxHp: 120\n"
             "price: 300\n"
             "mass: 40\n"
             "radius: 12\n"
             "\n"
             "[graphics]\n"
             "image: scout.png\n"
             "\n"
             "[attack]\n"
             "canAttack: true\n"
             "canAttackFlyingUnits: false\n"
             "canAttackLandUnits: true\n"
             "canAttackUnderwaterUnits: false\n"
             "\n"
             "[movement]\n"
             "movementType: LAND\n"
             "moveSpeed: 1.6",
             note="Этот код уже можно сохранить в .ini файл, и игра его поймёт."),
        quiz("Какой символ начинает комментарий?",
             ["//", "<!--", "*", "#"], 3,
             explain="Всё после # до конца строки игра игнорирует."),
        quiz("Какой из этих ключей обязателен в [core]?",
             ["speed", "name", "color", "sound"], 1,
             explain="name — внутреннее уникальное имя юнита. Без него будет ошибка."),
        practice("Собери минимального юнита: впиши недостающие ключи и значения",
                 "[core]\n"
                 "___1___: scoutBot\n"
                 "___2___: 150\n"
                 "price: 300\n"
                 "mass: 40\n"
                 "___3___: 12\n"
                 "\n"
                 "[graphics]\n"
                 "___4___: scout.png\n"
                 "\n"
                 "[attack]\n"
                 "___5___: true\n"
                 "canAttackFlyingUnits: false\n"
                 "canAttackLandUnits: true\n"
                 "canAttackUnderwaterUnits: false\n"
                 "\n"
                 "[movement]\n"
                 "movementType: ___6___",
                 {"1": "name", "2": "maxHp", "3": "radius", "4": "image", "5": "canAttack", "6": "LAND"},
                 hint="Вспомни обязательный минимум из теории. 6-й пропуск — сухопутный тип движения.",
                 explain="Ты только что написал полностью рабочий юнит с нуля!"),
    ],
)