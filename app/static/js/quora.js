$(document).ready(function() {
    $('#quora_widget_button').click(function() {
        var url = $('#quora_widget_url').val();
        $('#quora_widget_preview').addClass('loading');
        $('#steps').addClass('loading');

        $.get('http://codeville.org.in/quoracard/process', {url: url}, function(result) {
            $('#quora_widget_preview').html(result);
            $('#steps').show();
            $('#steps pre').html('\
&lt;<span class="tag">div</span> type=<span class="str">"card"</span> quora-profile=<span class="str">"'+ url +'"</span>&gt;&lt;/<span class="tag">div</span>&gt;\n\
&lt;<span class="tag">script</span> src=<span class="str">"http://codeville.org.in/static/js/quora-widget.min.js"</span>&gt;&lt;/<span class="tag">script</span>&gt;\
');
        }).always(function(){
            $('#quora_widget_preview').removeClass('loading');
            $('#steps').removeClass('loading');
        });
    });
});
