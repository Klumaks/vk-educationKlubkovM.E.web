$(document).ready(function() {
    var availableTags = [
        "perl", "python", "TechnoPark", "MySQL", "django",
        "Mail.Ru", "Voloshin", "Firefox", "moon", "park",
        "puzzle", "space", "engineering", "javascript", "html",
        "css", "programming", "web", "development"
    ];

    $("#tags").autocomplete({
        source: availableTags,
        minLength: 1,
        delay: 100
    });

    $(".close-btn, .btn-cancel").click(function() {
        alert("Form will be closed.");
    });

    $("#ask-form").submit(function(e) {
        e.preventDefault();

        let isValid = true;
        const title = $("#title").val().trim();
        const text = $("#text").val().trim();
        const tags = $("#tags").val().trim();

        if (title.length < 10) {
            $("#title").addClass("error-field");
            $("#title-error").show();
            isValid = false;
        } else {
            $("#title").removeClass("error-field");
            $("#title-error").hide();
        }

        if (text.length < 20) {
            $("#text").addClass("error-field");
            $("#text-error").show();
            isValid = false;
        } else {
            $("#text").removeClass("error-field");
            $("#text-error").hide();
        }

        const tagArray = tags.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0);
        if (tagArray.length === 0 || tagArray.length > 3) {
            $("#tags").addClass("error-field");
            $("#tags-error").show();
            isValid = false;
        } else {
            $("#tags").removeClass("error-field");
            $("#tags-error").hide();
        }

        if (isValid) {
            alert("Question submitted successfully!");
        }
    });
});
