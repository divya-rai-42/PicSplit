$(".images img").click(function(){
    $("#full-image").attr("src", $(this).attr("src"));
    $('#image-viewer').show();
  });
  
  $("#image-viewer").click(function(){
    $('#image-viewer').hide();
  });