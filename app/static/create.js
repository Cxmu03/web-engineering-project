const get_fragment_shader = async () => {
    var iterations = document.getElementById('iterations').value;
    var escape_radius = document.getElementById('escape_radius').value;
    var formula = document.getElementById('formula').value;
    var center_x = document.getElementById('center-x').value;
    var center_y = document.getElementById('center-y').value;
    var width = document.getElementById('width').value;

    return await fetch("/api/fragment?" + new URLSearchParams({
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
}

const reload_fragment_shader = (fragment_shader) => {
    var fragment_shader_block = document.getElementById("fragment_shader");
    fragment_shader_block.style.maxHeight = `${window.innerHeight - document.getElementById("navbar").offsetHeight}px`;
    fragment_shader_block.style.maxWidth = canvas.style.width; 
    fragment_shader_block.textContent = fragment_shader;
    fragment_shader_block.removeAttribute("data-highlighted");
    hljs.highlightElement(fragment_shader_block);
}

const formula_is_valid = async (formula) => {
    if(formula === "") {
        return false;
    }

    var formula_can_be_processed = await fetch(
        "/api/formula/" + encodeURIComponent(formula) + "/is-valid"
    )
        .then(response => response.text())
        .then(response => { return response });


    return formula_can_be_processed === "true";
}

const checkInputsForRendering = async (skipNameField) => { 
    var is_valid = true;

    for(const field of ["escape_radius", "center-x", "center-y", "width"]) {
        element = document.getElementById(field)
        var float = parseFloat(element.value);

        if(isNaN(float)) {
            element.classList.add("is-invalid");
            is_valid = false;    
        } else {
            element.classList.remove("is-invalid");
        }

        element.value = float;
    }

    iterations = document.getElementById("iterations");
    iterations_value = parseInt(iterations.value)

    iterations.value = iterations_value;

    if(isNaN(iterations_value)) {
        iterations.classList.add("is-invalid");
        is_valid = false;
    } else {
        iterations.classList.remove("is-invalid");
    }

    var formula = document.getElementById("formula");
    if(!(await formula_is_valid(formula.value))) {
        formula.classList.add("is-invalid");
        console.log("Here");
        is_valid = false;
    } else {
        formula.classList.remove("is-invalid");
    }

    if(!skipNameField) {
        var name = document.getElementById("name")
        
        if (name.value === "") {
            name.classList.add("is-invalid");
            is_valid = false;
        } else {
            name.classList.remove("is-invalid");
        }
    }

    return is_valid;
}

const render = async () => {
    if(!(await checkInputsForRendering(true))) {
        return;
    }

    document.getElementById("name").classList.remove("is-invalid");

    var fragment_shader = await get_fragment_shader();
    reload_fragment_shader(fragment_shader);
    render_to("#fractal", fragment_shader);
    adjust_element_sizes("#fractal", "#fragment_shader");

    var canvas = document.getElementById("fractal");
    var preview_canvas = document.getElementById("preview-canvas")

    var ctx_preview = preview_canvas.getContext("2d");

    ctx_preview.drawImage(canvas, 0, 0, preview_canvas.width, preview_canvas.height);

    document.getElementById("preview").value = preview_canvas.toDataURL();
}

const fullscreen = () => {
    var canvas = document.getElementById("fractal");
    canvas.requestFullscreen();
}

var canvas = document.querySelector("#fractal");
var fragment_shader = document.querySelector("#fragment_shader");
canvas.width = 1920;
canvas.height = 1080;
canvas.style.width = `${window.innerWidth / 2.0}px`;
canvas.style.height = `${canvas.style.width * (9.0 / 16.0)}px`;

console.log(document.getElementById("navbar"));

render();

const submitForm = async () => {
    form = document.getElementById("fractal-form");

    var inputs_are_valid = await checkInputsForRendering(false);

    if(inputs_are_valid) {
        form.submit();
    }
}

// Fetch all the forms we want to apply custom Bootstrap validation styles to
//var forms = document.querySelectorAll('.needs-validation')
//  
//// Loop over them and prevent submission
//Array.prototype.slice.call(forms)
//  .forEach(function (form) {
//    form.addEventListener('submit', async function (event) {
//      var inputs_are_valid = await checkInputsForRendering(false);
//      console.log(inputs_are_valid);
//      if (!inputs_are_valid) {
//        event.preventDefault()
//        event.stopPropagation()
//      }
//      form.classList.add('was-validated');
//    }, true)
//  })