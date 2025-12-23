// Add this at the top of your JS file
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});



function addDjangoMessage(message, tags = 'info') {
    const html = `
    <div class="alert alert-${tags} alert-dismissible fade show" role="alert">
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    `;

    $('.django-messages').append(html);
}


$(function() {

    $('#newsletter-form').on('submit', function(e) {
        console.log("hello");
        e.preventDefault();
        const emailValue = $('#newsletter-email').val();
        
        $.ajax({
            url: '/newsletter/subscribe/', 
            type: 'POST',
            data: {
                'email': emailValue,
                // 'csrfmiddlewaretoken': csrftoken
            },
            success: function(data) {
                addDjangoMessage("Success! Please check your email to confirm.", "success");
                $('#newsletter-form')[0].reset(); 
                $('html, body').animate({ scrollTop: 0 }, 'slow');
            },
            error: function(xhr) {
                const errorMsg = xhr.responseJSON ? xhr.responseJSON.message : "An error occurred.";
                addDjangoMessage("Error: " + errorMsg, "danger")
            }
        });
    });


});