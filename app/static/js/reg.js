$(document).ready(function(){
    $('#password, #confirm_password').on('keyup', function () {
        if ($('#password').val() == $('#confirm_password').val() ) {
          $('#message').html('Matching').css('color', 'green');
          $('#done').prop('disabled', false);
        } else {
          $('#message').html('Not Matching').css('color', 'red');
          $('#done').prop('disabled', true);
        }
      });
});

// Disabling a html button$('#Button').prop('disabled', true);
// Enabling a html button$('#Button').prop('disabled', false);