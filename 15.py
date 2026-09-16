from lesson_base import lesson, theory, code, quiz, practice

LESSON = lesson(
    id=15,
    chapter="Ресурсы и цены",
    title="Ресурсы: свои валюты",
    subtitle="Глобальные и локальные ресурсы",
    pages=[
        theory("Цена — это не только кредиты",
               "Поле `price` понимает список ресурсов: "
               "`price: 500, gold=5, stone=10`.\n\n"
               "Встроенные «ресурсы»:\n"
               "• `credits` — кредиты, глобальная валюта команды\n"
               "• `energy` — энергия юнита (лазеры, щиты, боезапас)\n"
               "• `hp` и `shield` — здоровье и щит, можно тратить и восполнять через `addResources: hp=-100`\n"
               "• `ammo` — скрытый локальный боезапас юнита, удобен для своих механик; есть `setFlag` / `unsetFlag` (флаги 0–31), `hasFlag` и `hasMissingFlag` — для условий"),
        theory("Глобальные ресурсы",
               "`[global_resource_имя]` — ресурс **всей команды**, как кредиты. "
               "Показывается наверху экрана.\n"
               "`displayName` — имя в интерфейсе; `displayNameShort` — короткое имя для мелких элементов; "
               "`displayColor` — цвет; `hidden` — скрыть от игрока; `iconImage` — иконка; "
               "`displayWhenZero` — показывать даже пустым; `displayPos` — позиция в интерфейсе; "
               "`displayTextPrefix` / `displayTextPostfix` — префикс и суффикс значения; "
               "`appendResourceInHUD` — пристыковать другой ресурс в HUD; "
               "`valueInStats` — вес в послематчевой статистике.\n"
               "Совет: объяви его в `all-units.template`, чтобы использовать во всём моде."),
        theory("Локальные ресурсы и генерация",
               "`[resource_имя]` — ресурс **одного юнита**, как боезапас. "
               "`equivalentGlobalResourceForAI` подсказывает ИИ, во что глобальное превращается этот локальный ресурс "
               "(например, когда харвестер сдаёт груз).\n"
               "Генерация дохода в `[core]`: `generation_resources: credits=5, gold=20`; "
               "`generation_credits` — только кредиты; `generation_delay: 40` — период (менять не рекомендуется); "
               "`generation_active` — логический выключатель генерации; `borrowResourcesWhileAlive` — занять ресурс при появлении и вернуть при смерти.\n"
               "Добыча: `canReclaimResources: true` у харвестера и `resourceRate` у ресурсной точки (обычно на нейтральной команде)."),
        code("Нефть как валюта мода",
             "[global_resource_oil]\n"
             "displayName: Нефть\n"
             "displayColor: #3b2f2f\n"
             "iconImage: oil_icon.png\n"
             "\n"
             "[resource_shells]\n"
             "displayName: Снаряды\n"
             "hidden: true\n"
             "\n"
             "[core]\n"
             "price: credits=500, oil=50\n"
             "generation_resources: credits=5, oil=1\n"
             "generation_delay: 40"),
        quiz("Кому принадлежит глобальный ресурс?",
             ["одному юниту", "всей команде", "только зданиям", "только ИИ"], 1,
             explain="Глобальный ресурс работает как кредиты — общий для команды."),
        quiz("Локальный ресурс юнита больше всего похож на…",
             ["кредиты", "боезапас", "карту", "команду"], 1,
             explain="Встроенный пример локального ресурса — ammo, боезапас."),
        practice("Объяви нефть: имя в интерфейсе, цвет, и используй её в цене",
                 "[global_resource_oil]\n"
                 "___1___: Нефть\n"
                 "___2___: #3b2f2f\n"
                 "hidden: false\n"
                 "\n"
                 "[core]\n"
                 "price: credits=500, ___3___=50",
                 {"1": "displayName", "2": "displayColor", "3": "oil"},
                 hint="Имя ресурса в игре задаёт displayName.",
                 explain="Теперь юнит стоит 500 кредитов и 50 нефти одновременно."),
    ],
)