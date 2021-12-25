$(document).on('ready', () =>
{

  $("form#offer-form :input").each(function()
  {
    filled = $(this).val().trim() == "";
  })


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
$(document).keyup(() =>
{
  filled = true

  $("form#offer-form :input[type='text']").each(function()
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
