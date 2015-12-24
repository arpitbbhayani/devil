$('#flashes').transition('slide down in', {
    onStart: function() {
        setTimeout(function() {
            $('#flashes').transition('slide down out');
        }, 3000);
    }
});

var uiModules = {
    /*
     *  uiModulesClass: Class that defines the UI Modules
     *  Contains all the methods that would enable showing errors,
     *  show waiting ticker, context menu .. etc.
     */

    notify : function(response) {
        $('#msg')
                .removeClass('negative positive')
                .addClass('info')
                .html(response)
                .transition('slide down in', {
                    onComplete: function() {
                        setTimeout(function() {
                            $('#msg').transition('slide down out');
                        }, 3000);
                    }
                });
    },

    showError : function(response) {
    var error = response.error;
        if (!error) {
            error = response;
        }
        $('#msg')
                .removeClass('info positive')
                .addClass('negative')
                .html(response)
                .transition('slide down in', {
                    onComplete: function() {
                        setTimeout(function() {
                            $('#msg').transition('slide down out');
                        }, 3000);
                    }
                });
    }
};
