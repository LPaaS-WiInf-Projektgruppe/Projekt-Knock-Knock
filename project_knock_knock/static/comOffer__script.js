$("#btn_end_date").on('click', () =>
{

  console.log("clicked div");

  if ($("#input_end_date").css('display') == "none")
  {
    $("#input_end_date").css({'display':'block'});
  }
  else
  {
    $("#input_end_date").css({'display':'none'});
  }

});


$(document).ready( function () {
    $('#com-offer-table').DataTable(
      {
        "pageLength": 5,
        "bLengthChange" : false,
        "pagingType": "numbers"
      }
    );


    $(".active").removeClass("active");
    $("#link-com-offer").addClass("active");
}


);
