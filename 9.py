from lesson_base import lesson, theory, code, quiz, practice

LESSON = lesson(
    id=9,
    chapter="Базовые секции",
    title="[movement] — движение",
    subtitle="Скорость, повороты и типы местности",
    pages=[
        theory("Типы движения",
               "`movementType` — единственный обязательный ключ. Варианты:\n\n"
               "• `LAND` — обычная наземная техника, не ходит по воде и скалам напрямую "
               "(в паре с `OVER_CLIFF` юнит шагает по скалам)\n"
               "• `AIR` — авиация, по умолчанию висит на высоте `targetHeight: 35`\n"
               "• `WATER` — только вода; `HOVER` — амфибия, летает над сушей и водой; "
               "`OVER_CLIFF_WATER` — ходит по скалам и воде; `BUILDING` — стоит на месте; "
               "`NONE` — не двигается; `OVER_CLIFF` — ходит по скалам"),
        theory("Скорость и повороты",
               "• `moveSpeed` — максимальная скорость; `moveAccelerationSpeed` — разгон до максимума; "
               "`moveDecelerationSpeed` — торможение. **Слишком низкое торможение = юнит проскакивает точки маршрута!**\n"
               "• `reverseSpeedPercentage` — скорость заднего хода в долях от прямой (по умолчанию 0.6; при 1 реверсирует как вперёд — удобно для неповоротливых)\n"
               "• `maxTurnSpeed` — предел скорости поворота; `turnAcceleration` — разгон поворота "
               "(по умолчанию мгновенный)\n"
               "• `moveSlidingMode: true` — скольжение с инерцией; `moveIgnoringBody: true` — двигаться, не доворачивая корпус (корабли, авиация); `moveSlidingDir` — направление скольжения; `joinsGroupFormations` — участие в групповых построениях (по умолчанию true, лучше не трогать)"),
        theory("Особое для воздуха",
               "• `targetHeight` — высота полёта (по умолчанию 0; у `AIR` — 35); `targetHeightDrift` — плавный дрейф высоты (по умолчанию 0; у `AIR` — 1.5)\n"
               "• `startingHeightOffset` — начальная высота при появлении (по умолчанию 0)\n"
               "• `landOnGround` — садиться ли на землю в простое (по умолчанию false)\n"
               "• `slowDeathFall: true` — падать медленно после смерти, сохраняя скорость (большие самолёты)\n"
               "• `heightChangeRate` — скорость изменения высоты; `fallingAcceleration` и `fallingAccelerationDead` — ускорение падения живого и мёртвого юнита"),
        code("Ховер и самолёт",
             "[movement]\n"
             "movementType: HOVER\n"
             "moveSpeed: 1.4\n"
             "moveAccelerationSpeed: 0.08\n"
             "moveDecelerationSpeed: 0.2\n"
             "maxTurnSpeed: 3.5\n"
             "turnAcceleration: 1.2\n"
             "moveSlidingMode: true",
             note="А для авиации: movementType: AIR, targetHeight: 35, slowDeathFall: true."),
        quiz("Какой movementType нужен самолёту?",
             ["LAND", "HOVER", "AIR", "OVER_CLIFF"], 2,
             explain="AIR даёт полёт и автоматическую высоту 35."),
        quiz("Юнит проскакивает точки маршрута и не может остановиться. Какой ключ увеличить?",
             ["moveAccelerationSpeed", "moveDecelerationSpeed", "reverseSpeedPercentage", "moveSlidingMode"], 1,
             explain="moveDecelerationSpeed отвечает за торможение."),
        practice("Ховер-танк: тип движения, скорость 1.4, ускорение поворота 1.5",
                 "[movement]\n"
                 "movementType: ___1___\n"
                 "moveSpeed: ___2___\n"
                 "maxTurnSpeed: 3\n"
                 "___3___: 1.5",
                 {"1": "HOVER", "2": "1.4", "3": "turnAcceleration"},
                 hint="Амфибия — это HOVER. Ускорение поворота — это про поворот.",
                 explain="Дробные значения скорости — норма: 1.0 это базовая скорость пехоты."),
    ],
)