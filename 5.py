from lesson_base import lesson, theory, code, quiz, practice

LESSON = lesson(
    id=4,
    chapter="Базовые секции",
    title="[graphics] — внешность",
    subtitle="Картинки, тени и анимация",
    pages=[
        theory("Главная картинка",
               "Единственный обязательный ключ секции — `image: файл.png`. "
               "Это спрайт юнита.\n\n"
               "• `image_offsetX` / `image_offsetY` — сдвиг картинки, если она «съехала»\n"
               "• `image_wreak` — картинка обломков после смерти. `NONE` — без обломков\n"
               "• `image_back` — рисуется позади юнита (удобно для заводов)\n"
               "• `scaleImagesTo` / `imageScale` — масштаб изображения"),
        theory("Тени, цвет команды, кадры",
               "• `image_shadow: AUTO` — тень автоматически из основного спрайта\n"
               "• `teamColoringMode` — как зелёные пиксели красятся в цвет команды "
               "(по умолчанию `pureGreen`)\n"
               "• `total_frames: 4` — количество кадров анимации в спрайте "
               "(кадры режутся из одной картинки)\n"
               "• `drawLayer` — слой отрисовки: `ground`, `air`, `wreaks` и другие\n"
               "• `icon_build: icon.png` — иконка в меню строительства"),
        code("Внешность меха",
             "[graphics]\n"
             "image: mech.png\n"
             "image_wreak: mech_wreak.png\n"
             "image_shadow: AUTO\n"
             "total_frames: 4\n"
             "teamColoringMode: pureGreen\n"
             "dustEffect: true\n"
             "icon_build: mech_icon.png",
             note="dustEffect: true добавляет пыль при движении по земле."),
        quiz("Как убрать обломки после смерти юнита?",
             ["image_back: NONE", "image_wreak: NONE", "image: NONE", "hideScorchMark: false"], 1,
             explain="image_wreak отвечает за картинку обломков. NONE — ничего не рисовать."),
        practice("Настрой графику меха: картинка, обломки, автотень и 4 кадра анимации",
                 "[graphics]\n"
                 "___1___: mech.png\n"
                 "___2___: mech_wreak.png\n"
                 "image_shadow: ___3___\n"
                 "___4___: 4",
                 {"1": "image", "2": "image_wreak", "3": "AUTO", "4": "total_frames"},
                 hint="Для автоматической тени есть специальное значение.",
                 explain="AUTO делает тень прямо из основного спрайта — удобно и быстро."),
    ],
)