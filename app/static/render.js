const vertex_shader_source = `#version 300 es
      in vec4 a_position;
     
      void main() {
        gl_Position = a_position;
      }
`

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


    var vertexShader = create_shader(gl, gl.VERTEX_SHADER, vertex_shader_source);
    var fragmentShader = create_shader(gl, gl.FRAGMENT_SHADER, fragment_shader);

    var program = create_program(gl, vertexShader, fragmentShader);

    var positionAttributeLocation = gl.getAttribLocation(program, "a_position");
    var size_uniform= gl.getUniformLocation(program, "size");

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

    gl.uniform2f(size_uniform, canvas.width, canvas.height);

    gl.enableVertexAttribArray(positionAttributeLocation);
    gl.vertexAttribPointer(positionAttributeLocation, 2, gl.FLOAT, false, 0, 0);

    gl.drawArrays(gl.TRIANGLE_FAN, 0, 4);
}

function render_default_mandelbrot(canvas_selector) {
    fetch("/fragment?iterations=1000&escape_radius=4.0&center_x=0.0&center_y=0.0&width=3.55&formula=z^2%2Bc")
        .then(response => response.text())
        .then(response => {
            console.log(response);
            render_to(canvas_selector, response);
        })
}

function render_default_burning_ship(canvas_selector) {
    fetch("/fragment?iterations=1000&escape_radius=4.0&center_x=0.0&center_y=0.0&width=3.55&formula=(abs(zx)%2Babs(zy)*I)^2%2Bc")
        .then(response => response.text())
        .then(response => {
            console.log(response);
            render_to(canvas_selector, response);
        })
}

function render_julia_set(canvas_selector, c_re, c_im) {
    fetch(`/fragment?iterations=1000&escape_radius=4.0&center_x=0.0&center_y=0.0&width=3.55&formula=(abs(zx)%2Babs(zy)*I)^2%2B((${c_re})%2B(${c_im})*I)`)
        .then(response => response.text())
        .then(response => {
            console.log(response);
            render_to(canvas_selector, response);
        })
}
