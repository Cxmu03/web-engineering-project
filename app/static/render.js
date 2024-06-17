const vertex_shader_source = `#version 300 es
      in vec4 a_position;
     
      void main() {
        gl_Position = a_position;
      }
`

function get_fragment_shader_source(max_iterations, init_step, calculation_step) {
    return `#version 300 es
        precision highp float;

        out vec4 FragColor;

        vec3 color_palette(int i);

        float map(float v, float v1, float v2, float r1, float r2) {
            return r1 + (((v - v1) / (v2 - v1)) * (r2 - r1));  
        }

        void main() {
            float x = map(gl_FragCoord.x, 0.0, 1920.0, -2.55, 1.0);
            float y = map(gl_FragCoord.y, 0.0, 1080.0, -1.0, 1.0);
            ${init_step}

            int i = 0;
            int max_iterations = ${max_iterations};

            for(; aa + bb <= 4.0 && i < max_iterations; i++) {
                ${calculation_step}
                /*b = 2.0 * a * b + y;
                a = aa - bb + x;
                a = a / b;
                aa = a * a;
                bb = b * b;*/
            }

            if(i < max_iterations) {
                float f = sqrt(float(i) / float(max_iterations));
                FragColor = vec4(vec3(sqrt(f)), 1.0);

            } else {
                FragColor = vec4(vec3(0.0), 1.0);
            }
        }
    `
}

function create_shader(gl, type, source) {
    var shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    var success = gl.getShaderParameter(shader, gl.COMPILE_STATUS);
    if (success) {
        return shader;
    }

    console.log(gl.getShaderInfoLog(shader));
    gl.deleteShader(shader);
}

function create_program(gl, vertexShader, fragmentShader) {
    var program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);
    var success = gl.getProgramParameter(program, gl.LINK_STATUS);
    if (success) {
        return program;
    }
 
    console.log(gl.getProgramInfoLog(program));
    gl.deleteProgram(program);
}

function render_to(canvas_selector, fragment_shader) {
    const canvas = document.querySelector(canvas_selector);
    const gl = canvas.getContext("webgl2");

    if (gl === null) {
        alert("Unable to initialize WebGL. Your browser or machine may not support it.",);
        return;
    }


    //
    //
    //var vertexShaderSource = document.querySelector("#vertex-shader-2d").text;
    //var fragmentShaderSource = document.querySelector("#fragment-shader-2d").text;
     
    var vertexShader = create_shader(gl, gl.VERTEX_SHADER, vertex_shader_source);
    var fragmentShader = create_shader(gl, gl.FRAGMENT_SHADER, fragment_shader);

    var program = create_program(gl, vertexShader, fragmentShader);

    var positionAttributeLocation = gl.getAttribLocation(program, "a_position");

    var vertexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);

    var vertices = [
        -1, -1,
        -1, 1,
        1, 1,
        1, -1
    ];

    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);

    gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);

    gl.clearColor(0.0, 0.0, 0.0, 0.0);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.useProgram(program);

    gl.enableVertexAttribArray(positionAttributeLocation);
    gl.vertexAttribPointer(positionAttributeLocation, 2, gl.FLOAT, false, 0, 0);

    gl.drawArrays(gl.TRIANGLE_FAN, 0, 4);
}

function render_default_mandelbrot(canvas_selector) {
    var fragment_shader = get_fragment_shader_source(
        1000,
        `
        float a = 0.0, b = 0.0, aa = 0.0, bb = 0.0;
        `,
        `
        b = 2.0 * a * b + y;
        a = aa - bb + x;
        aa = a * a;
        bb = b * b;
        `);
    
    render_to(canvas_selector, fragment_shader);
}
