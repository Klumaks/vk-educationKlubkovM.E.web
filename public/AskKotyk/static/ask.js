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

    function closeForm() {
        console.log("Closing form...");
        window.location.href = "/";
    }

    $(".close-btn").click(function(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log("Close button clicked");
        closeForm();
    });

    $(".btn-cancel").click(function(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log("Cancel button clicked");
        closeForm();
    });

    $(".overlay").click(function(e) {
        if (e.target === this) {
            console.log("Overlay clicked");
            closeForm();
        }
    });

    $(".ask-form-container").click(function(e) {
        e.stopPropagation();
    });

    $("#ask-form").submit(function(e) {
        e.preventDefault();
        console.log("Form submitted");

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
            console.log("Form is valid, submitting...");

            var formData = new FormData();
            formData.append('title', title);
            formData.append('text', text);
            formData.append('tags', tags);
            formData.append('csrfmiddlewaretoken', $('[name=csrfmiddlewaretoken]').val());

            $.ajax({
                url: '/ask/',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                    alert("Question submitted successfully!");
                    window.location.href = "/";
                },
                error: function(xhr, status, error) {
                    console.log("AJAX error:", error);
                    alert("Error submitting question. Please try again.");
                }
            });
        } else {
            console.log("Form validation failed");
        }
    });

    $("#title, #text, #tags").focus(function() {
        $(this).removeClass("error-field");
        $("#" + $(this).attr("id") + "-error").hide();
    });

    console.log("Ask.js loaded successfully");
    console.log("Close buttons:", $(".close-btn").length);
    console.log("Cancel buttons:", $(".btn-cancel").length);
});
