


// for the nav link iframes

document.addEventListener("DOMContentLoaded", function () {
    let links = document.querySelectorAll(".nav-link");
    let iframe = document.getElementById("content-frame");

    links.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault(); 
            let url = this.getAttribute("href");
            iframe.src = url; 
        });
    });
});