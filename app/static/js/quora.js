$(document).ready(function() {
    $('#quora_widget_button').click(function() {
        quora_widget($('#quora_widget_url').val(), 'quora_widget_preview');
    });
});
