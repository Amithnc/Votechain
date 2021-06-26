function show_details(name,aadhar_number,age,phone_number,image) {
    alertify.alert('Your Profile Details :','<div class="row"><div class="col-8"><br> Name: <strong>'+name+'</strong><br>Aadhar No: <strong>'+aadhar_number+'</strong><br>Age: <strong>'+age+'</strong><br>Phone Number: <strong>'+phone_number +'</div><div class="col-4"> <img src="'+image+'" class="img-fluid" style="border: solid black 2px"  /></div></div>');
}

