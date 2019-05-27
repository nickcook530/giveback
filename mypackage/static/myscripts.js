$(document).ready(function() {

    $("#primary-cat-btn").click(function(){
        var url_name = $('#primary-cat-btn').attr('data');
        $.ajax({
         url: url_name,
         type: "POST",
         success: function(resp){
            $('#category-header').empty().append(resp.headerdata);
            $('#category-body').empty().append(resp.bodydata);
        	}
        });
        alert(url_name);
    }); 


});

$('#ajax-content').on('click', "#sub-cat-btn-group > .btn", function() {
    // Set active button for sub_categories
    $("#sub-cat-btn-group > .btn").removeClass("active");
    $(this).addClass("active");

    //NEED TO ADD FUNCTIONALITY FOR ALL BUTTON
    var url_name = $('#sub-cat-btn-group > .sub-btn').attr('data');
    $.ajax({
     url: url_name,
     type: "POST",
     success: function(resp){
        $('#category-body').empty().append(resp.bodydata);
    	}
    });
    alert(url_name);
});