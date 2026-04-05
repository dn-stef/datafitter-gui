from numpy import exp, sin, cos
from scipy.special import gamma

def constant(x, a_0):
    return a_0

def linear(x, a_0, a_1):
    return a_0 + a_1 * x

def polynomial_n(degree):
    def polynomial(x, *coeffs):
        y = 0
        for i in range(degree + 1):
            y += coeffs[i] * x ** i
        return y
    return polynomial

def straight_power(x, a_0, a_1, a_2, a_3):
    return a_0 * (x + a_1) ** a_2 + a_3

def inverse_power(x, a_0, a_1, a_2, a_3):
    return a_0 / (x + a_1) ** a_2 + a_3

def hyperbolic(x, a_0, a_1, a_2):
    return a_0 / (x + a_1) + a_2

def exponential(x, a_0, a_1, a_2):
    return a_0 * exp(a_1 * x) + a_2

def sinf(x, a_0, a_1, a_2, a_3):
    return a_0 * sin(a_1 * x + a_2) + a_3

def cosf(x, a_0, a_1, a_2, a_3):
    return a_0 * cos(a_1 * x + a_2) + a_3

def normal(x, a_0, a_1, a_2, a_3):
    return a_0 * exp( - ((x - a_1) / a_2) ** 2) + a_3

def poisson(x, a_0, a_1, a_2):
    return a_0 * (a_1 ** x) * exp( - a_1) / gamma(x + 1) + a_2

registry = {'constant': constant,
            'linear': linear, 
            'polynomial': polynomial_n,
            'straight_power': straight_power,
            'inverse_power': inverse_power,
            'hyperbolic': hyperbolic,
            'exponential': exponential,
            'sin': sinf,
            'cos': cosf,
            'normal': normal,
            'poisson': poisson
}

equation_string = {'constant': 'a[0]',
                   'linear': 'a[0] + a[1] * x',
                   'polynomial': '',
                   'straight_power': 'a[0] * (x + a[1]) ^ a[2] + a[3]',
                   'inverse_power': 'a[0] / (x + a[1]) ^ a[2] + a[3]',
                   'hyperbolic': 'a[0] / (x + a[1]) + a[2]',
                   'exponential': 'a[0] * exp(a[1] * x) + a[2]',
                   'sin': 'a[0] * sin(a[1] * x + a[2]) + a[3]',
                   'cos': 'a[0] * cos(a[1] * x + a[2]) + a[3]',
                   'normal': 'a[0] * exp( - ((x - a[1]) / a[2]) ^ 2) + a[3]',
                   'poisson': 'a[0] * (a[1] ^ x) * exp(-a[1]) / gamma(x+1) + a[2]'
}

parameter_count = {'constant': 1,
            'linear': 2, 
            'straight_power': 4,
            'inverse_power': 4,
            'hyperbolic': 3,
            'exponential': 3,
            'sin': 4,
            'cos': 4,
            'normal': 4,
            'poisson': 3
}