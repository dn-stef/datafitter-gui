import wx
from gui.plot_panel import PlotTab
from gui.fit_results import FitResultsDialog
from data.loader import load_file, get_columns
from fitting.functions import equation_string, parameter_count
from fitting.engine import run_fit
from output.exporter import save_plots, save_stats

class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)
        self.df = None
        self.output_dir_path = None
        self.results = None
        self.initial_guesses = None
        self.init_ui()
    
    def init_ui(self):
        bitmap = wx.Image('assets/datafittergui.png', wx.BITMAP_TYPE_PNG).Scale(320, 150).ConvertToBitmap()
        widget = wx.StaticBitmap(self, bitmap=bitmap)
        self.main_sizer.Add(widget, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        input_file_label = wx.StaticText(self, label='Input file:')
        self.input_file_path = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.input_file_button = wx.Button(self, label='Choose file')
        self.input_file_button.Bind(wx.EVT_BUTTON, self.on_choose_file)
        input_file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        input_file_sizer.Add(input_file_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        input_file_sizer.Add(self.input_file_path, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        input_file_sizer.Add(self.input_file_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.main_sizer.Add(input_file_sizer, 0, wx.EXPAND | wx.ALL, 5)

        x_column_label = wx.StaticText(self, label='X column:')
        self.x_column_dropdown = wx.Choice(self, choices=[])
        self.x_column_dropdown.Bind(wx.EVT_CHOICE, self.on_column_change)
        x_error_column_label = wx.StaticText(self, label='X error column:')
        self.x_error_column_dropdown = wx.Choice(self, choices=[])
        self.x_error_column_dropdown.Bind(wx.EVT_CHOICE, self.on_column_change)
        y_column_label = wx.StaticText(self, label='Y column:')
        self.y_column_dropdown = wx.Choice(self, choices=[])
        self.y_column_dropdown.Bind(wx.EVT_CHOICE, self.on_column_change)
        y_error_column_label = wx.StaticText(self, label='Y error column:')
        self.y_error_column_dropdown = wx.Choice(self, choices=[])
        self.y_error_column_dropdown.Bind(wx.EVT_CHOICE, self.on_column_change)
        column_sizer = wx.BoxSizer(wx.HORIZONTAL)
        column_sizer.Add(x_column_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        column_sizer.Add(self.x_column_dropdown, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        column_sizer.Add(x_error_column_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        column_sizer.Add(self.x_error_column_dropdown, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        column_sizer.Add(y_column_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        column_sizer.Add(self.y_column_dropdown, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        column_sizer.Add(y_error_column_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        column_sizer.Add(self.y_error_column_dropdown, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.main_sizer.Add(column_sizer, 0, wx.EXPAND | wx.ALL, 5)

        fit_label = wx.StaticText(self, label='Fitting function:')
        self.fit_type = wx.Choice(self, choices=['-------', 'constant', 'linear', 'polynomial',
                                                 'straight_power', 'inverse_power', 'hyperbolic',
                                                 'exponential', 'sin', 'cos', 'normal', 'poisson'])
        self.fit_type.Bind(wx.EVT_CHOICE, self.on_fit_type_change)
        self.degree_label = wx.StaticText(self, label='Degree:')
        self.degree_label.Hide()
        self.degree_spinner = wx.SpinCtrl(self, min=1, max=5)
        self.degree_spinner.Hide()
        self.degree_spinner.Bind(wx.EVT_SPINCTRL, self.on_degree_change)
        self.equation_field = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.fit_button = wx.Button(self, label='Fit')
        self.fit_button.Bind(wx.EVT_BUTTON, self.on_fit)
        self.fit_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.fit_sizer.Add(fit_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.fit_sizer.Add(self.fit_type, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.fit_sizer.Add(self.degree_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.fit_sizer.Add(self.degree_spinner, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.fit_sizer.Add(self.equation_field, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        self.fit_sizer.Add(self.fit_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.main_sizer.Add(self.fit_sizer, 0, wx.EXPAND | wx.ALL, 5)

        guess_label = wx.StaticText(self, label='Initial guess:')
        self.guess_labels = []
        self.guess_fields = []
        self.guess_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.guess_sizer.Add(guess_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        for i in range(6):
            label = wx.StaticText(self, label=f'a[{i}]:')
            field = wx.TextCtrl(self, size=(60, -1))
            if i > 0:
                label.Hide()
                field.Hide()
            self.guess_labels.append(label)
            self.guess_fields.append(field)
            self.guess_sizer.Add(label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
            self.guess_sizer.Add(field, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.main_sizer.Add(self.guess_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        notebook = wx.Notebook(self)
        self.plot_data_tab = PlotTab(notebook, "Plot data")
        notebook.AddPage(self.plot_data_tab, "Data")
        self.plot_fit_tab = PlotTab(notebook, "Plot fit", show_legend=True)
        notebook.AddPage(self.plot_fit_tab, "Fit")
        self.plot_residuals_tab = PlotTab(notebook, "Plot residuals")
        notebook.AddPage(self.plot_residuals_tab, "Residuals")
        self.main_sizer.Add(notebook, 1, wx.EXPAND | wx.ALL, 5)

        output_directory_label = wx.StaticText(self, label="Output directory:")
        self.output_directory = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.choose_directory_button = wx.Button(self, label="Choose directory")
        self.choose_directory_button.Bind(wx.EVT_BUTTON, self.on_choose_directory)
        self.save_button = wx.Button(self, label="Save")
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)
        output_sizer = wx.BoxSizer(wx.HORIZONTAL)
        output_sizer.Add(output_directory_label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        output_sizer.Add(self.output_directory, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        output_sizer.Add(self.choose_directory_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        output_sizer.Add(self.save_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.main_sizer.Add(output_sizer, 0, wx.EXPAND | wx.ALL, 5)

    def update_guess_fields(self, n_params):
        for i in range(6):
            if i < n_params:
                self.guess_labels[i].Show()
                self.guess_fields[i].Show()
            else:
                self.guess_labels[i].Hide()
                self.guess_fields[i].Hide()
        self.guess_sizer.Layout()
    
    def on_fit_type_change(self, event):
        current_fit = self.fit_type.GetStringSelection()
        if current_fit == '-------':
            return
        if current_fit == 'polynomial':
            self.degree_label.Show()
            self.degree_spinner.Show()
            degree = self.degree_spinner.GetValue()
            self.update_guess_fields(degree + 1)
            self.equation_field.SetValue(self.get_polynomial_equation(degree))
        else:
            self.degree_label.Hide()
            self.degree_spinner.Hide()
            self.update_guess_fields(parameter_count[current_fit])
            self.equation_field.SetValue(equation_string[current_fit])
        self.fit_sizer.Layout()

    def on_degree_change(self, event):
        degree = self.degree_spinner.GetValue()
        self.update_guess_fields(degree + 1)
        self.equation_field.SetValue(self.get_polynomial_equation(degree))

    def update_plot_data(self, x, y, dx, dy, y_fitted=None):
        x_name = self.x_column_dropdown.GetStringSelection()
        y_name = self.y_column_dropdown.GetStringSelection()
        self.plot_data_tab.set_data(x, y, dx, dy, y_fitted, x_name, y_name)
        self.plot_fit_tab.set_data(x, y, dx, dy, y_fitted, x_name, y_name)
        self.plot_residuals_tab.set_data(x, y, dx, dy, y_fitted, x_name, y_name)

    def get_polynomial_equation(self, degree):
        terms = ['a[0]']
        for i in range(1, degree + 1):
            if i == 1:
                terms.append(f'a[1] * x')
            else:
                terms.append(f'a[{i}] * x ^ {i}')
        return ' + '.join(terms)

    def on_fit(self, event):
        if self.df is None:
            wx.MessageBox('Please load a data file first.', 'No data', wx.OK | wx.ICON_WARNING)
            return
        selected_fit = self.fit_type.GetStringSelection()
        if selected_fit == '-------':
            wx.MessageBox('Please select a fit type first.', 'No fit selected', wx.OK | wx.ICON_WARNING)
            return
        x = self.df[self.x_column_dropdown.GetStringSelection()]
        dx = self.df[self.x_error_column_dropdown.GetStringSelection()]
        y = self.df[self.y_column_dropdown.GetStringSelection()]
        dy = self.df[self.y_error_column_dropdown.GetStringSelection()]
        if selected_fit == 'polynomial':
            degree = self.degree_spinner.GetValue()
        else:
            degree = 0
        self.initial_guesses = []
        for field in self.guess_fields:
            if field.IsShown():
                value = field.GetValue()
                self.initial_guesses.append(float(value) if value else 1.0)
        results = run_fit(x, dx, y, dy, selected_fit, self.initial_guesses, degree)
        if results is None:
            wx.MessageBox('Fit failed to converge. Try different initial guesses.', 'Fit Error', wx.OK | wx.ICON_ERROR)
            return

        self.results = results

        self.update_plot_data(x, y, dx, dy, results['y_fitted'])

        dialog = FitResultsDialog(self, results, self.initial_guesses)
        dialog.ShowModal()

    def on_choose_file(self, event):
        file_dialog = wx.FileDialog(self, message="Choose a file", wildcard='All supported files (*.csv;*.xlsx)|*.csv;*.xlsx|CSV files (*.csv)|*.csv|Excel files (*.xlsx)|*.xlsx',
                                    style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) 
        if file_dialog.ShowModal() == wx.ID_OK:
            self.reset_ui()
            path = file_dialog.GetPath()
            self.input_file_path.SetValue(path)
            file = load_file(path)
            self.df = file
            columns = get_columns(file)
            self.x_column_dropdown.Clear()
            self.x_column_dropdown.AppendItems(columns)
            self.x_column_dropdown.SetSelection(0)
            self.x_error_column_dropdown.Clear()
            self.x_error_column_dropdown.AppendItems(columns)
            self.x_error_column_dropdown.SetSelection(1)
            self.y_column_dropdown.Clear()
            self.y_column_dropdown.AppendItems(columns)
            self.y_column_dropdown.SetSelection(2)
            self.y_error_column_dropdown.Clear()
            self.y_error_column_dropdown.AppendItems(columns)
            self.y_error_column_dropdown.SetSelection(3)
        
            self.update_plot_data(
                self.df[self.x_column_dropdown.GetStringSelection()],
                self.df[self.y_column_dropdown.GetStringSelection()],
                self.df[self.x_error_column_dropdown.GetStringSelection()],
                self.df[self.y_error_column_dropdown.GetStringSelection()]
            )
        
    def reset_ui(self):
            self.equation_field.SetValue('')
            for field in self.guess_fields:
                field.SetValue('')
            self.results = None
            self.initial_guesses = None
            self.degree_label.Hide()
            self.degree_spinner.Hide()
            self.fit_type.SetSelection(0)
            self.update_guess_fields(1)
            self.fit_sizer.Layout()

    def on_choose_directory(self, event):
        dir_dialog = wx.DirDialog(self, message="Choose a directory",
                                    style=wx.DD_DEFAULT_STYLE)
        if dir_dialog.ShowModal() == wx.ID_OK:
            path = dir_dialog.GetPath()
            self.output_directory.SetValue(path)
            self.output_dir_path = path

    def on_save(self, event):
        if self.output_dir_path is None:
            wx.MessageBox('Please choose an output directory before saving.', 'Output Directory Not Set', wx.OK | wx.ICON_WARNING)
            return
        
        if self.results is None:
            wx.MessageBox('No fit results to save.', 'No results', wx.OK | wx.ICON_WARNING)
            return

        self.plot_data_tab.on_plot(None, show=False)
        self.plot_fit_tab.on_plot(None, show=False)
        self.plot_residuals_tab.on_plot(None, show=False)

        figures = {}
        if hasattr(self.plot_data_tab, 'fig'):
            figures['data'] = self.plot_data_tab.fig
        if hasattr(self.plot_fit_tab, 'fig'):
            figures['fit'] = self.plot_fit_tab.fig
        if hasattr(self.plot_residuals_tab, 'fig'):
            figures['residuals'] = self.plot_residuals_tab.fig

        save_plots(figures, self.output_dir_path)
        save_stats(self.results, self.output_dir_path, self.fit_type.GetStringSelection())
        wx.MessageBox('Saved successfully.', 'Saved', wx.OK | wx.ICON_INFORMATION)

    def on_about(self, event):
        wx.MessageBox(
            'DataFitter\n\n'
            'A desktop GUI application for curve fitting and data visualization.\n\n'
            'Author: Daniel Stefanian\n'
            'GitHub: https://github.com/dn-stef',
            'About DataFitter',
            wx.OK | wx.ICON_INFORMATION
        )

    def on_font_change(self, size):
        sizes = {'small': 7, 'medium': 9, 'large': 12}
        font = wx.Font(sizes[size], wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        for child in self.GetChildren():
            child.SetFont(font)
        self.Layout()
        self.Refresh()
        self.Update()

    def on_fit_result(self, event):
        if self.df is None:
            wx.MessageBox('Please load a data file first.', 'No data', wx.OK | wx.ICON_WARNING)
            return
        if self.fit_type.GetStringSelection() == '-------':
            wx.MessageBox('Please select a fit type first.', 'No fit selected', wx.OK | wx.ICON_WARNING)
            return
        self.on_fit(event)

    def on_column_change(self, event):
        if self.df is None:
            return
        self.update_plot_data(
            self.df[self.x_column_dropdown.GetStringSelection()],
            self.df[self.y_column_dropdown.GetStringSelection()],
            self.df[self.x_error_column_dropdown.GetStringSelection()],
            self.df[self.y_error_column_dropdown.GetStringSelection()]
        )