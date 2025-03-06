document.addEventListener('DOMContentLoaded', () => {
    /* toggle showing items from hamburger menu on mobile devices */
    const hamburger = document.querySelector(".navbar-burger");
    const menu = document.querySelector("#main-menu");
    const addNoteForm = document.querySelector("#add-note-form");

    const noteSection = document.querySelector("#note-section");
    const noNoteSection = document.querySelector("#no-note-section");
    const addNoteSection = document.querySelector("#add-note-section");

    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("is-active");
        menu.classList.toggle("is-active");
    });

    addNoteForm.addEventListener("submit", function (event) {
        event.preventDefault();

        // display loading indicator on the button
        const saveNoteButton = document.querySelector("#save-note-button");
        saveNoteButton.classList.add("is-loading");

        const formData = new FormData(this);
        fetch(this.action, {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // after successfully adding a note
            if (data.success && data.note) {
                // disable loading on button
                saveNoteButton.classList.remove("is-loading");
                // remove no-note-section
                noNoteSection.classList.add("is-hidden");
                // remove add-note-section
                addNoteSection.classList.add("is-hidden");
                // display the note in note-section:
                noteSection.classList.remove("is-hidden");
                const noteText = document.querySelector("#note-text")
                noteText.textContent = data.note;
            }
        })
        .catch(error => console.error("Error:", error));
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
        $modal.querySelector("#movie-review-title").textContent = `${userName}'s note`;

        if (posterUrl != "None") {
            $modal.querySelector(".modal-movie-poster").src = posterUrl;
        } else {
            $modal.querySelector(".modal-movie-poster").src = "https://placehold.co/300x444?text=No%0APoster";
        }
        $modal.querySelector(".modal-movie-poster").alt = `${title} - movie poster`;

        updateButtonHref = `/users/${userId}/update_movie/${movieId}`;
        deleteButtonHref = `/users/${userId}/delete_movie/${movieId}`;
        addNoteAction = `/users/${userId}/add_note/${movieId}`;

        $modal.querySelector("#update-movie-button").href = updateButtonHref;
        $modal.querySelector("#delete-movie-button").href = deleteButtonHref;

        $modal.querySelector("#add-note-form").action = addNoteAction;
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