$(document).ready(function() {
    var $quora_widget_preview = $('#quora_widget_preview');

    $('#quora_widget_button').click(function() {
        var profile_url = $('#quora_widget_url').val();
        $quora_widget_preview.addClass('loading');
        $.get('/quora/process', {url:profile_url}, function(resp) {

        }).fail(function(response) {
            uiModules.showError(response.responseText);
        }).always(function() {
            $quora_widget_preview.removeClass('loading');
        });
    });
});
