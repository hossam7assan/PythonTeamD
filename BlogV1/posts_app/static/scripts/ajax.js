$(function(){

    var current_comment_id

    ////////////////////////////////////////////

//    $("#commentForm").submit(function(){
//
//        $.ajax({
//
//            type: $("#commentForm").attr("method"),
//            url: $("#commentForm").attr("action"),
//            data: {comment_text: $("#comment-text").val()},
//            success: function(resp){
//
//            }
//        });
//    });

    /////////////////////////////////////////

    $("#likeBtn").click(function(){

        $.ajax({

            url: '/ourblog/likepost',
            type: 'get',
            data: {
                post_id: $(this).attr("postId")
            },

            success: function(resp){

            
            }



        });

    });

    ///////////////////////////////////////

    $("#dislikeBtn").click(function(){


        $.ajax({

        url: '/likepost',
        type: 'post',
        data: {

            post_id: $(this).attr("postId")

        },
        success: function(){





        }



        });

    });

    /////////////////////////////////////

    $("#loginForm").submit(function(){

        $.ajax({

            type: $("#loginForm").attr("method"),
            url: $("#loginForm").attr("action"),
            data: $("#loginForm").serialize(),
            success: function(resp){

            }
        });
    });



    /////////////////////////////////////

    $("#subs").click(function(){

        if($(this).html() == "Subscribe")
            $(this).html("UnSubscribe");

        else
            $(this).html("Subscribe");

        $(this).toggleClass('btn-primary');
        $(this).toggleClass('btn-danger');
    });

});


