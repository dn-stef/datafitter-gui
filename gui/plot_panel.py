import wx
import matplotlib.pyplot as plt

class PlotTab(wx.Panel):
    def __init__(self, parent, button_label, show_legend=False):
        super().__init__(parent)
        self.button_label = button_label
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)
        self.show_legend = show_legend
        self.init_ui()


    def init_ui(self):
        title_input_label = wx.StaticText(self, label='Title:')
        self.title_input = wx.TextCtrl(self)
        title = wx.BoxSizer(wx.HORIZONTAL)
        title.Add(title_input_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        title.Add(self.title_input, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        x_input_label = wx.StaticText(self, label='X label:')
        self.x_input = wx.TextCtrl(self)
        x_title = wx.BoxSizer(wx.HORIZONTAL)
        x_title.Add(x_input_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        x_title.Add(self.x_input, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        y_input_label = wx.StaticText(self, label='Y label:')
        self.y_input = wx.TextCtrl(self)
        y_title = wx.BoxSizer(wx.HORIZONTAL)
        y_title.Add(y_input_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        y_title.Add(self.y_input, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.grid_checkbox = wx.CheckBox(self, label='Grid')
        self.plot_button = wx.Button(self, label=self.button_label)
        self.plot_button.Bind(wx.EVT_BUTTON, self.on_plot)
        checkbox_sizer = wx.BoxSizer(wx.HORIZONTAL)
        checkbox_sizer.Add(self.grid_checkbox, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        if self.show_legend:
            self.legend_checkbox = wx.CheckBox(self, label='Legend')
            checkbox_sizer.Add(self.legend_checkbox, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.main_sizer.Add(title, 0, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(x_title, 0, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(y_title, 0, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(checkbox_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.plot_button, 0, wx.EXPAND | wx.ALL, 5)

    def set_data(self, x, y, dx, dy, y_fitted=None, x_name='', y_name=''):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.y_fitted = y_fitted
        self.x_name = x_name
        self.y_name = y_name

    def on_plot(self, event, show=True):
        if not hasattr(self, 'x'):
            wx.MessageBox('No data loaded.', 'Error', wx.OK | wx.ICON_WARNING)
            return

        title = self.title_input.GetValue() or self.button_label.replace('Plot ', '').capitalize()
        x_label = self.x_input.GetValue() or self.x_name
        y_label = self.y_input.GetValue() or self.y_name
        grid = self.grid_checkbox.GetValue()

        self.fig, ax = plt.subplots()
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        if grid:
            ax.grid(True)

        if self.button_label == 'Plot data':
            ax.plot(self.x, self.y, 'o', markersize=4)
        elif self.button_label == 'Plot fit':
            ax.plot(self.x, self.y, 'o', markersize=4, label='Data')
            if self.y_fitted is not None:
                ax.plot(self.x, self.y_fitted, label='Fit')
            if hasattr(self, 'legend_checkbox') and self.legend_checkbox.GetValue():
                ax.legend()
        elif self.button_label == 'Plot residuals':
            if self.y_fitted is not None:
                residuals = self.y - self.y_fitted
                ax.errorbar(self.x, residuals, yerr=self.dy, fmt='o', capsize=3, markersize=3)
                ax.axhline(0, color='red', linestyle='--')

        if show:
            plt.show()