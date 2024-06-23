uniform_definitions = """
uniform vec2 size;
uniform vec2 center;
uniform float zoom;
"""

constant_definitions = """
vec2 size = {size};
vec2 center = {center};
float zoom;"""

fragment_shader_source = """#version 300 es 
precision highp float;

out vec4 FragColor;

uniform vec2 size;
uniform vec2 center;
uniform float zoom;

vec3 color_palette(int i);

float map(float v, float v1, float v2, float r1, float r2) {{
        return r1 + (((v - v1) / (v2 - v1)) * (r2 - r1));  
}}

void main() {{
    float cx = map(gl_FragCoord.x, 0.0, size.x, -2.55, 1.0);
    float cy = map(gl_FragCoord.y, 0.0, size.y, -1.0, 1.0);
    float zx = 0.0;
    float zy = 0.0;

    int i = 0;
    int max_iterations = {iterations};

    for(; pow(zx, 2.0)+zy*zy <= {escape_radius} && i < max_iterations; i++) {{
        float xtemp = {real_calc_step};
        zy = {imag_calc_step};
        zx = xtemp;
    }}

    if(i < max_iterations) {{
        float f = sqrt(float(i) / float(max_iterations));
        FragColor = vec4(vec3(sqrt(f)), 1.0);

    }} else {{
        FragColor = vec4(vec3(0.0), 1.0);
    }}
}}
"""
