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

    function assignDataToMovieModal($modal, data) {
        title = data.movieTitle;
        director = data.movieDirector;
        year = data.movieYear;
        rating = data.movieRating;
        posterUrl = data.moviePosterUrl;
        userName = data.movieUser;
        userId = data.userId;
        movieId = data.movieId;

        $modal.querySelector("#movie-title").textContent = title;
        $modal.querySelector("#movie-director").textContent = director;
        $modal.querySelector("#movie-year").textContent = year;
        $modal.querySelector("#movie-rating").textContent = rating;
        $modal.querySelector("#movie-review-title").textContent = `${userName}'s review`;

        if (posterUrl != "None") {
            $modal.querySelector(".modal-movie-poster").src = posterUrl;
        } else {
            $modal.querySelector(".modal-movie-poster").src = "https://placehold.co/300x444?text=No%0APoster";
        }
        $modal.querySelector(".modal-movie-poster").alt = `${title} - movie poster`;

        updateButtonHref = `/users/${userId}/update_movie/${movieId}`;
        deleteButtonHref = `/users/${userId}/delete_movie/${movieId}`;

        $modal.querySelector("#update-movie-button").href = updateButtonHref;
        $modal.querySelector("#delete-movie-button").href = deleteButtonHref;
    }

    // Functions to open and close a modal
    function openModal($modal, data) {
        if ($modal.id == "movie-modal") {
            assignDataToMovieModal($modal, data);
        }

        $modal.classList.add('is-active');
    }

    function closeModal($el) {
        $el.classList.remove('is-active');
    }

    function closeAllModals() {
        (document.querySelectorAll('.modal') || []).forEach(($modal) => {
            closeModal($modal);
        });
    }

    // Add a click event on buttons to open a specific modal
    (document.querySelectorAll('.js-modal-trigger') || []).forEach(($trigger) => {
        const modalData = $trigger.dataset;
        const modal = $trigger.dataset.target;
        const $target = document.getElementById(modal);

        $trigger.addEventListener('click', () => {
            openModal($target, modalData);
        });
    });

    // Add a click event on various child elements to close the parent modal
    (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
        const $target = $close.closest('.modal');

        $close.addEventListener('click', () => {
            closeModal($target);
        });
    });

    // Add a keyboard event to close all modals
    document.addEventListener('keydown', (event) => {
        if(event.key === "Escape") {
            closeAllModals();
        }
    });
});