

function openTab(name)
{
  var i;
  var x = document.getElementsByClassName("profile");
  var tabs = document.getElementsByClassName("tab");
  for (var i = 0; i < x.length; i++)
  {
    x[i].style.display = "none";
    tabs[i].style.background = "#7E888A";
  }
  document.getElementById(name).style.display = "block";
  document.getElementById(name + "-tab").style.backgroundColor = "white";
}
