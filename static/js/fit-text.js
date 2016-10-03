changeFontSize = function(element, interval) {
  var size = element.css("font-size");
  var newSize = parseInt(size.replace(/px/,"")) + interval;
  element.css("font-size",newSize);
  return newSize;
}

getBottomOfElement = function(element) {

  var offset = element.offset();

  var top = offset.top;

  var bottom = top + element.outerHeight();
  return bottom
}

fitToPanel = function(panelId) {
  
  panel = $("#panel-" + panelId)
  panelBody = $("#" + panelId)
  
  if( panelBody.text() != "" ){
    panelBody.css("font-size","1px");
    
    while( getBottomOfElement(panel) > getBottomOfElement(panelBody) + 20) {
      console.log("increasing font size");
      changeFontSize(panelBody,1);
    }
    
    changeFontSize(panelBody,0.5);
    
  }
  
}
