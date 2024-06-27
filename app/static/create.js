const get_fragment_shader = async () => {
    var iterations = document.getElementById('iterations').value;
    var escape_radius = document.getElementById('escape_radius').value;
    var formula = document.getElementById('formula').value;
    var center_x = document.getElementById('center-x').value;
    var center_y = document.getElementById('center-y').value;
    var width = document.getElementById('width').value;

    return await fetch("/fragment?" + new URLSearchParams({
        iterations: iterations,
        escape_radius: escape_radius,
        center_x: center_x,
        center_y: center_y,
        width: width,
        formula: formula
    }).toString())
        .then(response => response.text())
        .then(shader => {
            return shader
        });
}

const adjust_element_sizes = (canvas_selector, shader_selector) => {
    var canvas = document.querySelector(canvas_selector);
    var shader_element = document.querySelector(shader_selector);

    if(shader_element.style.height < canvas.height) {
        shader_element.style.height = canvas.height + "px";
    }
}

const reload_fragment_shader = (fragment_shader) => {
    var fragment_shader_block = document.getElementById("fragment_shader");
    fragment_shader_block.style.maxWidth = canvas.width; 
    fragment_shader_block.textContent = fragment_shader;
    fragment_shader_block.removeAttribute("data-highlighted");
    hljs.highlightElement(fragment_shader_block);
}

const render = async () => {
    var fragment_shader = await get_fragment_shader();
    reload_fragment_shader(fragment_shader);
    render_to("#fractal", fragment_shader);
    adjust_element_sizes("#fractal", "#fragment_shader");
}

var canvas = document.querySelector("#fractal");
var fragment_shader = document.querySelector("#fragment_shader");
canvas.width = window.innerWidth / 2.0;
canvas.height = canvas.width * (9.0 / 16.0);
fragment_shader.style.maxWidth = canvas.width; 


render();