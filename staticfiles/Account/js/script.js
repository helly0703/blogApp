
def add_friend(friend_id){
    $.ajax({
    url: "demo_test.txt",

    data: {
        'friend_id':friend_id
    }
    success: function(result){
      $("#div1").html(result);
    }});

}