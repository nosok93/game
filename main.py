import os
import re
import sys
import json
import importlib.util
from functools import partial

from kivy.config import Config

Config.set("graphics", "width", "480")
Config.set("graphics", "height", "860")

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex as hx

APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)

BG = hx("F4F6FB")
CARD = hx("FFFFFF")
INK = hx("1F2430")
MUTED = hx("6B7280")
PRIMARY = hx("2563EB")
PRIMARY_D = hx("1E40AF")
ACCENT = hx("D97706")
GREEN = hx("16A34A")
GREEN_D = hx("15803D")
GREEN_L = hx("86EFAC")
RED = hx("DC2626")
CODE_BG = hx("111827")
CODE_LN = hx("E5E7EB")
LINE_C = hx("E2E6EF")
OPT_BG = hx("EDF0F7")
OPT_SEL = hx("DBEAFE")
OK_BG = hx("DCFCE7")
BAD_BG = hx("FEE2E2")
BTN_GRAY = hx("E8EBF2")

_fonts = os.path.join(os.path.dirname(kivy.__file__), "data", "fonts")
_mono = os.path.join(_fonts, "RobotoMono-Regular.ttf")
if not os.path.exists(_mono):
    _mono = os.path.join(_fonts, "Roboto-Regular.ttf")
LabelBase.register(name="Mono", fn_regular=_mono, fn_bold=_mono)


def esc(s):
    return str(s).replace("[", "[[").replace("]", "]]")


def rich(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"[b]\1[/b]", s)
    s = re.sub(r"`([^`]+)`", r"[font=Mono][color=1D4ED8]\1[/color][/font]", s)
    return s


def norm(s):
    return re.sub(r"\s+", " ", s.strip())


class WrapLabel(Label):
    def __init__(self, **kw):
        kw.setdefault("markup", True)
        kw.setdefault("halign", "left")
        kw.setdefault("valign", "top")
        kw.setdefault("color", INK)
        kw.setdefault("font_size", dp(15))
        kw.setdefault("line_height", 1.25)
        super().__init__(**kw)
        self.size_hint_y = None
        self.bind(text=self._fit, font_size=self._fit, width=self._fit)
        Clock.schedule_once(self._fit, 0)

    def _fit(self, *a):
        self.text_size = (self.width, None)
        self.texture_update()
        self.height = self.texture_size[1] if self.texture else dp(12)


class Rounded:
    def _round(self, bg, radius, border=None):
        self._radius = radius
        with self.canvas.before:
            self._rc = Color(*bg)
            self._rr = RoundedRectangle(pos=self.pos, size=self.size, radius=[radius])
        if border:
            with self.canvas.after:
                Color(*border)
                self._rl = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, radius), width=1)
        else:
            self._rl = None
        self.bind(pos=self._rsync, size=self._rsync)

    def _rsync(self, *a):
        self._rr.pos = self.pos
        self._rr.size = self.size
        if self._rl:
            self._rl.rounded_rectangle = (self.x, self.y, self.width, self.height, self._radius)

    def set_bg(self, c):
        self._rc.rgba = c


class Card(Rounded, BoxLayout):
    def __init__(self, bg=CARD, radius=16, pad=dp(14), border=None, **kw):
        kw.setdefault("orientation", "vertical")
        kw.setdefault("spacing", dp(10))
        kw.setdefault("size_hint_y", None)
        super().__init__(**kw)
        self.padding = pad
        self._round(bg, radius, border)
        self.bind(minimum_height=self.setter("height"))


class RButton(Rounded, Button):
    def __init__(self, text="", bg=PRIMARY, radius=12, text_color=(1, 1, 1, 1), fs=dp(15), **kw):
        kw.setdefault("background_normal", "")
        kw.setdefault("background_down", "")
        kw.setdefault("background_color", (0, 0, 0, 0))
        super().__init__(text=text, color=text_color, bold=True, font_size=fs, **kw)
        self._round(bg, radius)

    def on_press(self):
        self._rc.a = 0.75

    def on_release(self):
        self._rc.a = 1.0


