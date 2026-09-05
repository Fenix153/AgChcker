import os
import sys
import time
import threading
import webbrowser
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from pynput.keyboard import Controller, Key, KeyCode

APP_NAME = "AgChecker"
APP_VERSION = "v1.0.0"
CREATOR = "deztinny, Recorz"
GITHUB_URL = "https://github.com/Fenix153"

BG_MAIN = "#1B2540"
BG_SIDEBAR = "#141B30"
BG_CARD = "#243252"
BOX_BG = "#101828"
TEXT_MAIN = "#EAEEF7"
TEXT_MUTED = "#8D97B5"
TEXT_ON_BOX = "#C7D0E8"

ACCENT_OPTIONS = {
    "Синий": "#3B6FD9",
    "Голубой": "#2E9BC9",
    "Фиолетовый": "#6C5FC7",
}

LAUNCHER_PATHS = {
    "TLauncher": os.path.join(os.environ.get("APPDATA", ""), ".minecraft"),
    "Legacy Launcher": os.path.join(
        os.environ.get("APPDATA", ""), ".tlauncher", "legacy", "Minecraft", "game"
    ),
}


def darken(hex_color, factor=0.82):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (max(0, int(c * factor)) for c in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


METHODS = [
    (
        "Метод 1 (Everything)",
        '"size:2263|size:5266|size:6515|size:6770|size:6778|size:7016|size:7218|size:7803|'
        'size:7891|size:9327|size:10283|size:10605|size:10958|size:11554|size:16541|size:17308|'
        'size:17339|size:18180|size:18527|size:18587|size:18734|size:19266|size:20578|size:20583|'
        'size:20639|size:20883|size:21161|size:21234|size:21664|size:22036|size:22861|size:26247|'
        'size:27546|size:27809|size:28084|size:28439|size:29304|size:29567|size:30279|size:31549|'
        'size:31607|size:34449|size:34669|size:35971|size:35993|size:38149|size:39017|size:39321|'
        'size:40142|size:42782|size:47159|size:48242|size:50828|size:51212|size:52426|size:54088|'
        'size:59381|size:62782|size:65316|size:65486|size:65765|size:66659|size:67491|size:68794|'
        'size:69757|size:72334|size:74105|size:80751|size:88896|size:95530|size:98811|size:100523|'
        'size:100799|size:101297|size:101571|size:101703|size:102297|size:102733|size:103761|'
        'size:104954|size:105623|size:105672|size:112386|size:120640|size:138417|size:143006|'
        'size:143597|size:143600|size:147329|size:147873|size:151762|size:153937|size:156722|'
        'size:156779|size:166677|size:169718|size:173698|size:183634|size:183651|size:192156|'
        'size:202720|size:257482|size:263070|size:267746|size:274865|size:300286|size:334588|'
        'size:343169|size:350629|size:409616|size:410358|size:517248|size:519731|size:532826|'
        'size:539151|size:556494|size:597406|size:636621|size:640838|size:878781|size:925493|'
        'size:1077149|size:1165063|size:1181556|size:1444714|size:1471429|size:1569093|'
        'size:1822841|size:3113569|size:3425801|size:3541075|size:3541138|size:3642292|'
        'size:3684385|size:4642998|size:5630483|size:7052171|size:7059952|size:22258750|'
        'size:25704986|size:26179274|size:26691896 *.jar"',
    ),
    (
        "Метод 2 (Everything)",
        'size:9951744|size:24536064|size:15438336|size:6229504|size:6573056|size:7187456|'
        'size:7969792|size:1562249|size:1672329|size:1677449|size:1680521|size:147329|'
        'size:138351|size:202720|size:7788032|size:22885|size:23810|size:138351|size:147329|'
        'size:7988736|size:3711166|size:3697285|size:3712014|size:5641728|size:4413440|'
        'size:114974|size:111866|size:274865|size:1820884|size:5007380|size:6944256|'
        'size:5934592|size:2545664|size:2108662|size:1961742|size:3684385|size:5143837|'
        'size:4413440|size:116689|size:1968128|size:8011776|size:1883602|size:5918208|'
        'size:1897269|size:31445308|size:24390144|size:25158656|size:2023236|size:16836288|'
        'size:88065933|size:197933122|size:2258533|size:2305645|size:2372788|size:18764384|'
        'size:9400174|size:2363704|size:15445581|size:2373676|size:138351|size:7788032|'
        'size:22885|size:23810|size:7988736|size:3711166|size:3697285|size:3712014|'
        'size:5641728|size:4413440|size:111866|size:1820884|size:5007380|size:6944256|'
        'size:5934592|size:2545664|size:2108662|size:1961742|size:3684385|size:5143837|'
        'size:1968128|size:8011776|size:1883602|size:6533121|size:16629226|size:28107997|'
        'size:8249687|size:5524900|size:140200|size:132133|size:110439|size:6244043|'
        'size:6867367|size:43883|size:514855|size:479296|size:9530356|size:355527744|'
        'size:1819289|size:1897269|size:16855568|size:16964112|size:2023236|size:5918208|'
        'ssize:31445308|size:24390144|size:10657176|size:460288|size:19521024|size:15076480|'
        'size:7204864|size:1613824|size:1499136|size:1488896|size:9332326|size:9400174|'
        'size:10071288|size:9400174|size:10071288|Baritone|Nursultan',
    ),
    (
        "Метод 3 (клиенты)",
        'impact | wurst | bleachhack | aristois | huzuni | skillclient | inertia | ares | sigma | '
        'meteor | liquidbounce | nurik | nursultan | celestial | calestial | celka | expensive | '
        'neverhook | excellent | wexside | wildclient | minced | deadcode | akrien | jigsaw | '
        'future | jessica | dreampool | norules | konas | richclient | rusherhack | thunderhack | '
        'moonhack | doomsday | nightware | ricardo | extazyy | troxill | antileak | arbuz | .akr | '
        '.wex | dauntiblyat | rename_me_please | editme | takker | fuzeclient | wisefolder| '
        'flauncher | vec.dll | USBOblivion.exe | Feather | delta | venus | baritone | spambot | '
        'CleanCut | spam_bot | inventory_walk | player_highlighter | aimbot | freecam | '
        'bedrock_breaker_mode | viaversion | double_hotbar | elytra_swap | armor_hotswap | '
        'smart_moving | chest | savesearcher | topkautobuy | topkaautobuy | tweakeroo | '
        'mob_hitbox | librarian_trade_finder | sacurachorusfind | autoattack | entity_outliner | '
        'invmove | viabackwards | viarewind | viafabric | viaforge | viaproxy | vialoader | '
        'viamcp | hitbox | elytrahack | DiamondSim | ForgeHax | clientcommands | Control-Tweaks | '
        'SwingThroughGrass | CutThrough | Haruka |  NewLauncher | Blade | Hachclient | Inertia | '
        'Fluger | Exloader | CatLean  | .ctl',
    ),
    (
        "Метод 4 (Everything)",
        'size:30720 utf8content:net/minecraft/client/entity/player/ClientPlayerEntity|'
        'net/minecraft/util/math/AxisAlignedBB',
    ),
    (
        "Метод 5 (Everything)",
        'ext:jar size:21kb-10mb content:"l.png" content:"mcmod.info"',
    ),
    (
        "Метод 6 (Everything)",
        '.exe size:12mb-25mb',
    ),
]


def get_programs_dir():
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(sys.executable)
        external = os.path.join(exe_dir, "programs")
        if os.path.isdir(external) and os.listdir(external):
            return external
        bundled = os.path.join(getattr(sys, "_MEIPASS", exe_dir), "programs")
        if os.path.isdir(bundled):
            return bundled
        return external
    else:
        return os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "programs")


