from lesson_base import lesson, theory, code, quiz, practice

LESSON = lesson(
    id=13,
    chapter="Продвинутые секции",
    title="LogicBoolean — логика",
    subtitle="Условия, сравнения и функции",
    pages=[
        theory("if, and, or, not",
               "Логические поля (`isLocked`, `autoTrigger`, `isVisible`, `canAttackFlyingUnits`…) "
               "принимают условия.\n"
               "Внутри условий работают арифметика и сравнения: `+  -  *  /`, а также `<`, `>`, `<=`, `>=`, `==`, `!=` (операторы сравнения доступны с 1.15).\n"
               "Сравнения можно писать и в старом стиле — параметрами функций: `greaterThan=`, `lessThan=`, `empty=`, `full=`.\n\n"
               "• `if` — любое условие начинается с него: `if self.isFlying()`\n"
               "• `and` — истинны **все** части; `or` — хотя бы одна; `not` — отрицание "
               "(в примере `if not self.isOverLiquid()` условие истинно, когда юнит **не** над водой)"),
        theory("Функции самопроверки",
               "Самые ходовые функции юнита (префикс `self.` можно писать на любом юните по ссылке):\n\n"
               "• `self.hp()`, `self.energy()`, `self.shield()`, `self.ammo()`, `self.resource(type=gold)`\n"
               "• `self.isFlying()`, `self.isMoving()`, `self.isInWater()`, `self.isOverLiquid()`, `self.isUnderwater()`\n"
               "• `self.hasFlag(id=1)` — флаг 0–31, `setFlag` / `unsetFlag` ставятся через `price` и `resourceUsage`\n"
               "• `self.tags(includes="tank")` — проверка тега\n"
               "• `numberOfUnitsInTeam(withTag="factory", lessThan=3)` — счётчик юнитов; есть версии для союзников, врагов и нейтралов: `numberOfUnitsInAllyTeam()`, `numberOfUnitsInEnemyTeam()`, `numberOfUnitsInNeutralTeam()`\n"
               "• `distanceBetween(self, other)` и `directionBetween(unit1, unit2)` — дистанция и направление между юнитами или маркерами; `rnd(min, max)` — случайное число; `select(условие, a, b)` — выбор значения по условию; `str()` и `int()` — преобразование типов"),
        theory("Ссылки на юнитов",
               "Кроме `self` есть готовые ссылки:\n"
               "`parent` — транспорт или носитель, `attacking` — текущая цель, `lastDamagedBy` — последний обидчик, "
               "`thisActionTarget` — цель текущего действия, `eventSource` — виновник события, "
               "`customTarget1` и `customTarget2` — свои привязки (по умолчанию `customTarget1` — создатель юнита), "
               "`nearestUnit(withinRange=500, withTag="x", relation="enemy")` — поиск ближайшего, "
               "`nullUnit` — пустая ссылка для сравнений, `getAsMarker()` — маркер позиции (легче юнита, переживает его смерть), "
               "`createMarker(x, y)` — маркер по координатам."),
        code("Примеры условий",
             "isLocked: if self.ammo(lessThan=1)\n"
             "isVisible: if self.energy(greaterThan=0.5) or self.hasFlag(id=3)\n"
             "isActive: if not self.isMoving() and self.hp(greaterThan=100)\n"
             "autoTrigger: if numberOfUnitsInTeam(withTag=\"base\", lessThan=1)\n"
             "canAttackFlyingUnits: if self.height(greaterThan=20)",
             note="Эти строки можно вставлять в действия, турели, canBuild и даже в [attack]."),
        quiz("У юнита maxHp: 200. Какое условие истинно, когда здоровье меньше половины?",
             ["if self.hp(empty=true)", "if self.hp(greaterThan=100)", "if self.hp(lessThan=100)", "if self.maxHp()"], 2,
             explain="lessThan=100 означает «меньше ста»."),
        practice("Собери условия: 1) энергия полная И юнит летит; 2) виден, только если НЕ над водой",
                 "isLocked: if self.isEnergyFull() ___1___ self.___2___()\n"
                 "isVisible: if ___3___ self.isOverLiquid()",
                 {"1": "and", "2": "isFlying", "3": "not"},
                 hint="И — это and, отрицание — not.",
                 explain="Такие условия работают почти везде: блокировки, видимость, авто-триггеры."),
    ],
)