document.addEventListener('DOMContentLoaded', () => {
    /* toggle showing items from hamburger menu on mobile devices */
    const hamburger = document.querySelector(".navbar-burger")
    const menu = document.querySelector("#main-menu");

    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("is-active");
        menu.classList.toggle("is-active");
    });

    /* remove notification from page upon clicking on the delete button */
    (document.querySelectorAll('.notification .delete') || []).forEach((delete_button) => {
        const notification = delete_button.parentNode;

        delete_button.addEventListener('click', () => {
            notification.parentNode.removeChild(notification);
        });
    });
});