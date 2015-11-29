function update_pre() {
    var media_type = $('#media_type').val();
    var genre = $('#genre').val();
    var api_key = $('#api_key').val();

    replace_helper = {
        'media_type': media_type,
        'genre': genre,
        'api_key': api_key
    };

    var URL_TEMPLATE = 'http://speedster.pythonanywhere.com/{{media_type}}/{{genre}}?api_key={{api_key}}'

    $.each($('#code-snippet'), function(index, block) {
        var restr = "{{" + Object.keys(replace_helper).join('}}|{{')+ "}}";
        var re = new RegExp(restr, "gi" );
        var new_content = URL_TEMPLATE.replace(re, function(matched) {
            matched = matched.slice(2, matched.length-2);
            return replace_helper[matched];
        });
        $(this).text(new_content);
    });
}

$(document).ready(function(){
    $('.ui.dropdown').dropdown();
    $('.menu .item').tab();

    update_pre();

    $('#media_type, #genre').change(function() {
        update_pre();
    });

    $('#share_form').form(
        {
            on: 'blur',
            inline : true,
            fields: {
                title: {
                    identifier  : 'title',
                    rules: [{
                        type   : 'empty',
                        prompt : 'Come on, you must have given some name to your application.'
                    }]
                },
                description: {
                    identifier  : 'description',
                    rules: [{
                        type   : 'empty',
                        prompt : "Won't you like to tell us what your application does?"
                    }]
                }
            }
        }
    );

});

$(function() {
    $('a[href*=#]:not([href=#])').click(function() {
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
            if (target.length) {
                $('html,body').animate({
                    scrollTop: target.offset().top
                }, 1000);
                return false;
            }
        }
    });
});

var fileExtentionRange = '.json';
var MAX_SIZE = 1; // MB

$(document).on('change', '.btn-file :file', function() {
    var input = $(this);

    if (navigator.appVersion.indexOf("MSIE") != -1) { // IE
        var label = input.val();
        input.trigger('fileselect', [ 1, label, 0 ]);
    } else {
        var label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
        var numFiles = input.get(0).files ? input.get(0).files.length : 1;
        var size = input.get(0).files[0].size;

        input.trigger('fileselect', [ numFiles, label, size ]);
    }
});

$('.btn-file :file').on('fileselect', function(event, numFiles, label, size) {
    $('#attachment').attr('name', 'attachment'); // allow upload.
    var postfix = label.substr(label.lastIndexOf('.'));
    if (fileExtentionRange.indexOf(postfix.toLowerCase()) > -1) {
        if (size > 1024 * 1024 * MAX_SIZE ) {
            alert('max size：<strong>' + MAX_SIZE + '</strong> MB.');
            $('#attachment').removeAttr('name'); // cancel upload file.
        } else {
            $('#_attachment').val(label);
        }
    } else {
        alert('file type：<br/> <strong>' + fileExtentionRange + '</strong>');
        $('#attachment').removeAttr('name'); // cancel upload file.
    }
});
