$(document).ready(function() {
    var availableTags = [
        "perl", "python", "TechnoPark", "MySQL", "django",
        "Mail.Ru", "Voloshin", "Firefox", "moon", "park",
        "puzzle", "space", "engineering", "javascript", "html",
        "css", "programming", "web", "development"
    ];

    $("#id_tags").autocomplete({
        source: availableTags,
        minLength: 1,
        delay: 100
    });

    function closeForm() {
        window.location.href = "/";
    }

    $(".close-btn").click(function(e) {
        e.preventDefault();
        closeForm();
    });

    $(".btn-cancel").click(function(e) {
        e.preventDefault();
        closeForm();
    });

    $(".overlay").click(function(e) {
        if (e.target === this) {
            closeForm();
        }
    });

    $(".ask-form-container").click(function(e) {
        e.stopPropagation();
    });

    $("#ask-form").submit(function() {
        return true; 
    });
});
