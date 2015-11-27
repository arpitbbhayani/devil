$(document).ready(function(){
    $('.ui.dropdown').dropdown();
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
