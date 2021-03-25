function validate(){
    var input=document.getElementById("candidate_name").value;
    if(input==""){
        alertify.alert('❌ERROR', 'SELECT APPROPRIATE CANDIDATE TO VOTE', function () { alertify.error('please select any of the candidate form the dropdown'); });
        return false
    }
}