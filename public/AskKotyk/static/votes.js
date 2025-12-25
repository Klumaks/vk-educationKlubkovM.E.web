$(document).ready(function() {
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 10) === ('csrftoken=')) {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
            }
        }
    });

    $(document).on('click', '.vote-btn', function(e) {
        e.preventDefault();
        const button = $(this);

        const questionId = button.data('question-id');
        const answerId = button.data('answer-id');
        const authenticated = button.data('authenticated');

        if (authenticated && authenticated.toString().toLowerCase() !== 'true') {
            alert('Please login to vote');
            window.location.href = '/login/?next=' + encodeURIComponent(window.location.pathname);
            return;
        }

        const voteType = button.hasClass('up') ? 'like' : 'dislike';

        let url, data;
        if (questionId) {
            url = '/ajax/vote/question/';
            data = { question_id: parseInt(questionId), vote_type: voteType };
        } else if (answerId) {
            url = '/ajax/vote/answer/';
            data = { answer_id: parseInt(answerId), vote_type: voteType };
        } else {
            console.error('No question-id or answer-id found');
            return;
        }

        console.log('Sending AJAX request:', { url, data, authenticated });

        $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                console.log('AJAX success:', response);
                if (response.success) {
                    const counter = button.siblings('.vote-count');
                    counter.text(response.votes_count);

                    const container = button.closest('.votes');
                    const upBtn = container.find('.vote-btn.up');
                    const downBtn = container.find('.vote-btn.down');

                    upBtn.removeClass('active');
                    downBtn.removeClass('active');

                    if (response.user_vote === 'like') {
                        upBtn.addClass('active');
                    } else if (response.user_vote === 'dislike') {
                        downBtn.addClass('active');
                    }
                }
            },
            error: function(xhr) {
                console.error('AJAX error:', xhr.status, xhr.responseJSON);
                if (xhr.status === 403 || xhr.status === 401) {
                    alert('Please login to vote');
                    window.location.href = '/login/?next=' + encodeURIComponent(window.location.pathname);
                } else if (xhr.responseJSON && xhr.responseJSON.error) {
                    alert('Error: ' + xhr.responseJSON.error);
                } else {
                    alert('Unknown error occurred. Please try again.');
                }
            }
        });
    });

    $(document).on('click', '.mark-correct-btn', function(e) {
        e.preventDefault();
        const button = $(this);
        const answerId = button.data('answer-id');

        console.log('Marking correct answer:', answerId);

        $.ajax({
            url: '/ajax/mark-correct/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ answer_id: parseInt(answerId) }),
            success: function(response) {
                console.log('Mark correct success:', response);
                if (response.success) {
                    const answerDiv = $('#answer-' + answerId);
                    const badge = answerDiv.find('.correct-badge');

                    if (response.is_correct) {
                        badge.show();
                        button.text('✓ Correct');
                        button.addClass('active');

                        $('.answer').not(answerDiv).each(function() {
                            $(this).find('.mark-correct-btn').text('Mark as Correct').removeClass('active');
                            $(this).find('.correct-badge').hide();
                        });
                    } else {
                        badge.hide();
                        button.text('Mark as Correct');
                        button.removeClass('active');
                    }

                    alert(response.message);
                }
            },
            error: function(xhr) {
                console.error('Mark correct error:', xhr.status, xhr.responseJSON);
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    alert('Error: ' + xhr.responseJSON.error);
                } else {
                    alert('Unknown error occurred. Please try again.');
                }
            }
        });
    });
        $('#id_avatar').hide();

    $('label.btn-choose[for="id_avatar"]').on('click', function(e) {
        e.preventDefault();
        $('#id_avatar').click();
    });

    $('#id_avatar').on('change', function() {
        var fileName = $(this).val().split('\\').pop();
        var fileSpan = $('.file-path');

        if (fileName) {
            fileSpan.text(fileName);
        } else {

            fileSpan.text('No avatar selected');
        }
    });
});