def get_icon_path():
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(sys.executable)
        external = os.path.join(exe_dir, "icon.ico")
        if os.path.isfile(external):
            return external
        bundled = os.path.join(getattr(sys, "_MEIPASS", exe_dir), "icon.ico")
        if os.path.isfile(bundled):
            return bundled
        return None
    else:
        local = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "icon.ico")
        return local if os.path.isfile(local) else None


def get_exe_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(sys.argv[0]))


APP_DIR = get_programs_dir()
EXE_DIR = get_exe_dir()
ICON_PATH = get_icon_path()
LOGS_DIR = os.path.join(EXE_DIR, "logs")
MINECRAFT_DIR = os.path.join(os.environ.get("APPDATA", ""), ".minecraft")


def ensure_folder(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError:
            pass


def get_programs():
    ensure_folder(APP_DIR)
    if not os.path.isdir(APP_DIR):
        return []
    files = [f for f in os.listdir(APP_DIR) if f.lower().endswith((".exe", ".lnk", ".bat"))]
    return sorted(files)


def clear_app_logs():
    if not os.path.isdir(LOGS_DIR):
        return
    for entry in os.listdir(LOGS_DIR):
        full_path = os.path.join(LOGS_DIR, entry)
        try:
            if os.path.isfile(full_path) or os.path.islink(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                for root, dirs, files in os.walk(full_path, topdown=False):
                    for f in files:
                        os.remove(os.path.join(root, f))
                    for d in dirs:
                        os.rmdir(os.path.join(root, d))
                os.rmdir(full_path)
        except OSError:
            pass


CHECK_EXCLUDED_CHARS = {"t", "l", "p", "e", "/"}

CHECK_SPECIAL_KEYS = [
    Key.f1, Key.f2, Key.f3, Key.f4, Key.f5, Key.f6,
    Key.f7, Key.f8, Key.f9, Key.f10, Key.f11, Key.f12,
    Key.space, Key.enter, Key.backspace, Key.tab, Key.caps_lock,
    Key.shift, Key.shift_r, Key.ctrl_l, Key.ctrl_r, Key.alt_l, Key.alt_r,
    Key.up, Key.down, Key.left, Key.right,
    Key.home, Key.end, Key.page_up, Key.page_down,
    Key.insert, Key.delete, Key.num_lock, Key.scroll_lock,
    Key.print_screen, Key.menu,
]


def build_check_keys():
    keys = []
    for c in "abcdefghijklmnopqrstuvwxyz0123456789":
        if c in CHECK_EXCLUDED_CHARS:
            continue
        keys.append((c.upper(), KeyCode.from_char(c)))
    for k in CHECK_SPECIAL_KEYS:
        keys.append((str(k).replace("Key.", ""), k))
    return keys


CHECK_KEYS = build_check_keys()


def run_keyboard_check(progress_callback, delay=0.05):
    controller = Controller()
    total = len(CHECK_KEYS)
    pressed = []
    failed = []
    for index, (label, key) in enumerate(CHECK_KEYS, start=1):
        try:
            controller.press(key)
            controller.release(key)
            pressed.append(label)
        except Exception:
            failed.append(label)
        time.sleep(delay)
        progress_callback(index, total, label)
    return pressed, failed


def launch(path):
    try:
        os.startfile(path)
    except Exception as e:
        messagebox.showerror("Ошибка запуска", f"Не удалось запустить:\n{path}\n\n{e}")


def open_folder(path, create=True):
    if create:
        ensure_folder(path)
    if not os.path.isdir(path):
        messagebox.showerror("Ошибка", f"Папка не найдена:\n{path}")
        return
    try:
        os.startfile(path)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть папку:\n{e}")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.accent = ACCENT_OPTIONS["Синий"]
        self.accent_hover = darken(self.accent)

        self.title(APP_NAME)
        self.geometry("900x600")
        self.minsize(760, 500)
        self.configure(fg_color=BG_MAIN)

        if ICON_PATH:
            try:
                self.iconbitmap(ICON_PATH)
            except Exception:
                pass

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()

        self.content = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")

        self.show_programs()


    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, corner_radius=0, width=220)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)

        title_row = ctk.CTkFrame(sidebar, fg_color="transparent")
        title_row.pack(anchor="w", padx=20, pady=(24, 30), fill="x")

        if ICON_PATH:
            try:
                logo_img = ctk.CTkImage(Image.open(ICON_PATH), size=(26, 26))
                ctk.CTkLabel(title_row, image=logo_img, text="").pack(side="left", padx=(0, 8))
            except Exception:
                pass

        ctk.CTkLabel(
            title_row, text=APP_NAME, font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT_MAIN
        ).pack(side="left")

        self.nav_buttons = {}
        nav_items = [
            ("programs", "🖥   Программы", self.show_programs),
            ("everything", "🔎   Everything", self.show_everything),
            ("check", "✅   Check", self.show_check),
            ("about", "ℹ️   О программе", self.show_about),
            ("settings", "⚙️   Настройки", self.show_settings),
        ]
        for key, label, command in nav_items:
            btn = ctk.CTkButton(
                sidebar,
                text=label,
                anchor="w",
                fg_color="transparent",
                hover_color=darken(BG_CARD, 0.9),
                text_color=TEXT_MAIN,
                font=ctk.CTkFont(size=14),
                height=42,
                corner_radius=8,
                command=command,
            )
            btn.pack(fill="x", padx=12, pady=4)
            self.nav_buttons[key] = btn

        version_label = ctk.CTkLabel(
            sidebar, text=APP_VERSION, font=ctk.CTkFont(size=11), text_color=TEXT_MUTED
        )
        version_label.pack(side="bottom", pady=16)

    def _set_active(self, key):
        for k, btn in self.nav_buttons.items():
            btn.configure(fg_color=self.accent if k == key else "transparent")

    def _clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def _page_header(self, text):
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=28, pady=(24, 10))
        ctk.CTkLabel(
            header, text=text, font=ctk.CTkFont(size=24, weight="bold"), text_color=TEXT_MAIN
        ).pack(side="left")
        return header


    def show_programs(self):
        self._set_active("programs")
        self._clear_content()

        header = self._page_header("Программы")
        ctk.CTkButton(
            header, text="🔄 Обновить", width=110, fg_color=BG_CARD, hover_color=darken(BG_CARD, 0.9),
            command=self.show_programs,
        ).pack(side="right")

        scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=28, pady=(0, 20))

        programs = get_programs()
        if not programs:
            ctk.CTkLabel(
                scroll,
                text="Программы не найдены.\nДобавь .exe / .lnk файлы в папку 'programs'\n"
                     "(вкладка «Настройки»)",
                font=ctk.CTkFont(size=13),
                text_color=TEXT_MUTED,
                justify="center",
            ).pack(pady=40)
            return

        columns = 3
        for col in range(columns):
            scroll.grid_columnconfigure(col, weight=1, uniform="programs")

        for index, name in enumerate(programs):
            full_path = os.path.join(APP_DIR, name)
            display_name = os.path.splitext(name)[0]

            row, col = divmod(index, columns)

            card = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=10, height=110)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            card.grid_propagate(False)
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                card, text=display_name, font=ctk.CTkFont(size=14, weight="bold"),
                text_color=TEXT_MAIN, wraplength=180, justify="center",
            ).grid(row=0, column=0, padx=16, pady=(18, 10), sticky="ew")

            ctk.CTkButton(
                card, text="Запустить", width=110, fg_color=self.accent, hover_color=self.accent_hover,
                command=lambda p=full_path: launch(p),
            ).grid(row=1, column=0, pady=(0, 16))


    def _bind_scroll_passthrough(self, widget, scrollable_frame):

        def _on_mousewheel(event):
            scrollable_frame._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        widget.bind("<MouseWheel>", _on_mousewheel)
        try:
            widget._textbox.bind("<MouseWheel>", _on_mousewheel)
        except AttributeError:
            pass

    def copy_text(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()

    def show_everything(self):
        self._set_active("everything")
        self._clear_content()
        self._page_header("Everything")

        scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=28, pady=(0, 20))

        for title, text in METHODS:
            card = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=10)
            card.pack(fill="x", pady=8)

            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=(12, 6))
            ctk.CTkLabel(
                row, text=title, font=ctk.CTkFont(size=14, weight="bold"), text_color=TEXT_MAIN
            ).pack(side="left")
            ctk.CTkButton(
                row, text="Скопировать", width=110, fg_color=self.accent, hover_color=self.accent_hover,
                command=lambda t=text: self.copy_text(t),
            ).pack(side="right")

            box = ctk.CTkTextbox(
                card, height=70, fg_color=BOX_BG, text_color=TEXT_ON_BOX,
                wrap="word", font=ctk.CTkFont(size=11),
            )
            box.pack(fill="x", padx=16, pady=(0, 14))
            box.insert("1.0", text)
            box.configure(state="disabled")
            self._bind_scroll_passthrough(box, scroll)

    def show_check(self):
        self._set_active("check")
        self._clear_content()
        self._page_header("Check")

        wrap = ctk.CTkFrame(self.content, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=28, pady=(0, 24))

        info_card = ctk.CTkFrame(wrap, fg_color=BG_CARD, corner_radius=10)
        info_card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(
            info_card,
            text="Нажимает по очереди все клавиши клавиатуры (кроме T, L, P, /, ESC, E),\n"
                 "чтобы проверить, не открывается ли где-то окно чит-клиента по горячей клавише.\n"
                 "Перед запуском переключись на окно Minecraft — клавиши идут в активное окно.",
            font=ctk.CTkFont(size=13), text_color=TEXT_MUTED, justify="left",
        ).pack(anchor="w", padx=20, pady=16)

        control_row = ctk.CTkFrame(wrap, fg_color="transparent")
        control_row.pack(fill="x", pady=(0, 12))

        status_label = ctk.CTkLabel(
            control_row, text="Готово к запуску", font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_MAIN,
        )
        status_label.pack(side="left")

        log_box = ctk.CTkTextbox(
            wrap, fg_color=BOX_BG, text_color=TEXT_ON_BOX, wrap="word",
            font=ctk.CTkFont(size=12),
        )
        log_box.pack(fill="both", expand=True, pady=(0, 12))
        log_box.configure(state="disabled")

        def log(line):
            log_box.configure(state="normal")
            log_box.insert("end", line + "\n")
            log_box.see("end")
            log_box.configure(state="disabled")

        def on_progress(index, total, label):
            self.after(0, lambda: status_label.configure(text=f"Нажато {index} из {total}: {label}"))
            self.after(0, lambda: log(f"[{index}/{total}] {label}"))

        def on_finish(pressed, failed):
            def _update():
                status_label.configure(text=f"Готово: нажато {len(pressed)} из {len(pressed) + len(failed)}")
                if failed:
                    log("Не нажались: " + ", ".join(failed))
                else:
                    log("Все клавиши успешно нажаты.")
                start_btn.configure(state="normal", text="Начать проверку")
            self.after(0, _update)

        def countdown(n):
            if n > 0:
                status_label.configure(text=f"Переключись на Minecraft… {n}")
                self.after(1000, lambda: countdown(n - 1))
            else:
                start_btn.configure(state="disabled", text="Идёт проверка…")
                log_box.configure(state="normal")
                log_box.delete("1.0", "end")
                log_box.configure(state="disabled")
                threading.Thread(
                    target=lambda: on_finish(*run_keyboard_check(on_progress)),
                    daemon=True,
                ).start()

        def start_check():
            countdown(3)

        start_btn = ctk.CTkButton(
            control_row, text="Начать проверку", width=160, fg_color=self.accent,
            hover_color=self.accent_hover, command=start_check,
        )
        start_btn.pack(side="right")

    def show_about(self):
        self._set_active("about")
        self._clear_content()
        self._page_header("О программе")

        wrap = ctk.CTkFrame(self.content, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=28, pady=(0, 24))

        info_card = ctk.CTkFrame(wrap, fg_color=BG_CARD, corner_radius=10)
        info_card.pack(fill="x", pady=6)

        lines = [
            (APP_NAME, APP_VERSION),
            ("Создатель:", CREATOR),
            ("Найдено программ:", str(len(get_programs()))),
        ]
        for label, value in lines:
            row = ctk.CTkFrame(info_card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=10)
            ctk.CTkLabel(row, text=label, text_color=TEXT_MUTED, font=ctk.CTkFont(size=13)).pack(
                anchor="w"
            )
            ctk.CTkLabel(
                row, text=value, text_color=TEXT_MAIN, font=ctk.CTkFont(size=13, weight="bold"),
                wraplength=680, justify="left",
            ).pack(anchor="w")

        link_row = ctk.CTkFrame(info_card, fg_color="transparent")
        link_row.pack(fill="x", padx=20, pady=(0, 16))
        ctk.CTkLabel(link_row, text="GitHub:", text_color=TEXT_MUTED, font=ctk.CTkFont(size=13)).pack(
            anchor="w"
        )
        link_btn = ctk.CTkButton(
            link_row, text=GITHUB_URL, fg_color="transparent", hover_color=darken(BG_CARD, 0.9),
            text_color=self.accent, anchor="w", font=ctk.CTkFont(size=13, weight="bold", underline=True),
            command=lambda: webbrowser.open(GITHUB_URL),
        )
        link_btn.pack(anchor="w")


    def show_settings(self):
        self._set_active("settings")
        self._clear_content()
        self._page_header("Настройки")

        wrap = ctk.CTkFrame(self.content, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=28, pady=(0, 24))

        card = ctk.CTkFrame(wrap, fg_color=BG_CARD, corner_radius=10)
        card.pack(fill="x", pady=6)

        def setting_row(parent, label_text):
            row = ctk.CTkFrame(parent, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=14)
            ctk.CTkLabel(
                row, text=label_text, font=ctk.CTkFont(size=14), text_color=TEXT_MAIN
            ).pack(side="left")
            return row


        row_theme = setting_row(card, "Тема")

        def on_theme_change(choice):
            self.accent = ACCENT_OPTIONS.get(choice, self.accent)
            self.accent_hover = darken(self.accent)
            self.show_settings()

        theme_menu = ctk.CTkOptionMenu(
            row_theme, values=list(ACCENT_OPTIONS.keys()), fg_color=self.accent,
            button_color=self.accent, button_hover_color=self.accent_hover, command=on_theme_change,
        )
        theme_menu.set([k for k, v in ACCENT_OPTIONS.items() if v == self.accent][0])
        theme_menu.pack(side="right")


        row_lang = setting_row(card, "Язык")
        lang_menu = ctk.CTkOptionMenu(
            row_lang, values=["Русский", "English"], fg_color=self.accent,
            button_color=self.accent, button_hover_color=self.accent_hover,
        )
        lang_menu.set("Русский")
        lang_menu.pack(side="right")


        row_vol = setting_row(card, "Громкость интерфейса")
        vol_value = ctk.CTkLabel(row_vol, text="100", text_color=TEXT_MUTED)
        vol_value.pack(side="right", padx=(10, 0))

        def on_vol(v):
            vol_value.configure(text=str(int(float(v))))

        vol_slider = ctk.CTkSlider(
            row_vol, from_=0, to=100, number_of_steps=100, command=on_vol,
            progress_color=self.accent, button_color=self.accent,
        )
        vol_slider.set(100)
        vol_slider.pack(side="right", fill="x", expand=True, padx=10)


        def folder_row(parent, label_text, path, create=True):
            row = ctk.CTkFrame(parent, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=14)
            ctk.CTkLabel(
                row, text=label_text, font=ctk.CTkFont(size=14), text_color=TEXT_MAIN
            ).pack(side="left")
            ctk.CTkButton(
                row, text="ОТКРЫТЬ", width=110, fg_color=self.accent, hover_color=self.accent_hover,
                command=lambda: open_folder(path, create=create),
            ).pack(side="right")


        row_mc = ctk.CTkFrame(card, fg_color="transparent")
        row_mc.pack(fill="x", padx=20, pady=14)
        ctk.CTkLabel(
            row_mc, text="Открыть путь к Minecraft", font=ctk.CTkFont(size=14), text_color=TEXT_MAIN
        ).pack(side="left")

        def open_selected_launcher():
            choice = launcher_menu.get()
            open_folder(LAUNCHER_PATHS.get(choice, MINECRAFT_DIR), create=False)

        ctk.CTkButton(
            row_mc, text="ОТКРЫТЬ", width=110, fg_color=self.accent, hover_color=self.accent_hover,
            command=open_selected_launcher,
        ).pack(side="right", padx=(8, 0))

        launcher_menu = ctk.CTkOptionMenu(
            row_mc, values=list(LAUNCHER_PATHS.keys()), fg_color=self.accent,
            button_color=self.accent, button_hover_color=self.accent_hover, width=150,
        )
        launcher_menu.set("TLauncher")
        launcher_menu.pack(side="right")

        folder_row(card, "Открыть путь к чекеру", EXE_DIR, create=False)
        folder_row(card, "Открыть папку с программами", APP_DIR, create=True)
        folder_row(card, "Открыть папку с логами", LOGS_DIR, create=True)


        row_clear = ctk.CTkFrame(card, fg_color="transparent")
        row_clear.pack(fill="x", padx=20, pady=14)
        ctk.CTkLabel(
            row_clear, text="Очистить логи и кэш AgChecker",
            font=ctk.CTkFont(size=14), text_color=TEXT_MAIN,
        ).pack(side="left")

        def on_clear_logs():
            if messagebox.askyesno(
                "Подтверждение",
                "Удалить содержимое папки логов AgChecker?\nЭто действие необратимо.",
            ):
                clear_app_logs()
                messagebox.showinfo("Готово", "Логи и кэш AgChecker очищены.")

        ctk.CTkButton(
            row_clear, text="ОЧИСТИТЬ", width=110, fg_color=self.accent, hover_color=self.accent_hover,
            command=on_clear_logs,
        ).pack(side="right")


if __name__ == "__main__":
    app = App()
    app.mainloop()
