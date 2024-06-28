var canvas = document.getElementById("fractal-canvas");

if(canvas != null) {
    canvas.width = 1920;
    canvas.height = 1080;
    canvas.style.height = `${window.innerHeight / 2.0}px`;
    canvas.style.width = `${(canvas.style.height * 16.0) / 9.0}px`;

    render_default_burning_ship("#fractal-canvas");
}