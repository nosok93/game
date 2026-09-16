from lesson_base import lesson, theory, code, quiz, practice

LESSON = lesson(
    id=6,
    chapter="Базовые секции",
    title="[turret_NAME] — турели",
    subtitle="Стволы, задержки и поворот",
    pages=[
        theory("Что такое турель",
               "Турель — это точка, из которой вылетают снаряды. У юнита может быть "
               "**до 30 турелей**: `[turret_1]`, `[turret_2]`, `[turret_gun]`.\n\n"
               "Обязательных ключей всего два: `x` и `y` — позиция турели на спрайте "
               "(0 — центр, плюсы вправо/вверх).\n\n"
               "• `projectile: shot` — каким снарядом стреляет (ссылка на `[projectile_shot]`)\n"
               "• `delay: 1s` — пауза между выстрелами (переопределяет общий `shootDelay`)\n"
               "• `size` — длина ствола: откуда именно вылетает снаряд"),
        theory("Поворот и особые режимы",
               "• `turnSpeed` — скорость поворота турели; "
               "`turnSpeedAcceleration` — плавный разгон поворота (по умолчанию сразу полная скорость)\n"
               "• `idleDir` — направление турели в покое; `shouldResetTurret: false` — не возвращаться в него после боя; "
               "`limitingAngle` — сектор обстрела относительно `idleDir`\n"
               "• `limitingRange` / `limitingMinRange` — потолок и минималка дальности именно этой турели "
               "(не ставь на все турели — меняй `maxAttackRange`)\n"
               "• `attachedTo` — прикрепить турель к другой; `slave: true` — синхронизировать направление и перезарядку\n"
               "• `idleSpin` — вращение в покое, как у ракетных установок; `invisible: true` — скрыть турель, но оставить выстрел"),
        theory("Выстрел и ресурсы",
               "• `shoot_sound` — звук выстрела: встроенный (`tank_firing`, `missile_fire`, `gun_fire`, `plasma_fire`…) или свой файл `ROOT:audio/shoot.ogg`\n"
               "• `shoot_flame` — вспышка: `small`, `large`, `smoke`, `shockwave` или `CUSTOM:имя_эффекта`\n"
               "• `recoilOffset` + `recoilOutTime` + `recoilReturnTime` — отдача ствола в пикселях и время возврата; "
               "`barrelOffsetX_onOddShots` — сдвиг ствола на нечётных выстрелах (двустволки)\n"
               "• `energyUsage` — энергия за выстрел; `resourceUsage: credits=5, ammo=1` — любые ресурсы "
               "(если не хватает — стрелять не будет)\n"
               "• `warmup` — разгон перед выстрелом; `warmupCallDownRate`, `warmupNoReset`, `warmupShootDelayTransfer` — "
               "настройка разгона и переноса задержки; `chargeEffectImage` — эффект заряжания; `onShoot_playAnimation` / `onShoot_triggerActions` — что запустить при выстреле; "
               "`showShotDelayBar` в `[graphics]` — полоска разгона в интерфейсе"),
        theory("ПВО, лазер и строители",
               "• `interceptProjectiles_withTags: nuke` — перехват снарядов с меткой (анти-нук); "
               "`interceptProjectiles_andUnderDistance` / `interceptProjectiles_andTargetingGroundUnderDistance` — условия перехвата по дистанции; "
               "`interceptProjectiles_andOverHeight` — по высоте цели; `laserDefenceEnergyUse` — лазерная защита (нужен `energyMax` в `[core]`)\n"
               "• `isMainNanoTurret: true` — турель для строительства (обычно `canShoot: false`; должна быть одна такая)\n"
               "• `altProjectile` + `altProjectileCondition` — альтернативный снаряд по логическому условию; "
               "`aimOffsetSpread` на уровне турели — разброс; `clearTurretTargetAfterFiring` — сброс подцели при мульти-таргетинге"),
        code("Турель для танка",
             "[turret_1]\n"
             "x: 0\n"
             "y: 6\n"
             "projectile: shot\n"
             "delay: 0.9s\n"
             "turnSpeed: 5\n"
             "size: 9\n"
             "shoot_sound: gun_fire\n"
             "shoot_flame: small\n"
             "recoilOffset: 3\n"
             "recoilReturnTime: 0.3s"),
        quiz("Какие два ключа обязательны в любой турели?",
             ["x и y", "delay", "projectile", "image"], 0,
             explain="Без координат игра не знает, где находится турель."),
        practice("Турель в точке (0, 6), стреляет снарядом `shot`, скорость поворота 3",
                 "[turret_1]\n"
                 "___1___: 0\n"
                 "___2___: 6\n"
                 "projectile: ___3___\n"
                 "delay: 1.2s\n"
                 "___4___: 3\n"
                 "size: 8",
                 {"1": "x", "2": "y", "3": "shot", "4": "turnSpeed"},
                 hint="Позиция — это координаты, скорость поворота — turnSpeed.",
                 explain="projectile: shot ищет в файле секцию [projectile_shot]."),
    ],
)