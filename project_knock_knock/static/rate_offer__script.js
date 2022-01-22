/* Test if input[type="range"] supported (via Modernizr) [footnote 1] */
var bool,
    output = document.createElement("output"),
    range = document.createElement("input"),
    smile = ":)";

range.setAttribute("type", "range");

if (bool = range.type !== "text") {
  range.value = smile;
  range.style.cssText = "position:absolute;visibility:hidden;";
  if (range.style.WebkitAppearance !== undefined ) {
    document.body.appendChild(range);
    bool = range.offsetHeight !== 0; // Mobile android web browser has false positive, so must check the height to see if the widget is actually there.
    document.body.removeChild(range);
  }
} else {
  bool = range.value == smile;
}

if (bool) { initRange(); } // input[type="range"] is supported


function initRange() {
  var listItemContent, listItem,
      selects = document.getElementsByTagName("select"),
      list = document.createElement("ol"),
      i, j;

  output.setAttribute("for","rating");
  output.value = 0;
  range.value = range.style.cssText = ""; // reset range from support testing

  /* input["range"] polyfill (via @remysharp) [footnote 2] */
  for (i = selects.length; i--;) {
    if (selects[i].getAttribute("data-type") == "range") { (function(select) {

      /* Create an ordered list based on the select element for use in the "images off" scenario*/
      for (j = 0; j < select.length; j++) {
        listItemContent = Number(select.options[j].value.substr(0,1));
        if (listItemContent) {
          listItem = document.createElement("li");
          listItem.innerHTML = listItemContent.toString();
          list.appendChild(listItem);
        }
      }

      select.parentNode.appendChild(list);

      /* Turn off display and show with CSS to account for CSS off scenario */
      list.style.display = "none";

      /* Replace Select element with Input Type = Range */
      select = select.parentNode.replaceChild(range, select);
      range.name = "rating";
      range.value = range.step = range.min = 1;
      range.max = 5;
    })(selects[i]);}
  }
  /* end polyfill */

  range.className = "default";
  range.parentNode.appendChild(output);

  bindEvent(range, "touchstart", function(e) { ratingSwap(this,e); });
  bindEvent(range, "mousedown", function() { ratingSwap(this); });
  bindEvent(range, "change", function() { ratingSwap(this); });
  /*  bindEvent(range, "click", function(e) { ratingSwap(this,e); }); */
}

/**
* @param el The element to be bound.
* @param eventName The event to attach to the element.
* @param eventHandler The function to trigger on event activation.
**/
function bindEvent(el, eventName, eventHandler) {
  if (el.addEventListener) { el.addEventListener(eventName, eventHandler, false); }
  else if (el.attachEvent) { el.attachEvent("on" + eventName, eventHandler); }
  else { alert("Event binding failed due to lack of support for addEventListener/attachEvent"); }
}

/**
* @param el The input[type="range"] element.
* @param e The interaction event.
**/
function ratingSwap(el, e) {
  var areaClicked = 0,
    currentStep = 0,
    areaStep = 16,  /* step width of range (i.e. star width) */
    areaSteps = 5,  /* number of steps in range (i.e. # of stars) */
    i;

  if (el.className == "default") {
    el.className = "";
  };

  /* Triggers on click (1) on smartphone tap, (2) on click of current star on desktop */
  if (e) {
    /**
    * Get click position respective to the input
    * position = (click) - (relatively positioned parent location) - (input location)
    **/
    areaClicked = e.pageX - e.target.parentNode.offsetLeft - e.target.offsetLeft;

    /* Map click positions to input values; assign values */
    for (i = areaSteps; i--;) {
      if (Math.abs(areaClicked) <= (i * areaStep)) {
        el.value = i;
        break;
      }
    }
  }

  /* Get the correct background-position for the star sprite */
  currentStep = ((el.value - 2) * -(areaStep) - 1) + "px";

  /* Set the correct background-position for the star sprite */
  el.style.backgroundPosition = "0 " + currentStep + ", 0 0";
   /* Update the output value */
  output.innerHTML = el.value;
}
