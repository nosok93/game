from lesson_base import lesson, theory, code, quiz, practice

LESSON = lesson(
    id=8,
    chapter="Базовые секции",
    title="Собираем танк целиком",
    subtitle="Первый полноценный юнит",
    pages=[
        theory("Порядок сборки",
               "Полноценный стреляющий юнит — это связка секций:\n"
               "`[core]` → `[graphics]` → `[attack]` → `[turret_1]` → "
               "`[projectile_...]` → `[movement]`\n\n"
               "Главное правило: **турель ссылается на снаряд по имени**. "
               "`projectile: shot` в турели означает «ищи секцию `[projectile_shot]`».\n\n"
               "Совет из официальной справки: начинай освоение именно с турелей и снарядов — "
               "это самый быстрый путь к ванильному стилю."),
        theory("Читай ошибки!",
               "Если игра не может загрузить юнит, она пишет, **чего именно не хватает**. "
               "Вот реальная ошибка:\n\n"
               "`Could not find canAttackUnderwaterUnits in section: attack`\n\n"
               "Перевод: в секции `[attack]` не найден ключ `canAttackUnderwaterUnits`. "
               "Открываешь файл, находишь секцию из ошибки, дописываешь ключ. "
               "В 90% случаев ошибка мода — это просто забытая строка."),
        code("Готовый боевой танк",
             "[core]\n"
             "name: battleTank\n"
             "displayText: Боевой танк\n"
             "maxHp: 320\n"
             "price: 600\n"
             "mass: 120\n"
             "radius: 14\n"
             "\n"
             "[graphics]\n"
             "image: tank_body.png\n"
             "image_turret: tank_gun.png\n"
             "\n"
             "[attack]\n"
             "canAttack: true\n"
             "canAttackFlyingUnits: false\n"
             "canAttackLandUnits: true\n"
             "canAttackUnderwaterUnits: false\n"
             "maxAttackRange: 140\n"
             "\n"
             "[turret_1]\n"
             "x: 0\n"
             "y: 4\n"
             "projectile: shot\n"
             "delay: 1.1s\n"
             "turnSpeed: 4\n"
             "\n"
             "[projectile_shot]\n"
             "directDamage: 45\n"
             "life: 200\n"
             "speed: 6\n"
             "drawType: 0\n"
             "\n"
             "[movement]\n"
             "movementType: LAND\n"
             "moveSpeed: 1.0\n"
             "maxTurnSpeed: 3\n"
             "turnAcceleration: 1"),
        quiz("Ошибка: «Could not find canAttackUnderwaterUnits in section: attack». Что делать?",
             ["добавить canAttackUnderwaterUnits в [attack]", "удалить секцию [attack]", "переименовать файл", "ничего, это просто предупреждение"], 0,
             explain="Игра буквально называет секцию и ключ, который нужно дописать."),
        practice("Свяжи башню со снарядом `shot`, допиши имя секции снаряда и тип движения",
                 "[turret_1]\n"
                 "x: 0\n"
                 "y: 8\n"
                 "projectile: ___1___\n"
                 "delay: 1s\n"
                 "\n"
                 "[projectile___2___]\n"
                 "directDamage: 40\n"
                 "life: 200\n"
                 "speed: 5\n"
                 "\n"
                 "[movement]\n"
                 "movementType: ___3___\n"
                 "moveSpeed: 1.1",
                 {"1": "shot", "2": "_shot", "3": "LAND"},
                 hint="Имя секции снаряда складывается из названия и имени: [projectile_имя].",
                 explain="Ты связал турель и снаряд — это главный «клей» всего моддинга."),
    ],
)