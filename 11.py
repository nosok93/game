from lesson_base import lesson, theory, code, quiz, practice

LESSON = lesson(
    id=11,
    chapter="Продвинутые секции",
    title="canBuild — очередь строительства",
    subtitle="Что и как строит твоё здание",
    pages=[
        theory("canBuild_NAME",
               "Секция `[canBuild_1]`, `[canBuild_2]` и так далее описывают кнопки "
               "в очереди строительства завода.\n\n"
               "• `name: lightTank, heavyTank` — список юнитов, которые можно построить. "
               "Специальное слово `setRally` добавляет кнопку точки сбора "
               "(список может начинаться прямо с него: `name: setRally, tank`)\n"
               "• `pos: 0.1` — порядок кнопки в интерфейсе; `tech` — техуровень (1–3, влияет на цвет кнопки)\n"
               "• `forceNano: true` — строить цель как здание, даже если это юнит; `isVisible` и `isLocked` — логические условия; "
               "`isLockedMessage` — сообщение, почему заблокировано; `isLockedAlt` / `isLockedAlt2` — альтернативные причины блокировки со своими сообщениями; "
               "`isGuiBlinking` — мигание кнопки в интерфейсе"),
        theory("Цены и обратная связь",
               "• `price` — переопределить цену цели прямо здесь: `price: credits=1000, ammo=5` "
               "(по умолчанию берётся цена самого юнита)\n"
               "• `addResources` — добавить ресурсы владельцу при заказе: `addResources: ammo=5, setFlag=1`\n\n"
               "Альтернативный путь — `builtFrom_1_name` в самом юните: «меня можно строить из этих зданий». "
               "`builtFrom` — связь в обратную сторону, `canBuild` обычно удобнее.\n"
               "Для выхода построенных юнитов есть `exit_x`, `exit_y`, `exit_dirOffset`, `exit_heightOffset`, "
               "`exit_moveAwayAmount` и `exitHeightIgnoreParent` (для зданий-пристроек)."),
        code("Очередь завода",
             "[canBuild_1]\n"
             "name: setRally, lightTank, heavyTank\n"
             "pos: 0.1\n"
             "tech: 1\n"
             "isLocked: if self.resource(type=oil) < 10\n"
             "isLockedMessage: Нужно 10 нефти"),
        quiz("Как добавить кнопку точки сбора в очередь?",
             ["написать setRally в списке name", "rallyPoint: true", "addWaypoint: rally", "pos: rally"], 0,
             explain="setRally — служебное слово внутри списка юнитов."),
        practice("Добавь кнопку точки сбора и блокировку при нехватке нефти",
                 "[canBuild_1]\n"
                 "name: ___1___, lightTank, heavyTank\n"
                 "pos: 0.1\n"
                 "isLocked: if self.resource(type=___2___) < 10\n"
                 "isLockedMessage: Нужно 10 нефти",
                 {"1": "setRally", "2": "oil"},
                 hint="Служебное слово точки сбора пишется прямо в списке.",
                 explain="isLocked принимает любые LogicBoolean — разберём их в уроке про логику."),
    ],
)