$(function() {
    // http://stackoverflow.com/questions/18972515/how-to-create-ajax-refresh-for-django-simple-captcha
    // Add refresh button after field (this can be done in the template as well)
    $('input#id_captcha_1').after(
        $('<a href="#void" class="captcha-refresh"><button class="btn-default btn">Refresh</button></a>')
    );

    // Click-handler for the refresh-link
    $('.captcha-refresh').click(function(){
        var $form = $(this).parents('form');
        var url = location.protocol + "//" + window.location.hostname + ":"
                  + location.port + "/captcha/refresh/";

        // Make the AJAX-call
        $.getJSON(url, {}, function(json) {
            $form.find('input[name="captcha_0"]').val(json.key);
            $form.find('img.captcha').attr('src', json.image_url);
        });

        return false;
    });
});