var uiModulesClass = function(crons) {
    /*
     *  uiModulesClass: Class that defines the UI Modules
     *  Contains all the methods that would enable showing errors,
     *  show waiting ticker, context menu .. etc.
     */

    this.notifySaved = function() {
    };

    this.showError = function(response) {
        if( typeof(response) == 'string' ) {
            $('#error-msg').html(response);
        }
        else {
            $('#error-msg').html(response.error);
        }

        $('#error-zone')
            .sidebar('setting', 'transition', 'overlay')
            .sidebar('setting', 'dimPage', false)
            .sidebar('toggle');

    };

    this.showWaiting = function(targetElement) {
        targetElement.html('<i class="fa fa-spinner fa-spin"></i>');
    }

    this.removeWaiting = function(targetElement) {
        targetElement.html(null);
    }
};
