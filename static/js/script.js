document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector(".navbar-burger")
    const menu = document.querySelector("#main-menu");

    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("is-active");
        menu.classList.toggle("is-active");
    });
});