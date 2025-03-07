document.addEventListener('DOMContentLoaded', () => {
    const MAX_NOTE_LENGTH = 120;

    /* toggle showing items from hamburger menu on mobile devices */
    const hamburger = document.querySelector(".navbar-burger");
    const menu = document.querySelector("#main-menu");

    const noteSection = document.querySelector("#note-section");
    const noNoteSection = document.querySelector("#no-note-section");
    const addNoteSection = document.querySelector("#add-note-section");

    const addNoteForm = document.querySelector("#add-note-form");

    const addNoteTextarea = document.querySelector("#note-textarea");

    const addNoteButton = document.querySelector("#add-note-button");
    const editNoteButton = document.querySelector("#edit-note-button");
    const cancelNoteButton = document.querySelector("#cancel-note-button");

    function showNoteSection() {
        noteSection.classList.remove("is-hidden");
        noNoteSection.classList.add("is-hidden");
        addNoteSection.classList.add("is-hidden");
    }

    function showNoNoteSection() {
        noNoteSection.classList.remove("is-hidden");
        noteSection.classList.add("is-hidden");
        addNoteSection.classList.add("is-hidden");
    }

    function setNoteRemainingCharacters(remainingCharacters) {
        document.querySelector("#note-char-counter").textContent = `${remainingCharacters} remaining`;
    }

    function getNoteRemainingCharacters(noteText) {
        return MAX_NOTE_LENGTH - noteText.length;
    }

    function showAddNoteSection() {
        const noteText = document.querySelector("#note-text").textContent || '';
        setNoteRemainingCharacters(getNoteRemainingCharacters(noteText));
        displayNoteValidation("");
        addNoteSection.classList.remove("is-hidden");
        noNoteSection.classList.add("is-hidden");
        noteSection.classList.add("is-hidden");
    }

    function addNoteText(text) {
        document.querySelector("#note-text").textContent = text;
    }

    function addNoteToTextarea(text) {
        document.querySelector("#note-textarea").value = text
    }

    function modalCleanup() {
        // hide all sections
        noteSection.classList.add("is-hidden");
        noNoteSection.classList.add("is-hidden");
        addNoteSection.classList.add("is-hidden");

        // note cleanup
        addNoteToTextarea("");
        addNoteText("")
    }

    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("is-active");
        menu.classList.toggle("is-active");
    });

    addNoteButton.addEventListener("click", () => {
        showAddNoteSection();
    });

    editNoteButton.addEventListener("click", () => {
        const noteText = document.querySelector("#note-text").textContent;
        showAddNoteSection();
        addNoteToTextarea(noteText);
    });

    function saveNoteButtonLoadingOn() {
        const saveNoteButton = document.querySelector("#save-note-button");
        saveNoteButton.classList.add("is-loading");
    }

    function saveNoteButtonLoadingOff() {
        const saveNoteButton = document.querySelector("#save-note-button");
        saveNoteButton.classList.remove("is-loading");
    }

    function displayNoteValidation(text) {
        document.querySelector("#note-error-message").textContent = text;
    }

    addNoteForm.addEventListener("submit", function (event) {
        event.preventDefault();

        saveNoteButtonLoadingOn();
        const formData = new FormData(this);

        fetch(this.action, {
            method: "POST", body: formData
        })
            .then(response => response.json())
            .then(data => {
                // after successfully adding a note
                if (data.success) {
                    showNoteSection()
                    addNoteText(data.note);
                    // update the data-movie-note of js-modal-trigger
                    const noteMovieId = this.getAttribute("data-movie-id");
                    const modalTrigger = document.querySelector(`.js-modal-trigger[data-movie-id="${noteMovieId}"]`);
                    modalTrigger.setAttribute("data-movie-note", data.note);
                } else {
                    displayNoteValidation(data.error);
                }
            })
            .catch(error => console.error("Error:", error))
            .finally(() => {
                // disable loading on button
                saveNoteButtonLoadingOff();
            });
    });

    // set reminding characters of the note on typing
    addNoteTextarea.addEventListener("keyup", function (event) {
        const noteText = event.target.value;
        setNoteRemainingCharacters(getNoteRemainingCharacters(noteText));
    })

    cancelNoteButton.addEventListener("click", () => {
        const movieNote = document.querySelector("#note-text").textContent

        if (movieNote !== "") {
            showNoteSection();
        } else {
            showNoNoteSection();
        }

        addNoteToTextarea("");
    });

    /* remove notification from page upon clicking on the delete button */
    (document.querySelectorAll('.notification .delete') || []).forEach((delete_button) => {
        const notification = delete_button.parentNode;

        delete_button.addEventListener('click', () => {
            notification.parentNode.removeChild(notification);
        });
    });

    function assignDataToMovieModal($modal, data) {
        const title = data.movieTitle;
        const director = data.movieDirector;
        const year = data.movieYear;
        const rating = data.movieRating;
        const posterUrl = data.moviePosterUrl;
        const userName = data.movieUser;
        const userId = data.userId;
        const movieId = data.movieId;
        const movieNote = data.movieNote;

        addNoteForm.setAttribute("data-movie-id", movieId);

        $modal.querySelector("#movie-title").textContent = title;
        $modal.querySelector("#movie-director").textContent = director;
        $modal.querySelector("#movie-year").textContent = year;
        $modal.querySelector("#movie-rating").textContent = rating;
        $modal.querySelector("#movie-review-title").textContent = `${userName}'s note`;

        console.log(movieNote);
        if (movieNote !== "None") {
            addNoteText(movieNote);
            showNoteSection();
        } else {
            addNoteText("");
            showNoNoteSection();
        }

        if (posterUrl !== "None") {
            $modal.querySelector(".modal-movie-poster").src = posterUrl;
        } else {
            $modal.querySelector(".modal-movie-poster").src = "https://placehold.co/300x444?text=No%0APoster";
        }

        $modal.querySelector(".modal-movie-poster").alt = `${title} - movie poster`;

        const updateButtonHref = `/users/${userId}/update_movie/${movieId}`;
        const deleteButtonHref = `/users/${userId}/delete_movie/${movieId}`;
        const addNoteAction = `/users/${userId}/add_note/${movieId}`;

        $modal.querySelector("#update-movie-button").href = updateButtonHref;
        $modal.querySelector("#delete-movie-button").href = deleteButtonHref;
        $modal.querySelector("#add-note-form").action = addNoteAction;
    }

    // Functions to open and close a modal
    function openModal($modal, data) {
        if ($modal.id === "movie-modal") {
            assignDataToMovieModal($modal, data);
        }

        $modal.classList.add('is-active');
    }

    function closeModal($el) {
        $el.classList.remove('is-active');
        modalCleanup();
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
    (document.querySelectorAll(".modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button") || [])
        .forEach(($close) => {
            const $target = $close.closest('.modal');

            $close.addEventListener('click', () => {
                closeModal($target);
            });
        });

    // Add a keyboard event to close all modals
    document.addEventListener('keydown', (event) => {
        if (event.key === "Escape") {
            closeAllModals();
        }
    });
});