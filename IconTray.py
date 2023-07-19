import datetime
import PIL.Image
import pystray
import win32console
import win32gui
import win32api
import win32con

class IconTray:
    def __init__(self, root):
        self.root = root  # Save the 'root' instance as an attribute
        self.image = PIL.Image.open('pic/web.png')
        self.current_icon = 'web'
        
        self.console = win32console.GetConsoleWindow()
        win32gui.ShowWindow(self.console, 0)
        win32api.SetConsoleCtrlHandler(lambda x: True, True)
        
        self.icon = pystray.Icon("web", self.image)
        self.icon.menu = pystray.Menu(
            pystray.MenuItem('1', self.action, default=True, visible=False),
            pystray.MenuItem("open app", self.on_clicked),
            pystray.MenuItem("hide app", self.on_clicked),
            pystray.MenuItem("open console", self.on_clicked),
            pystray.MenuItem("hide console", self.on_clicked),
            pystray.MenuItem("Exit", self.on_clicked)
        )

    def on_clicked(self, icon, item):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if str(item) == "open console":
            win32gui.ShowWindow(self.console, win32con.SW_SHOW)
        elif str(item) == "hide console":
            win32gui.ShowWindow(self.console, 0)
            win32api.SetConsoleCtrlHandler(lambda x: True, True)
        elif str(item) == "open app":
            root.deiconify()
        elif str(item) == "hide app":
            root.withdraw()
        elif str(item) == "Exit":
            root.destroy()

    def change_icon(self, new_icon_path):
        self.icon.icon = PIL.Image.open(new_icon_path)
        self.current_icon = new_icon_path
        self.icon.update_menu()

    def action(self, icon, item):
        self.change_icon('pic/web.png')
        root.deiconify()