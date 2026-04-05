import matplotlib.pyplot as plt
import os

def save_plots(figures, output_dir):
    for fig in figures:
        figures[fig].savefig(fname=os.path.join(output_dir, fig + '.png'), dpi=150, format='png', bbox_inches='tight')

def save_stats(results, output_dir, fit_name):
    filepath = os.path.join(output_dir, 'fit_stats.txt')
    with open(filepath, 'w') as f:
        f.write(f'Fit type: {fit_name}\n\n')
        f.write('Fitted parameters:\n')
        for i, (param, uncertainty) in enumerate(zip(results['fit_params'], results['uncertainties'])):
            pct_error = (uncertainty / abs(param)) * 100
            f.write(f'a[{i}] = {param:.3f} +- {uncertainty:.3f} ({pct_error:.3f}% error)\n')
        f.write('\n')
        f.write(f'Chi squared: {results["chi_squared"]:.3f}\n')
        f.write(f'Degrees of freedom: {results["dof"]}\n')
        f.write(f'Chi squared reduced: {results["chi_squared_reduced"]:.3f}\n')
        f.write(f'P-probability: {results["p_probability"]:.3f}\n')