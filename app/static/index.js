const deleteFractal = (id) => {
    fetch("/api/fractal/" + id, {
        method: "DELETE"
    }).then((response) => {
        var preview = document.getElementById("preview-for-" + id);

        preview.remove();
    });
}