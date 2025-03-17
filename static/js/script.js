document.addEventListener("DOMContentLoaded", () => {
    const MAX_NOTE_LENGTH = 120;

    const hamburger = document.querySelector(".navbar-burger");
    const menu = document.querySelector("#main-menu");

    const noteSection = document.querySelector("#note-section");
    const noNoteSection = document.querySelector("#no-note-section");
    const addNoteSection = document.querySelector("#add-note-section");

    const addNoteForm = document.querySelector("#add-note-form");

    const addNoteTextarea = document.querySelector("#note-textarea");

    const addNoteButton = document.querySelector("#add-note-button");
    const editNoteButton = document.querySelector("#edit-note-button");
    const saveNoteButton = document.querySelector("#save-note-button");
    const cancelNoteButton = document.querySelector("#cancel-note-button");

    /**
     * Show the section with a note and hide all other sections.
     */
    function showNoteSection() {
        noteSection.classList.remove("is-hidden");
        noNoteSection.classList.add("is-hidden");
        addNoteSection.classList.add("is-hidden");
    }

    /**
     * Show the section with info about no note added and hide other sections.
     */
    function showNoNoteSection() {
        noNoteSection.classList.remove("is-hidden");
        noteSection.classList.add("is-hidden");
        addNoteSection.classList.add("is-hidden");
    }

    /**
     * Set remaining characters on character counter bellow textarea upon note adding/editing.
     * @param remainingCharacters characters remaining to use for the note.
     */
    function setNoteRemainingCharacters(remainingCharacters) {
        document.querySelector("#note-char-counter").textContent = `${remainingCharacters} remaining`;
    }

    /**
     * Subtract current note length from maximum note length
     * and return the count as a remaining characters for a note.
     *
     * @param noteText note text to calculate remaining characters for
     * @returns {number} remaining characters to the maximal note length
     */
    function getNoteRemainingCharacters(noteText) {
        return MAX_NOTE_LENGTH - noteText.length;
    }

    /**
     * Show note textarea, remaining character counter and submit button.
     * Remove residual note validation message if present.
     */
    function showAddNoteSection() {
        const noteText = document.querySelector("#note-text").textContent || "";
        setNoteRemainingCharacters(getNoteRemainingCharacters(noteText));
        displayNoteValidation("");
        addNoteSection.classList.remove("is-hidden");
        noNoteSection.classList.add("is-hidden");
        noteSection.classList.add("is-hidden");
    }

    /**
     * Insert the note text to note holding element.
     * @param text note text to display
     */
    function addNoteText(text) {
        document.querySelector("#note-text").textContent = text;
    }

    /**
     * Insert the note text as a value to the note textarea element for
     * adding or editing the note.
     * @param text note text to display in the textarea element
     */
    function addNoteToTextarea(text) {
        document.querySelector("#note-textarea").value = text;
    }

    /**
     * Cleaning up, hiding note section, no note warning section and add/edit note section,
     * removing residual note text from text area and removing note text from note element.
     */
    function modalCleanup() {
        // hide all sections
        noteSection.classList.add("is-hidden");
        noNoteSection.classList.add("is-hidden");
        addNoteSection.classList.add("is-hidden");
        // note cleanup
        addNoteToTextarea("");
        addNoteText("");
    }

    /**
     * Turn loading indicator on save note button on.
     */
    function saveNoteButtonLoadingOn() {
        saveNoteButton.classList.add("is-loading");
    }

    /**
     * Turn loading indicator on save note button off.
     */
    function saveNoteButtonLoadingOff() {
        saveNoteButton.classList.remove("is-loading");
    }

    /**
     * Display note validation error.
     * @param text validation error to display in note error message element
     */
    function displayNoteValidation(text) {
        document.querySelector("#note-error-message").textContent = text;
    }

    // MODAL ACTIONS & HELPERS

    /**
     * Handle validation of movie data:
     * When value is "None" return "N/A", else return the value.
     *
     * Explanation:
     *      When no value was found in backend the value returned is "None".
     *      Unknown values from backend have value "N/A".
     *      This function unifies the output to "N/A" for unknown values.
     * @param text text data for validation
     * @returns {*|string} valid text value or "N/A"
     */
    function validateDataValue(text) {
        if (text === "None") {
            return "N/A";
        }
        return text;
    }

    /**
     * Add movie data to displayed movie modal.
     * @param $modal movie modal element
     * @param data data object holding movie details passed as data attributes to modal
     */
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

        $modal.querySelector("#movie-title").textContent = validateDataValue(title);
        $modal.querySelector("#movie-director").textContent = validateDataValue(director);
        $modal.querySelector("#movie-year").textContent = validateDataValue(year);
        $modal.querySelector("#movie-rating").textContent = validateDataValue(rating);
        $modal.querySelector("#movie-review-title").textContent = `${userName}'s note`;

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

    /**
     * Open the movie modal and assign the data from data attributes to it before
     * displaying it.
     * @param $modal modal element to show.
     * @param data modal data passed as values of data attributes on modal trigger.
     */
    function openModal($modal, data) {
        assignDataToMovieModal($modal, data);
        $modal.classList.add("is-active");
    }

    /**
     * Close the active modal and clean modal data.
     * @param $el modal element to assign "is-active" class to
     */
    function closeModal($el) {
        $el.classList.remove("is-active");
        modalCleanup();
    }

    /**
     * Hide all active modals on the page.
     */
    function closeAllModals() {
        (document.querySelectorAll(".modal") || []).forEach(($modal) => {
            closeModal($modal);
        });
    }

    // *** EVENT HANDLERS ***

    /**
     * Toggle hamburger menu on/off.
     */
    function handleHamburgerMenuToggle() {
        hamburger.classList.toggle("is-active");
        menu.classList.toggle("is-active");
    }

    /**
     * Handle saving note with visual clues and validation.
     * @param event submit event to stop
     */
    function handleSavingNote(event) {
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
    }

    /**
     * Handle setting reminding characters of the note during typing.
     * @param event note textarea event to obtain the note text from
     */
    function handleSetRemainingCharactersOnNote(event) {
        const noteText = event.target.value;
        setNoteRemainingCharacters(getNoteRemainingCharacters(noteText));
    }

    /**
     * Handle aborting note editing via cancel button.
     */
    function handleCancelNote() {
        const movieNote = document.querySelector("#note-text").textContent;

        if (movieNote !== "") {
            showNoteSection();
        } else {
            showNoNoteSection();
        }

        // reset residual value of note textarea
        addNoteToTextarea("");
    }

    /**
     * Handle start of note editing via Add/Edit note button.
     */
    function handleEditNote() {
        const noteText = document.querySelector("#note-text").textContent;
        showAddNoteSection();
        addNoteToTextarea(noteText);
    }

    // *** EVENT LISTENERS ***

    hamburger.addEventListener("click", handleHamburgerMenuToggle);
    addNoteButton.addEventListener("click", showAddNoteSection);
    addNoteForm.addEventListener("submit", handleSavingNote);
    addNoteTextarea.addEventListener("keyup", handleSetRemainingCharactersOnNote);
    cancelNoteButton.addEventListener("click", handleCancelNote);
    editNoteButton.addEventListener("click", handleEditNote);

    // *** MODAL EVENTS ***

    // remove notification from page upon clicking on the delete button
    (document.querySelectorAll(".notification .delete") || []).forEach((delete_button) => {
        const notification = delete_button.parentNode;

        delete_button.addEventListener("click", () => {
            notification.parentNode.removeChild(notification);
        });
    });

    // add a click event on buttons to open a specific modal
    (document.querySelectorAll(".js-modal-trigger") || []).forEach(($trigger) => {
        const modalData = $trigger.dataset;
        const modal = $trigger.dataset.target;
        const $target = document.getElementById(modal);

        $trigger.addEventListener("click", () => {
            openModal($target, modalData);
        });
    });

    // add a click event on various child elements to close the parent modal
    (document.querySelectorAll(".modal-background, .modal-close") || [])
        .forEach(($close) => {
            const $target = $close.closest(".modal");

            $close.addEventListener("click", () => {
                closeModal($target);
            });
        });

    // add a keyboard event to close all modals
    document.addEventListener("keydown",(event) => {
        if (event.key === "Escape") {
            closeAllModals();
        }
    });
});