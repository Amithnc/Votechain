function vote(canndidate_id,party,candodtae){
    alertify.confirm('Please Confirm','<h4>Are you sure you want to vote <strong>'+String(candodtae)+'</strong> of party <strong> '+String(party)+'</strong></h4><br>  <div class="badge badge-warning" >Vote cannot be revoked once submitted please choose carefully</div>',function(){ cast_vote(canndidate_id)}
                , function(){ alertify.error('Canceled')}).set('labels', {ok:' YES and  Cast Vote', cancel:'Cancel'});
}
function cast_vote(canndidate_id){
    document.getElementById("vote_div").style.display = "none";
    document.getElementById("spinner").style.display = "block";
    alertify.alert('! Do Not Close','<div id="spinner">Please Wait till we process your request<div class="spinner-border text-primary" role="status"><span class="visually-hidden"></span></div></div> ')
    console.log(canndidate_id)
}