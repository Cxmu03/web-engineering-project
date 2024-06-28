import re as regex

from sympy import *
from sympy.printing.glsl import glsl_code 
from sympy.parsing.sympy_parser import parse_expr

from .fragment import fragment_shader_source

class Fractal:
    def __init__(self, iterations, escape_radius, formula):
        self.iterations = iterations
        self.escape_radius = escape_radius
        self.formula = formula

    def emit_glsl(self):
        ...

    def emit_html_pre(self):
        ...

def get_calculation_steps(formula: str):
    zx, zy, cx, cy = symbols("zx zy cx cy", real=True)

    print(formula)

    local_symbols = {
        "zx": zx,
        "zy": zy,
        "cx": cx,
        "cy": cy
    } 

    replacements = {
        "(z|c)($|[^xy])": r"(\1x+I*\1y)\2",
        "\^": "**",
    }

    for pattern, replacement in replacements.items():
        formula = regex.sub(pattern, replacement, formula)

    expr = parse_expr(formula, local_dict=local_symbols)

    expr = expr.expand().simplify()

    return expr.as_real_imag()

def get_fragment_shader(iterations: int, escape_radius: float, center_x: float, center_y: float, width: float, formula: str):
    real_calc_step, imag_calc_step = get_calculation_steps(formula)

    return fragment_shader_source.format(iterations=iterations,
                                         escape_radius=escape_radius,
                                         center_x=center_x,
                                         center_y=center_y,
                                         width=width,
                                         real_calc_step=glsl_code(real_calc_step.xreplace({i:Symbol(str(i)+".") for i in real_calc_step.atoms(Integer)})),
                                         imag_calc_step=glsl_code(imag_calc_step.xreplace({i:Symbol(str(i)+".") for i in imag_calc_step.atoms(Integer)})))

