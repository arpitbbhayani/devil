function quora_widget(url, element) {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == XMLHttpRequest.DONE ) {
            if(xmlhttp.status == 200){
                console.log(element);
                element.innerHTML = xmlhttp.responseText;
            }
            else if(xmlhttp.status == 400) {
                alert('There was an error 400')
            }
            else {
                alert('something else other than 200 was returned')
            }
        }
    }
    xmlhttp.open("GET", "http://codeville.org.in/quora/process?url=" + url, true);
    xmlhttp.send();
}

window.addEventListener("DOMContentLoaded", function() {
    var quora_profile_elements = document.querySelectorAll("[quora-profile]");
    for(var i = 0; i < quora_profile_elements.length; i++) {
        var quora_profile_element = quora_profile_elements[i];
        var url = quora_profile_element.getAttribute('quora-profile');

        quora_widget(url, quora_profile_element);
    }
}, false);
