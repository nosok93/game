from lesson_base import lesson, theory, code, quiz, practice

LESSON = lesson(
    id=7,
    chapter="Базовые секции",
    title="[projectile_NAME] — снаряды",
    subtitle="Урон, полёт и спецэффекты",
    pages=[
        theory("Обязательная база",
               "Снаряду нужны: **урон** и **время жизни**.\n\n"
               "• `directDamage: 30` — точечный урон по цели, в которую попал\n"
               "• `areaDamage: 40` — урон по области вокруг точки попадания; размер области задаёт `areaRadius` "
               "(урон спадает к краям, если не включить `areaDamageNoFalloff`)\n"
               "• `life: 300` — сколько снаряд живёт до исчезновения. "
               "Подбирай под скорость и дальность, иначе снаряд умрёт на полпути\n"
               "• `targetGround: true` — снаряд целится в точку на земле, а не в юнит. "
               "В таком режиме работает только `areaDamage`"),
        theory("Полёт",
               "• `speed` — стартовая скорость; `targetSpeed` + `targetSpeedAcceleration` — разгон до крейсерской (ракеты)\n"
               "• `instant: true` — мгновенное попадание (лазеры, молнии); "
               "`instantReuseLast: true` — один и тот же луч на каждый кадр (лучевое оружие); "
               "`instantReuseLast_alsoChangeTurretAim` — турель учитывает разброс луча; `laserEffect` / `lightingEffect` — визуал луча и молнии "
               "(оба лучше всего смотрятся вместе с `instant: true`)\n"
               "• `ballistic: true` — баллистическая дуга; `ballistic_height` — высота дуги; `ballistic_delaymove_height` — задержка старта по высоте; "
               "1.13.3+: `initialUnguidedSpeedHeight` + `gravity` — навесные снаряды с честной гравитацией (для `targetGround`)\n"
               "• `targetGroundSpread` — разброс по площади (огнемёты, артиллерия); `speedSpread` — разброс стартовой скорости; "
               "`turnSpeed` — предел поворота в полёте (0 ведёт себя как `targetGround`, но бьёт и воздух)\n"
               "• `retargetingInFlight: true` — снаряд ищет новую цель прямо в полёте (флак, сталкивающиеся снаряды): "
               "`retargetingInFlightSearchDelay` — как часто искать, `retargetingInFlightSearchRange` — радиус поиска, "
               "`retargetingInFlightSearchLead` — упреждение, `retargetingInFlightSearchOnlyTags` — фильтр по тегам; "
               "`autoTargetingOnDeadTarget: true` — ретаргет, если цель умерла в полёте"),
        theory("Визуал",
               "• `drawType` — встроенные спрайты: 0 = `projectiles.png` (12 кадров), 1 = `projectiles_large.png` (3 кадра), 2 = `projectiles2.png` (6 кадров); "
               "`frame` — номер кадра, начинается с 0\n"
               "• `image` — свой спрайт (перекрывает `drawType` и `frame`); `drawSize` — масштаб (по умолчанию 1); `color` — перекраска по hex; `drawUnderUnits` — рисовать под юнитами (торпеды)\n"
               "• `trailEffect` — след: `true` для встроенного или `CUSTOM:имя`; `trailEffectRate` — частота следов (по умолчанию 3)\n"
               "• `lightCastOnGround` — свет на землю; `lightSize` — размер света (1 = 1 тайл); `lightColor` — цвет света; `largeHitEffect` — большой визуал и звук попадания; `explodeEffect` — свои эффекты взрыва; `explodeEffectOnShield` — визуал при попадании в щит; `hitSound` — звук попадания (по умолчанию true)\n"
               "• `nukeWeapon: true` — показывать на миникарте при пуске (и другие ядерные побочки); `shouldRevealFog` — раскрывать туман при взрыве; `alwaysVisibleInFog` — виден даже в тумане; `deflectionPower` — сколько энергии нужно лазерной защите для отклонения (-1 = нельзя отклонить, например огнемёт)"),
        theory("Спавны и превращения",
               "• `spawnUnit` — создать юнитов в точке взрыва: `spawnUnit: heavyTank, tank*5, hoverTank(offsetX=10)`\n"
               "• `spawnProjectilesOnExplode` — снаряды при попадании (кассеты); `spawnProjectilesOnEndOfLife` — снаряды в конце жизни (разделение); `spawnProjectilesOnCreate` — снаряды в момент создания (настоящий дробовик)\n"
               "• `convertHitToSourceTeam: true` — перекрашивать поражённые цели в команду стрелявшего (механика захвата)\n"
               "• `friendlyFire` — урон своим: `false`, `true` или `only-ignoreEnemy` (ядерное оружие)\n"
               "• `buildingDamageMultiplier` и `shieldDamageMultiplier` — множители урона по зданиям и щитам; `hullDamageMultiplier` — множитель по корпусу (0 = ЭМП по щитам); `shieldDefectionMultiplier` — пробой щита (0 = игнор щита и сразу корпус)\n"
               "• `mutator1_ifUnitWithTags` + `mutator1_directDamageMultiplier` — ситуативный урон по тегам цели; "
               "`pushForce` и `pushVelocity` — толчок поражённых целей (первый делится на массу цели, второй её игнорирует)"),
        code("Два снаряда: пуля и мина",
             "[projectile_shot]\n"
             "directDamage: 35\n"
             "life: 240\n"
             "speed: 7\n"
             "drawType: 0\n"
             "frame: 0\n"
             "color: #ffe92b\n"
             "trailEffect: true\n"
             "\n"
             "[projectile_mine]\n"
             "areaDamage: 60\n"
             "areaRadius: 40\n"
             "life: 4000\n"
             "targetGround: true\n"
             "explodeOnEndOfLife: true\n"
             "invisible: true",
             note="explodeOnEndOfLife взрывает снаряд в конце жизни — так делают мины и зоны."),
        quiz("Какой ключ задаёт размер области для areaDamage?",
             ["speed", "areaRadius", "drawType", "frame"], 1,
             explain="areaDamage бьёт по кругу, а areaRadius задаёт радиус этого круга."),
        quiz("Как сделать мгновенное попадание?",
             ["instant: true", "speed: 999", "life: 1", "targetGround: true"], 0,
             explain="instant: true попадает в цель сразу — идеально для лазеров."),
        practice("Допиши пулю: время жизни 240, скорость 6, цвет жёлтый",
                 "[projectile_shot]\n"
                 "directDamage: 35\n"
                 "___1___: 240\n"
                 "speed: ___2___\n"
                 "drawType: 0\n"
                 "___3___: #ffe92b",
                 {"1": "life", "2": "6", "3": "color"},
                 hint="Время жизни — life, цвет — color.",
                 explain="life подбирается под дальность: если снаряд исчезает раньше цели — увеличивай."),
    ],
)