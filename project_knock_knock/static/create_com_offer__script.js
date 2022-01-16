$(document).on('ready', () =>
{
  google.maps.event.addDomListener(window, 'load', init);

  filled = true

  $("form#offer-form :input").each(function()
  {
    filled = $(this).val().trim() == "";
  })

  if (filled)
  {
    $("#create-offer-btn").css("color","#7E888A");
    $("#create-offer-btn").css("border","solid #7E888A 1px");
    $("#create-offer-btn").attr("disabled", true);
  }
  else
  {
    $("#create-offer-btn").css("color","#79AB64");
    $("#create-offer-btn").css("border","solid #79AB64 1px");
    $("#create-offer-btn").attr("disabled", false);
  }
})
$(document).keyup(() =>
{
  filled = true

  $("form#offer-form :input").each(function()
  {
    console.log($(this).val());
    if ($(this).val() == "")
    {
      console.log("entered if case");
      filled = false;
    }

  })

  console.log(filled);

  if (filled)
  {
    $("#create-offer-btn").css("color","#79AB64");
    $("#create-offer-btn").css("border","solid #79AB64 1px");
    $("#create-offer-btn").attr("disabled", false);

  }

  else
  {
    $("#create-offer-btn").css("color","#7E888A");
    $("#create-offer-btn").css("border","solid #7E888A 1px");
    $("#create-offer-btn").attr("disabled", true);
  }

})


$(document).mouseup(() =>
{
  filled = true

  $("form#offer-form :input").each(function()
  {
    console.log($(this).val());
    if ($(this).val() == "")
    {
      console.log("entered if case");
      filled = false;
    }

  })

  console.log(filled);

  if (filled)
  {
    $("#create-offer-btn").css("color","#79AB64");
    $("#create-offer-btn").css("border","solid #79AB64 1px");
    $("#create-offer-btn").attr("disabled", false);

  }

  else
  {
    $("#create-offer-btn").css("color","#7E888A");
    $("#create-offer-btn").css("border","solid #7E888A 1px");
    $("#create-offer-btn").attr("disabled", true);
  }

})

function init() {
   var from_input = document.getElementById('from-input');
   var to_input = document.getElementById('to-input');
   var autocomplete_from = new google.maps.places.Autocomplete(from_input);
   var autocomplete_to = new google.maps.places.Autocomplete(to_input);
  // var  autocomlete = new google.maps.places.Autocomplete($("#from-input"))
}
