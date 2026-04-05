from scipy.stats import chi2
from scipy.optimize import curve_fit
from .functions import registry, equation_string, parameter_count
from numpy import ones, diag, sqrt

def run_fit(x, dx, y, dy, fit, initial_guess=None, n=0):
    if fit == 'polynomial':
        fit_type = registry[fit](n)
    else:
        fit_type = registry[fit]

    if initial_guess is None:
        if fit == 'polynomial':
            initial_guess = ones(n + 1)
        else:
            initial_guess = ones(parameter_count[fit])
    
    try:
        fit_params, cov_matrix = curve_fit(fit_type, x, y, initial_guess, dy)
        uncertainties = sqrt(diag(cov_matrix))
        y_fitted = fit_type(x, *fit_params)
        chi_squared = sum(((y - y_fitted) / dy) ** 2)
        dof = len(y) - len(fit_params)
        chi_squared_reduced = chi_squared / dof
        p_probability = chi2.sf(chi_squared, dof)

        results = {'fit_params': fit_params,
                'uncertainties': uncertainties,
                'y_fitted': y_fitted,
                'chi_squared': chi_squared,
                'dof': dof,
                'chi_squared_reduced': chi_squared_reduced,
                'p_probability': p_probability
        }
        
        return results
    except RuntimeError:
        return None
    