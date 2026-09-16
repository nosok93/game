from lesson_base import lesson, theory, code, quiz, practice

LESSON = lesson(
    id=14,
    chapter="Продвинутые секции",
    title="[effect] и [animation]",
    subtitle="Визуальные эффекты и анимации",
    pages=[
        theory("Эффекты — это чисто визуал",
               "`[effect_имя]` создаёт визуальный объект, который живёт и исчезает. "
               "Урон они **не наносят** — за урон отвечают снаряды.\n"
               "Запуск: `spawnEffects: CUSTOM:имя`, `effectOnDeath`, `shoot_flame: CUSTOM:имя`.\n"
               "Счётчик `*5` создаёт сразу 5 штук: `CUSTOM:pieces*3`.\n\n"
               "• `life` — время жизни (по умолчанию 200); `lifeRandom` — случайный разброс времени жизни; `fadeOut` — плавное исчезание; `fadeInTime` — плавное появление; `alpha` — прозрачность 0–1 (значение выше 1 откладывает эффект `fadeOut`)\n"
               "• `image` — свой спрайт; `stripIndex` — встроенный набор (`effects`, `explode_big`, `flame`, `projectiles`…); "
               "`frameIndex` — конкретный кадр; `total_frames` + `animateFrameStart` / `animateFrameEnd` / `animateFrameSpeed` / `animateFramePingPong` / `animateFrameLooping` — покадровая анимация эффекта\n"
               "• `scaleFrom` / `scaleTo` — эффект растёт или сжимается; `color` — перекраска (лучше всего работать с чисто-белым спрайтом); `teamColorRatio` — подмешать цвет команды; `shadow` и `imageShadow` — тень"),
        theory("Движение эффектов и звук",
               "• `attachedToUnit: true` — эффект приклеен к создателю (выхлоп, трение)\n"
               "• `xSpeedRelative` / `ySpeedRelative` — скорость относительно источника; `xSpeedAbsolute` / `ySpeedAbsolute` — абсолютная скорость по карте; все четыре имеют `Random`-варианты для разброса; "
               "`xOffsetRelative` / `yOffsetAbsolute` и их `Random`-варианты — смещения старта; `hOffset` и `hSpeed` — высота и её скорость; `dirOffset` и `dirSpeed` — направление и вращение спрайта; `alwayStartDirAtZero` — игнорировать направление источника; `pivotOffset` — смещение оси вращения (поворачивает и дочерние элементы); `attachedToUnit` + `physics` + `physicsGravity` — падение и отскок (нужна высота); `atmospheric` — сопротивление воздуха и лёгкий ветер; `drawUnderUnits` — отрисовка под юнитами; `showInFog` — видно в тумане войны; `delayedStartTimer` — отложить появление; `alsoEmitEffects` / `alsoEmitEffectsOnDeath` / `ifSpawnFailsEmitEffects` — цепочки эффектов; `createWhenOffscreen` / `createWhenZoomedOut` / `createWhenOverLiquid` / `createWhenOverLand` / `spawnChance` — условия появления; `priority` — приоритет при перегрузке; `alsoPlaySound` — звук вместе с эффектом (громкость задаётся через двоеточие: `meow.wav:0.5`)"),
        theory("Анимации",
               "`[animation_имя]` проигрывает ключевые кадры для тела, рук и ног:\n"
               "`onActions: move` / `attack` / `idle` / `underConstruction` — запуск по событию; "
               "`blendIn` / `blendOut` — плавные переходы; `pingPong` — проигрывание вперёд-назад; "
               "`KeyframeTimeScale` — ускорить или замедлить всю анимацию разом; "
               "`direction_units`, `direction_strideX`, `direction_strideY`, `direction_starting` — переопределение параметров из `[graphics]` на время анимации.\n"
               "Ключевые кадры пишутся так: `имя_время: {параметры}` — "
               "`arm1_1s: {x: 4, dir: 20}`, `leg1_3s: {dir: 300}`, `body_4s: {frame: 4, scale: 0.5}`, `effect_2s: {name:CUSTOM:myExplode, x: 0, y: 5}`."),
        code("Эффект и анимация",
             "[effect_boost]\n"
             "life: 40\n"
             "image: flame.png\n"
             "attachedToUnit: true\n"
             "scaleFrom: 0.7\n"
             "scaleTo: 1.3\n"
             "fadeOut: true\n"
             "ySpeedRelative: 2\n"
             "alsoPlaySound: boost.ogg\n"
             "\n"
             "[animation_walk]\n"
             "onActions: move\n"
             "pingPong: true\n"
             "arm1_1s: {x: 4, dir: 20}\n"
             "arm1_2s: {x: -4, dir: -20}"),
        quiz("Наносит ли эффект [effect_имя] урон?",
             ["нет, эффект только визуальный", "да, всегда", "только по зданиям", "если задан color"], 0,
             explain="Урон — это снаряды. Эффекты — картинка и звук."),
        quiz("Как приклеить эффект к юниту, чтобы он двигался вместе с ним?",
             ["physics: true", "attachedToUnit: true", "fadeOut: true", "spawnChance: 1"], 1,
             explain="attachedToUnit привязывает эффект к создателю."),
        practice("Дым: свой спрайт, рост с 0.6 до 1.4, приклеен к юниту",
                 "[effect_smoke]\n"
                 "life: 60\n"
                 "___1___: smoke.png\n"
                 "scaleFrom: 0.6\n"
                 "___2___: 1.4\n"
                 "fadeOut: true\n"
                 "___3___: true",
                 {"1": "image", "2": "scaleTo", "3": "attachedToUnit"},
                 hint="Рост задаёт пара scaleFrom → scaleTo.",
                 explain="Ставь life как можно меньше — эффекты съедают производительность."),
    ],
)