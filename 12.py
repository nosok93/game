from lesson_base import lesson, theory, code, quiz, practice

LESSON = lesson(
    id=12,
    chapter="Продвинутые секции",
    title="[action_NAME] — действия",
    subtitle="Кнопки, апгрейды и автопилот",
    pages=[
        theory("Кнопки юнита",
               "`[action_имя]` — кнопка в меню юнита. `[hiddenAction_имя]` — то же самое, "
               "но **игрок её не видит**: скрытые действия нужны для внутренней логики.\n"
               "Действие не должно быть пустым — нужен хотя бы один исход.\n"
               "Порядок в меню задаёт `pos` — он объединяется с позициями кнопок `canBuild`.\n\n"
               "• `text` и `description` — подпись и описание кнопки "
               "(оба поддерживают динамический текст вроде `Очки: %{self.resource.ammo}`)\n"
               "• `price` — цена действия; `buildSpeed: 5s` — время выполнения в очереди; "
               "`highPriorityQueue: true` — перепрыгнуть обычные очереди; "
               "`whenBuilding_cannotMove: true` — нельзя двигаться во время очереди (деплой); "
               "`whenBuilding_playAnimation` / `whenBuilding_rotateTo` — анимация и поворот во время очереди"),
        theory("Триггеры",
               "• `autoTrigger` — логическое условие. Когда оно истинно, действие срабатывает "
               "**само**, игнорируя цену, очередь и видимость — это и есть автопилот; "
               "`autoTriggerCheckRate` — как часто проверять (`everyFrame` по умолчанию); `autoTriggerCheckWhileNotBuilt` — проверка даже у недостроенных юнитов\n"
               "• `autoTriggerOnEvent` — срабатывать по событию: `created`, `destroyed`, `tookDamage`, "
               "`killedAnyUnit`, `queuedUnitFinished`, `teamChanged`, `enteredTransport`, `leftTransport` и многим другим. "
               "В обработчике доступен `eventSource` — виновник события (кто нанёс урон, кто умер и т.д.); "
               "`autoTriggerOnEventRecursionLimit` — защита от бесконечных циклов; `autoTriggerCooldownTime` — перезарядка авто-триггера (по умолчанию 1 секунда)"),
        theory("Что умеют действия",
               "• `convertTo` — превратить юнит в другой (свойства сохраняются); "
               "`convertTo_keepCurrentTags` / `convertTo_keepCurrentFields` — сохранить теги и поля; "
               "`whenBuilding_temporarilyConvertTo` — превращение только на время очереди\n"
               "• `addResources` и `addEnergy` — выдать ресурсы/энергию; `deleteSelf` — удалить без взрыва; "
               "`setUnitStats` — поменять статы на лету; `setUnitMemory` — записать в память юнита; "
               "`resetCustomTimer` — сбросить таймер; `spawnEffects` — эффекты; `spawnUnits` и `produceUnits` — спавн юнитов "
               "(второй выходит как с завода и получает точку отхода)\n"
               "• `fireTurretXAtGround` — выстрелить турелью по точке на земле "
               "(обходит `canShoot` турели); варианты: `fireTurretXAtGround_withProjectile` — другим снарядом, "
               "`fireTurretXAtGround_count` — количество выстрелов, `fireTurretXAtGround_withTarget` — по цели по ссылке, "
               "`fireTurretXAtGround_onlyOverPassableTileOf` — только по проходимым тайлам; `fireTurretXAtSelfOnDeath` в `[core]` — выстрел по себе при смерти; "
               "`offsetSelfAbsolute` — сдвинуть юнита по координатам; `teleportTo` — телепорт по ссылке на юнит или маркер; `setCustomTarget1` / `setCustomTarget2` — привязки юнитов без памяти; "
               "`addWaypoint_type` — добавить точку маршрута (move, attack, reclaim…); `clearAllWaypoints` / `clearActiveWaypoint` — очистка маршрута; "
               "`alsoTriggerAction` / `alsoQueueAction` — цепочки действий; `addActionCooldownTime` — перезарядка кнопки; `playSoundAtUnit`, `playSoundGlobally`, `playSoundToPlayer` — звуки; "
               "`showMessageToPlayer`, `showMessageToAllPlayers`, `showQuickWarLogToAllPlayers` — сообщения; `temporarilyAddTags` / `temporarilyRemoveTags` / `addGlobalTeamTags` — теги; "
               "`attachments_addNewUnits` — добавить юниты в слоты-прицепы; `switchToNeutralTeam` / `switchToAggressiveTeam` / `switchToTeam` — смена команды; "
               "`takeResources` — выкачивать ресурсы из других юнитов; `convertResource_from` / `convertResource_to` — конвертация ресурсов; "
               "`setBuilt: 0.5` — прогресс постройки 0–1; `sendMessageTo` / `sendMessageWithTags` / `sendMessageWithData` — сообщения юнитам; "
               "`ai_isDisabled` / `ai_isHighPriority` — настройка поведения ИИ; `isAlsoViewableByAllies` / `isAlsoViewableByEnemies` — показ действия другим игрокам (статы, счётчики)"),
        code("Три действия",
             "[action_repair]\n"
             "text: Ремкомплект\n"
             "description: Чинит корпус на 100\n"
             "pos: 1\n"
             "price: 200\n"
             "buildSpeed: 4s\n"
             "addResources: hp=100\n"
             "\n"
             "[action_upgrade]\n"
             "text: Улучшить\n"
             "pos: 2\n"
             "price: 800\n"
             "buildSpeed: 6s\n"
             "convertTo: tank_v2\n"
             "\n"
             "[hiddenAction_auto_heal]\n"
             "autoTrigger: if self.hp(lessThan=50) and self.customTimer(laterThanSeconds=10)\n"
             "addResources: hp=5\n"
             "resetCustomTimer: true"),
        quiz("Как называется действие, которое игрок не видит?",
             ["hiddenAction_NAME", "action_NAME", "template_NAME", "comment_NAME"], 0,
             explain="hiddenAction работает так же, но спрятан от интерфейса."),
        quiz("Какой ключ превращает юнит в другой юнит?",
             ["spawnUnits", "convertTo", "addEnergy", "deleteSelf"], 1,
             explain="convertTo — основа всех апгрейдов."),
        practice("Кнопка апгрейда: тип отображения `upgrade`, превращение в `tank_v2`",
                 "[action_upgrade]\n"
                 "text: Улучшить\n"
                 "price: 800\n"
                 "buildSpeed: 6s\n"
                 "___1___: tank_v2\n"
                 "___2___: upgrade",
                 {"1": "convertTo", "2": "displayType"},
                 hint="Первый пропуск — превращение, второй — тип отображения кнопки.",
                 explain="displayType влияет на вид кнопки: none, rally, upgrade, queueUnit, building, action."),
    ],
)