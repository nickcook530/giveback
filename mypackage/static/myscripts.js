$(document).ready(function() {

    $(".loading").hide();
    
    $(".primary-cat-btn").click(function(){
        $('#category-body').empty()
        $('#category-header').empty()
        $(".loading").show();
        var url_name = $(this).attr("data");
        $.ajax({
         url: url_name,
         type: "GET",
         success: function(resp){
            $(".loading").hide();
            $('#category-header').empty().append(resp.headerdata);
            $('#category-body').empty().append(resp.bodydata);
        	}
        });
    }); 


});



$('#ajax-content').on('click', "#sub-cat-btn-group > .btn", function() {
    // Set active button for sub_categories
    $("#sub-cat-btn-group > .btn").removeClass("active");
    $(this).addClass("active");
    $('#category-body').empty()
    $(".loading").show();
    var url_name = $(this).attr('data');
    $.ajax({
     url: url_name,
     type: "GET",
     success: function(resp){
        $(".loading").hide();
        $('#category-body').empty().append(resp.bodydata);
    	}
    });
});