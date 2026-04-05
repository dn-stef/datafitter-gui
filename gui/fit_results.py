import wx

class FitResultsDialog(wx.Dialog):
    def __init__(self, parent, results, initial_guesses):
        super().__init__(parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)
        self.results = results
        self.initial_guesses = initial_guesses
        self.init_ui()

    def init_ui(self):
            results_title = wx.StaticText(self, label='Results:')
            results_title_underscore = wx.StaticText(self, label='========')
            initial_guesses_title = wx.StaticText(self, label='Initial parameters:')
            initial_guesses = wx.StaticText(self, label=' '.join(str(v) for v in self.initial_guesses))
            fitted_params_title = wx.StaticText(self, label='Fitted parameters:')
            chi_squared_title = wx.StaticText(self, label=f'Chi squared: {self.results["chi_squared"]:.3f}')
            dof_title = wx.StaticText(self, label=f'Degrees of freedom: {self.results["dof"]}')
            chi_squared_red_title = wx.StaticText(self, label=f'Chi squared reduced: {self.results["chi_squared_reduced"]:.3f}')
            p_prob_title = wx.StaticText(self, label=f'P-probability: {self.results["p_probability"]:.3f}')
            close_button = wx.Button(self, wx.ID_OK, label='Close')

            self.main_sizer.Add(results_title, 0, wx.ALL, 5)
            self.main_sizer.Add(results_title_underscore, 0, wx.ALL, 5)
            self.main_sizer.Add(initial_guesses_title, 0, wx.ALL, 5)
            self.main_sizer.Add(initial_guesses, 0, wx.ALL, 5)
            self.main_sizer.Add(fitted_params_title, 0, wx.ALL, 5)

            for i, (param, uncertainty) in enumerate(zip(self.results['fit_params'], self.results['uncertainties'])):
                pct_error = (uncertainty / abs(param)) * 100
                param_label = wx.StaticText(self, label=f'a[{i}] = {param:.3f} +- {uncertainty:.3f} ({pct_error:.3f}% error)')
                self.main_sizer.Add(param_label, 0, wx.ALL, 5)

            self.main_sizer.Add(chi_squared_title, 0, wx.ALL, 5)
            self.main_sizer.Add(dof_title, 0, wx.ALL, 5)
            self.main_sizer.Add(chi_squared_red_title, 0, wx.ALL, 5)
            self.main_sizer.Add(p_prob_title, 0, wx.ALL, 5)
            self.main_sizer.Add(close_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)

            self.main_sizer.Fit(self)