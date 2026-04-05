import wx
from gui.menu_bar import create_menu_bar
from gui.main_window import MainPanel

class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='DataFitter')
        self.SetSize(1100, 900)
        self.Centre()
        create_menu_bar(self)
        self.panel = MainPanel(self)

if __name__ == '__main__':
    app = wx.App()
    window = MainWindow()
    window.Show()
    app.MainLoop()
