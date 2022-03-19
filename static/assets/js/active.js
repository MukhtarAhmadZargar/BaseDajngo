$(document).ready(function(){
  $('.navbar-nav li a').click(function(){
    $('li').removeClass("active");
    $(this).addClass("active");
});
});
