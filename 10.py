from lesson_base import lesson, theory, code, quiz, practice

LESSON = lesson(
    id=10,
    chapter="Базовые секции",
    title="[ai] — мозг для ботов",
    subtitle="Как ИИ распоряжается твоим юнитом",
    pages=[
        theory("На кого это влияет",
               "Секция `[ai]` **не влияет на игрока** — она объясняет компьютерному "
               "противнику, что делать с твоим юнитом.\n\n"
               "• `useAsBuilder: true` — использовать как строителя\n"
               "• `useAsHarvester` — как сборщика ресурсов; `useAsTransport` — как транспорт "
               "(все три по умолчанию включаются, если юнит умеет соответствующее)\n"
               "• `disableUse: true` — запретить ИИ строить этот юнит вообще; `ai_upgradePriority` — приоритет апгрейда (0–1)"),
        theory("Приоритеты строительства",
               "• `buildPriority` — от 0 до 1, насколько ИИ хочет это построить. "
               "Для ориентира: первый наземный завод у ИИ имеет 0.8, авиазавод 0.48, первая турель 0.47; "
               "`noneInBaseExtraPriority` — надбавка, если в базе этого ещё нет; `noneGlobalExtraPriority` — надбавка, если этого нет нигде на карте; "
               "`recommendedInEachBaseNum` — сколько штук ИИ рекомендует держать в каждой базе; `recommendedInEachBasePriorityIfUnmet` — приоритет, пока рекомендация не выполнена (по умолчанию 0.5)\n"
               "• `maxGlobal` — максимум таких зданий на всю карту для команды ИИ; "
               "`maxEachBase` — максимум на одну базу. Проверить «базу» ИИ в песочнице: включить дебаг и нажать `Shift+F3`\n"
               "• `upgradedFrom` — связка со старой версией, чтобы лимиты считались совместно; "
               "`notPassivelyTargetedByOtherUnits` и `lowPriorityTargetForOtherUnits` — чтобы ИИ не зацикливался на стенах и тому подобном"),
        code("ИИ-настройки строителя и турели",
             "[ai]\n"
             "useAsBuilder: true\n"
             "buildPriority: 0.4\n"
             "maxGlobal: 10\n"
             "maxEachBase: 4\n"
             "noneInBaseExtraPriority: 2"),
        quiz("На кого влияет секция [ai]?",
             ["только на ИИ", "только на игрока", "на всех", "ни на кого"], 0,
             explain="Игроку она ничего не запрещает — только подсказывает ботам."),
        quiz("Как ограничить число зданий на одну базу ИИ?",
             ["maxGlobal", "maxEachBase", "buildPriority", "disableUse"], 1,
             explain="maxEachBase — лимит на базу, maxGlobal — на всю карту."),
        practice("ИИ-строитель: включи его как строителя, приоритет 0.4, максимум 4 на базу",
                 "[ai]\n"
                 "useAsBuilder: ___1___\n"
                 "buildPriority: ___2___\n"
                 "maxEachBase: ___3___",
                 {"1": "true", "2": "0.4", "3": "4"},
                 hint="Булевы значения пишутся как true / false.",
                 explain="Хорошие приоритеты — залог того, что ИИ вообще будет строить твои юниты."),
    ],
)