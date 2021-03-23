// Closing the alert
setTimeout(function () { 
    $('#alert').alert('close');
}, 5000);

//form validation

function validateForm() {
    name = document.getElementById("name").value
    email = document.getElementById("email").value
    phone = document.getElementById("phone").value;
    aadhar = document.getElementById("aadhar").value;
    password = document.getElementById("password").value;
    cnfpassword = document.getElementById("cnfpassword").value;
    //set cookie.....
    var d = new Date();
    d.setTime(d.getTime() + (30 * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = "phone" + "=" + phone + ";" + expires + ";path=/";
    document.cookie = "aadhar" + "=" + aadhar + ";" + expires + ";path=/";
    document.cookie = "name" + "=" + name + ";" + expires + ";path=/";
    document.cookie = "email" + "=" + email + ";" + expires + ";path=/";
    //end set cookie...
    if (isNaN(phone)) {
        alertify.alert('❌ERROR', "Please enter correct phone number", function () { alertify.error('Enter Correct Phone Number'); });
        return false
    }
    if (isNaN(aadhar)) {
        alertify.alert('❌ERROR', "Please enter correct aadhar number", function () { alertify.error('Enter Correct Aadhar Number'); });
        return false
    }
    if (password != cnfpassword) {
        alertify.alert('❌ERROR', "Both passwords doesnt match", function () { alertify.error('Enter Correct passwords'); });
        return false
    }
}
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
function checkCookie() {
    var user = getCookie("name");
    var phone = getCookie("phone");
    var aadhar= getCookie("aadhar"); 
    var email= getCookie("email");
    document.getElementById("name").value = user;
    document.getElementById("phone").value = phone;
    document.getElementById("aadhar").value = aadhar;
    document.getElementById("email").value = email;
}

function display_message(){
    alertify.alert('Instructions:', '<img src="/media/bulb.png" class="mt-4" width="40%"/><br><h5>1. Make sure to stay in well lighted area.</h5><img src="/media/face-detection.png" class="mt-4" width="40%" /><h5>2. Make sure your face is clearly visible</h5>', function () { alertify.success('click continue to move to the next step'); });
}

