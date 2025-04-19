document.addEventListener("DOMContentLoaded", function () {
    const navLinks = document.querySelectorAll(".nav-link");
    const iframeContainer = document.getElementById("iframe-container");
    const iframe = document.getElementById("content-frame");
    const backButton = document.getElementById("back-button");

    navLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default navigation

            const url = this.getAttribute("href");
            iframe.src = url; // Load the clicked link inside the iframe

            // Show the iframe with a fade-in effect
            iframeContainer.style.display = "block";
            setTimeout(() => {
                iframeContainer.style.opacity = "1";
                iframeContainer.style.transform = "translateY(0)";
            }, 50);

            // Show back button with animation
            backButton.style.display = "block";
            setTimeout(() => {
                backButton.style.opacity = "1";
            }, 100);
        });
    });

    backButton.addEventListener("click", function () {
        // Hide the iframe smoothly
        iframeContainer.style.opacity = "0";
        iframeContainer.style.transform = "translateY(20px)";

        // Hide back button smoothly
        backButton.style.opacity = "0";
        backButton.style.transform = "translateX(-50%) scale(0.9)";

        // Delay hiding elements for a smooth transition
        setTimeout(() => {
            iframeContainer.style.display = "none";
            iframe.src = ""; // Clear iframe src
            backButton.style.display = "none";
        }, 400);
    });
});
