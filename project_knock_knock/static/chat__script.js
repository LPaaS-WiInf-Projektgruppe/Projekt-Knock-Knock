

  $(function()
  {
    window.setInterval(function()
    {
      loadNewChats()
    }, 1000)

  function loadNewChats()
  {
    $.ajax(
      {
        url:"/update_chat/{{dude.id}}",
        type: "POST",
        dataType: "json",
        success: function(data)
        {
          $(messages).replaceWith(data)
        }
      }
    )
  }
});