def code_markup(line):
    if not line.strip():
        return " "
    s = line.strip()
    if s.startswith("#"):
        return "[color=6B7280]%s[/color]" % esc(line)
    if s.startswith("[") and s.endswith("]"):
        return "[color=F59E0B][b]%s[/b][/color]" % esc(line)
    if ":" in line:
        k, _, v = line.partition(":")
        return "[color=7DD3FC]%s[/color][color=E5E7EB]:%s[/color]" % (esc(k), esc(v))
    return "[color=E5E7EB]%s[/color]" % esc(line)


def template_markup(line):
    parts = re.split(r"(___\\d+___)", line) if False else re.split(r"(___\\d+___)", line)
    out = []
    for p in re.split(r"(___\\d+___)", line):
        if not p:
            continue
        m = re.fullmatch(r"___(\d+)___", p)
        if m:
            out.append("[color=FBBF24][b]__%s__[/b][/color]" % m.group(1))
        else:
            out.append(code_markup(p))
    return "".join(out)


class CodeBlock(Card):
    def __init__(self, text, **kw):
        super().__init__(bg=CODE_BG, radius=14, pad=dp(12), spacing=dp(2), **kw)
        for ln in text.split("\n"):
            self.add_widget(WrapLabel(text=code_markup(ln), font_name="Mono",
                                      font_size=dp(13), color=CODE_LN, line_height=1.2))


class TemplateBlock(Card):
    def __init__(self, text, **kw):
        super().__init__(bg=CODE_BG, radius=14, pad=dp(12), spacing=dp(2), **kw)
        for ln in text.split("\n"):
            self.add_widget(WrapLabel(text=template_markup(ln), font_name="Mono",
                                      font_size=dp(13), color=CODE_LN, line_height=1.2))


