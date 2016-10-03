changeFontSize = function(element, interval) {
  var size = element.css("font-size");
  var newSize = parseInt(size.replace(/px/,"")) + interval;
  element.css("font-size",newSize);
  return newSize;
}

getBottomOfElement = function(element) {

  var offset = element.offset();

  var top = offset.top;
  var left = offset.left;

  var bottom = top + element.outerHeight();
  return bottom
}

fitToPanel = function(panelId) {
  
  panel = $("#panel-" + panelId)
  panelBody = $("#" + panelId)
  
  
  if( getBottomOfElement(panel) > getBottomOfElement(panelBody) ) {
    while( getBottomOfElement(panel) > getBottomOfElement(panelBody) + 10 ) {
      console.log("increasing font size");
      changeFontSize(panelBody,1);
    }
  }
  else {
    while( getBottomOfElement(panel) < getBottomOfElement(panelBody) - 10 ) {
      console.log("decreasing font size");
      changeFontSize(panelBody,-1);
    }
  }
  
  
}
