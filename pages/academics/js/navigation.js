const hamburger = document.querySelector(".hamburger");
const closeBtn = document.querySelector(".close-btn");
const navLinks = document.querySelector(".nav-links");

const toggleMenu = () => {
  navLinks.classList.toggle("active");
};

hamburger.addEventListener("click", toggleMenu);
closeBtn.addEventListener("click", toggleMenu);

document.querySelectorAll(".nav-links a").forEach((link) => {
  link.addEventListener("click", toggleMenu);
});

document.addEventListener("click", (e) => {
  if (
    !navLinks.contains(e.target) &&
    !hamburger.contains(e.target) &&
    navLinks.classList.contains("active")
  ) {
    toggleMenu();
  }
});