class TrackFill(Rounded, Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._round(GREEN_L, dp(5))


class ProgressTrack(Rounded, BoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._round((1, 1, 1, 0.28), dp(7))
        self.fill = TrackFill(size_hint=(None, 1), width=0)
        self.add_widget(self.fill)


class ChapterLabel(BoxLayout):
    def __init__(self, text):
        super().__init__(size_hint_y=None, height=dp(36), padding=(dp(2), dp(16), 0, dp(2)))
        self.add_widget(WrapLabel(text="[b]%s[/b]" % esc(text.upper()), font_size=dp(12.5), color=MUTED))


class RoundedBadge(Rounded, BoxLayout):
    def __init__(self, bg=PRIMARY, **kw):
        kw.setdefault("size_hint", (None, None))
        kw.setdefault("size", (dp(46), dp(46)))
        super().__init__(**kw)
        self._round(bg, 14)


class LessonCard(Rounded, ButtonBehavior, BoxLayout):
    def __init__(self, app_ref, meta, done):
        super().__init__(orientation="horizontal", size_hint_y=None, height=dp(74),
                         padding=dp(12), spacing=dp(12))
        self._round(CARD, 16, border=LINE_C)
        self.app_ref = app_ref
        self.meta = meta
        badge = RoundedBadge(bg=GREEN if done else PRIMARY)
        num = meta["key"] if str(meta["key"]).isdigit() else "✦"
        badge.add_widget(Label(text=str(num), color=(1, 1, 1, 1), bold=True, font_size=dp(16)))
        self.add_widget(badge)
        col = BoxLayout(orientation="vertical", spacing=dp(2))
        t = Label(text=meta["title"], color=INK, bold=True, font_size=dp(15),
                  halign="left", valign="middle")
        s = Label(text=meta.get("subtitle", ""), color=MUTED, font_size=dp(12),
                  halign="left", valign="middle")
        for w in (t, s):
            w.bind(width=lambda inst, v: setattr(inst, "text_size", (inst.width, None)))
        col.add_widget(t)
        col.add_widget(s)
        self.add_widget(col)
        self.add_widget(Label(text="✓" if done else "›", color=GREEN if done else MUTED,
                              bold=True, font_size=dp(20), size_hint_x=None, width=dp(26)))

    def on_press(self):
        self._rc.a = 0.85

    def on_release(self):
        self._rc.a = 1.0
        self.app_ref.open_lesson(self.meta["key"])


class HomeScreen(Screen):
    def __init__(self, app_ref):
        super().__init__(name="home")
        self.app_ref = app_ref
        root = BoxLayout(orientation="vertical", padding=(dp(16), dp(16)), spacing=dp(10))
        head = Card(bg=PRIMARY, radius=20, pad=dp(18), spacing=dp(6))
        head.add_widget(WrapLabel(text="[b]RW SCRIPT[/b]", font_size=dp(26), color=(1, 1, 1, 1)))
        head.add_widget(WrapLabel(text="Интерактивный курс моддинга Rusted Warfare",
                                  font_size=dp(13), color=(0.85, 0.9, 1, 1)))
        row = BoxLayout(size_hint_y=None, height=dp(16), spacing=dp(10))
        self.prog_label = Label(text="", color=(1, 1, 1, 1), font_size=dp(12), bold=True,
                                size_hint_x=0.5, halign="left", valign="middle")
        self.prog_label.bind(size=lambda inst, v: setattr(inst, "text_size", inst.size))
        self.prog_track = ProgressTrack()
        row.add_widget(self.prog_label)
        row.add_widget(self.prog_track)
        head.add_widget(row)
        root.add_widget(head)
        self.list_box = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.list_box.bind(minimum_height=self.list_box.setter("height"))
        sv = ScrollView()
        sv.add_widget(self.list_box)
        root.add_widget(sv)
        self.add_widget(root)

    def refresh(self):
        lb = self.list_box
        lb.clear_widgets()
        lessons = self.app_ref.lessons
        done = self.app_ref.progress["done"]
        n_done = sum(1 for l in lessons if str(l["key"]) in done)
        self.prog_label.text = "Пройдено %d из %d" % (n_done, len(lessons))
        ratio = (n_done / len(lessons)) if lessons else 0

        def set_fill(*a):
            self.prog_track.fill.width = self.prog_track.width * ratio

        Clock.schedule_once(set_fill, 0)
        chapters = []
        for l in lessons:
            ch = l.get("chapter", "Мои уроки")
            if ch not in chapters:
                chapters.append(ch)
        for ch in chapters:
            lb.add_widget(ChapterLabel(ch))
            for l in lessons:
                if l.get("chapter", "Мои уроки") == ch:
                    lb.add_widget(LessonCard(self.app_ref, l, str(l["key"]) in done))


class LessonScreen(Screen):
    def __init__(self, app_ref):
        super().__init__(name="lesson")
        self.app_ref = app_ref
        outer = BoxLayout(orientation="vertical")
        self.top = BoxLayout(size_hint_y=None, height=dp(56), padding=(dp(12), dp(8)), spacing=dp(10))
        self.flash_slot = BoxLayout(orientation="vertical", size_hint_y=None,
                                    padding=(dp(14), dp(2), dp(14), dp(6)))
        self.flash_slot.bind(minimum_height=lambda inst, v: setattr(inst, "height", v + dp(8)))
        self.content = BoxLayout(orientation="vertical", size_hint_y=None,
                                 padding=(dp(16), dp(12)), spacing=dp(14))
        self.content.bind(minimum_height=self.content.setter("height"))
        self.sv = ScrollView()
        self.sv.add_widget(self.content)
        self.bottom = BoxLayout(size_hint_y=None, height=dp(64), padding=(dp(14), dp(10)), spacing=dp(10))
        outer.add_widget(self.top)
        outer.add_widget(self.flash_slot)
        outer.add_widget(self.sv)
        outer.add_widget(self.bottom)
        self.add_widget(outer)
        self.meta = None
        self.i = 0
        self.passed = set()
        self.quiz_sel = {}
        self.wrong_msg = {}
        self.pr_inputs = {}
        self.pr_text = {}
        self.feedback = {}

    def set_lesson(self, meta):
        self.meta = meta
        self.i = 0
        self.passed = set()
        self.quiz_sel = {}
        self.wrong_msg = {}
        self.pr_inputs = {}
        self.pr_text = {}
        self.feedback = {}
        self.flash_slot.clear_widgets()
        self.render()

    def render(self):
        self.render_top()
        self.content.clear_widgets()
        page = self.meta["pages"][self.i]
        t = page["type"]
        if t == "theory":
            self.render_theory(page)
        elif t == "code":
            self.render_code(page)
        elif t == "quiz":
            self.render_quiz(page)
        elif t == "practice":
            self.render_practice(page)
        self.build_bottom()
        Clock.schedule_once(lambda *a: setattr(self.sv, "scroll_y", 1), 0)

    def render_top(self):
        self.top.clear_widgets()
        back = RButton(text="<", bg=BTN_GRAY, text_color=INK, radius=12,
                       size_hint_x=None, width=dp(44), fs=dp(18))
        back.bind(on_release=lambda *a: self.app_ref.go_home())
        self.top.add_widget(back)
        t = Label(text=self.meta["title"], color=INK, bold=True, font_size=dp(16),
                  halign="left", valign="middle", shorten=True)
        t.bind(width=lambda inst, v: setattr(inst, "text_size", (inst.width, None)))
        self.top.add_widget(t)
        self.top.add_widget(Label(text="%d/%d" % (self.i + 1, len(self.meta["pages"])),
                                  color=MUTED, font_size=dp(13), bold=True,
                                  size_hint_x=None, width=dp(42)))

    def header(self, text):
        self.content.add_widget(WrapLabel(text="[b]%s[/b]" % esc(text), font_size=dp(20), color=INK))

    def render_theory(self, page):
        self.header(page.get("title", "Теория"))
        for block in page["text"].split("\n\n"):
            block = block.strip()
            if not block:
                continue
            if block.startswith("## "):
                self.content.add_widget(WrapLabel(text="[b]%s[/b]" % esc(block[3:]),
                                                  font_size=dp(16.5), color=PRIMARY_D))
            else:
                card = Card(pad=dp(14), spacing=dp(4))
                card.add_widget(WrapLabel(text=rich(block), font_size=dp(15), line_height=1.32))
                self.content.add_widget(card)

    def render_code(self, page):
        self.header(page.get("title", "Код"))
        self.content.add_widget(CodeBlock(page["code"]))
        if page.get("note"):
            self.content.add_widget(WrapLabel(text=rich(page["note"]), font_size=dp(13), color=MUTED))

    def feedback_label(self, idx):
        page = self.meta["pages"][idx]
        if idx in self.passed:
            l = WrapLabel(text=rich("**Верно!** " + page.get("explain", "")),
                          color=GREEN_D, font_size=dp(14), line_height=1.3)
        elif idx in self.wrong_msg:
            l = WrapLabel(text=esc(self.wrong_msg[idx]), color=RED, font_size=dp(14))
        else:
            l = WrapLabel(text="", font_size=dp(14))
        self.feedback[idx] = l
        return l

    def render_quiz(self, page):
        idx = self.i
        self.header("Проверь себя")
        self.content.add_widget(WrapLabel(text="[b]%s[/b]" % esc(page["question"]), font_size=dp(16)))
        box = Card(pad=dp(12), spacing=dp(8))
        sel = self.quiz_sel.get(idx)
        for n, opt in enumerate(page["options"]):
            bg, tc = OPT_BG, INK
            if idx in self.passed:
                if n == page["answer"]:
                    bg, tc = OK_BG, GREEN_D
                elif n == sel:
                    bg, tc = BAD_BG, RED
            elif sel == n:
                bg, tc = OPT_SEL, PRIMARY_D
            b = RButton(text=opt, bg=bg, text_color=tc, radius=12,
                        size_hint_y=None, height=dp(46), fs=dp(14))
            if idx not in self.passed:
                b.bind(on_release=partial(self.quiz_pick, idx, n))
            else:
                b.disabled = True
            box.add_widget(b)
        self.content.add_widget(box)
        self.content.add_widget(self.feedback_label(idx))

    def quiz_pick(self, idx, n, *a):
        self.quiz_sel[idx] = n
        self.wrong_msg.pop(idx, None)
        self.render()

    def render_practice(self, page):
        idx = self.i
        self.header("Практика")
        self.content.add_widget(WrapLabel(text=rich(page["task"]), font_size=dp(15), line_height=1.3))
        if page.get("hint"):
            self.content.add_widget(WrapLabel(text=rich("Подсказка: " + page["hint"]),
                                              font_size=dp(13), color=MUTED))
        self.content.add_widget(TemplateBlock(page["template"]))
        blanks = []
        for b in re.findall(r"___(\d+)___", page["template"]):
            if b not in blanks:
                blanks.append(b)
        box = Card(pad=dp(12), spacing=dp(8))
        self.pr_inputs[idx] = {}
        self.pr_text.setdefault(idx, {})
        for b in blanks:
            row = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(44))
            row.add_widget(Label(text=b + ".", color=ACCENT, bold=True, font_size=dp(15),
                                 size_hint_x=None, width=dp(30)))
            ti = TextInput(text=self.pr_text[idx].get(b, ""), multiline=False, write_tab=False,
                           font_size=dp(15), foreground_color=INK, cursor_color=PRIMARY,
                           background_normal="", background_active="",
                           background_color=(0.93, 0.95, 0.99, 1), padding=[dp(10), dp(10)])
            ti.bind(text=partial(self.pr_store, idx, b))
            if idx in self.passed:
                ti.readonly = True
            self.pr_inputs[idx][b] = ti
            row.add_widget(ti)
            box.add_widget(row)
        self.content.add_widget(box)
        if idx not in self.passed:
            wrap = BoxLayout(size_hint_y=None, height=dp(38))
            link = RButton(text="Показать ответ", bg=BTN_GRAY, text_color=MUTED,
                           radius=10, size_hint_x=0.55, fs=dp(13))
            link.bind(on_release=partial(self.show_answer, idx))
            wrap.add_widget(link)
            self.content.add_widget(wrap)
        self.content.add_widget(self.feedback_label(idx))

    def pr_store(self, idx, bid, inst, value):
        self.pr_text.setdefault(idx, {})[bid] = value

    def show_answer(self, idx, *a):
        page = self.meta["pages"][idx]
        for bid, ans in page["answers"].items():
            self.pr_inputs[idx][bid].text = ans
        self.flash("Ответ показан. Запомни и попробуй повторить!", ACCENT)

    def flash(self, msg, color=RED):
        self.flash_slot.clear_widgets()
        card = Card(bg=color, radius=12, pad=dp(10))
        card.add_widget(WrapLabel(text=esc(msg), font_size=dp(13.5), color=(1, 1, 1, 1)))
        self.flash_slot.add_widget(card)
        Clock.schedule_once(lambda *a: self.flash_slot.clear_widgets(), 2.6)

    def build_bottom(self):
        b = self.bottom
        b.clear_widgets()
        pages = self.meta["pages"]
        page = pages[self.i]
        last = self.i == len(pages) - 1
        back = RButton(text="Назад", bg=BTN_GRAY, text_color=INK, radius=12, fs=dp(14))
        back.bind(on_release=lambda *a: self.prev_page())
        if self.i == 0:
            back.disabled = True
            back.opacity = 0.35
        b.add_widget(back)
        if page["type"] in ("quiz", "practice") and self.i not in self.passed:
            chk = RButton(text="Проверить", radius=12, fs=dp(14))
            chk.bind(on_release=lambda *a: self.check())
            b.add_widget(chk)
        nxt = RButton(text="Завершить" if last else "Далее",
                      bg=GREEN if last else PRIMARY, radius=12, fs=dp(14))
        nxt.bind(on_release=lambda *a: (self.finish() if last else self.next_page()))
        b.add_widget(nxt)

    def check(self):
        page = self.meta["pages"][self.i]
        idx = self.i
        if page["type"] == "quiz":
            sel = self.quiz_sel.get(idx)
            if sel is None:
                self.flash("Сначала выбери вариант ответа")
                return
            if sel == page["answer"]:
                self.passed.add(idx)
                self.wrong_msg.pop(idx, None)
            else:
                self.wrong_msg[idx] = "Неверно. Подумай ещё раз!"
            self.render()
        else:
            inputs = self.pr_inputs.get(idx, {})
            wrong = []
            for bid, ans in page["answers"].items():
                ti = inputs.get(bid)
                if ti is None or norm(ti.text) != norm(ans):
                    wrong.append(bid)
            fb = self.feedback[idx]
            if not wrong:
                self.passed.add(idx)
                self.wrong_msg.pop(idx, None)
                fb.color = GREEN_D
                fb.text = rich("**Отлично, всё верно!** " + page.get("explain", ""))
                for ti in inputs.values():
                    ti.readonly = True
                self.build_bottom()
            else:
                fb.color = RED
                fb.text = "Ошибки в пропусках: " + ", ".join(wrong)

    def prev_page(self):
        if self.i > 0:
            self.i -= 1
            self.render()

    def next_page(self):
        if self.i < len(self.meta["pages"]) - 1:
            self.i += 1
            self.render()

    def finish(self):
        tasks = [n for n, p in enumerate(self.meta["pages"]) if p["type"] in ("quiz", "practice")]
        if all(t in self.passed for t in tasks):
            self.app_ref.mark_done(self.meta["key"])
            self.render_complete()
        else:
            left = len([t for t in tasks if t not in self.passed])
            self.flash("Осталось заданий: %d. Вернись и выполни их." % left)

    def render_complete(self):
        self.content.clear_widgets()
        card = Card(pad=dp(20), spacing=dp(12))
        card.add_widget(WrapLabel(text="[b]Урок пройден![/b]", font_size=dp(24), color=GREEN_D))
        card.add_widget(WrapLabel(text=rich("Отличная работа! Тема **«%s»** закрыта. Так держать!"
                                            % self.meta["title"]), font_size=dp(15), color=MUTED))
        self.content.add_widget(card)
        row = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        hb = RButton(text="К списку уроков", bg=BTN_GRAY, text_color=INK, radius=12, fs=dp(14))
        hb.bind(on_release=lambda *a: self.app_ref.go_home())
        row.add_widget(hb)
        nxt = self.app_ref.next_of(self.meta["key"])
        if nxt:
            nb = RButton(text="Следующий урок", bg=PRIMARY, radius=12, fs=dp(14))
            nb.bind(on_release=lambda *a: self.app_ref.open_lesson(nxt["key"]))
            row.add_widget(nb)
        self.content.add_widget(row)
        self.bottom.clear_widgets()
        Clock.schedule_once(lambda *a: setattr(self.sv, "scroll_y", 1), 0)


def discover_lessons():
    lessons = []
    skip = {"main.py", "lesson_base.py", "__init__.py"}
    for fn in sorted(os.listdir(APP_DIR)):
        if not fn.endswith(".py") or fn.lower() in skip:
            continue
        path = os.path.join(APP_DIR, fn)
        try:
            spec = importlib.util.spec_from_file_location("rw_lesson_" + fn[:-3], path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        except Exception as e:
            print("Урок не загрузился:", fn, e)
            continue
        data = getattr(mod, "LESSON", None)
        if not isinstance(data, dict) or "pages" not in data:
            continue
        data["key"] = fn[:-3]
        data.setdefault("chapter", "Мои уроки")
        data.setdefault("subtitle", "")
        lessons.append(data)

    def order(l):
        k = str(l["key"])
        return (0, int(k)) if k.isdigit() else (1, k)

    lessons.sort(key=order)
    return lessons


class RWScriptApp(App):
    def build(self):
        Window.clearcolor = BG
        self.title = "RW Script — курс моддинга"
        self.progress_file = os.path.join(self.user_data_dir, "progress.json")
        self.lessons = discover_lessons()
        self.progress = self.load_progress()
        self.sm = ScreenManager(transition=SlideTransition(duration=0.25))
        self.home = HomeScreen(self)
        self.ls = LessonScreen(self)
        self.sm.add_widget(self.home)
        self.sm.add_widget(self.ls)
        self.home.refresh()
        return self.sm

    def load_progress(self):
        try:
            with open(self.progress_file, "r", encoding="utf-8") as f:
                d = json.load(f)
                d.setdefault("done", [])
                return d
        except Exception:
            return {"done": []}

    def save_progress(self):
        try:
            with open(self.progress_file, "w", encoding="utf-8") as f:
                json.dump(self.progress, f, ensure_ascii=False)
        except Exception:
            pass

    def mark_done(self, key):
        k = str(key)
        if k not in self.progress["done"]:
            self.progress["done"].append(k)
            self.save_progress()

    def open_lesson(self, key):
        meta = next((l for l in self.lessons if str(l["key"]) == str(key)), None)
        if not meta:
            return
        self.ls.set_lesson(meta)
        self.sm.transition.direction = "left"
        self.sm.current = "lesson"

    def go_home(self):
        self.home.refresh()
        self.sm.transition.direction = "right"
        self.sm.current = "home"

    def next_of(self, key):
        keys = [str(l["key"]) for l in self.lessons]
        i = keys.index(str(key))
        return self.lessons[i + 1] if i + 1 < len(self.lessons) else None


if __name__ == "__main__":
    RWScriptApp().run()