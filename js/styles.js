/*
  Style changes to Python iNotebook
  Copyright 2018: Lemuel Kumarga
*/

$(document).ready(function(){

  var is_notebook = $(".jpNotebook").length;

  /* ============================================= 
    Edit Metadata
  ============================================== */

  /* On Mobiles: Reduce Width Instead of Zooming Out */
  $("head").append('<meta name="viewport" content="width=device-width, initial-scale=1">')
  
  /* ============================================= 
    Remove unnecessary classes and add final_output_identifier
  ============================================== */
  
  $("body").addClass("jp-RenderedHTML");
  $(".jp-RenderedHTMLCommon").removeClass("jp-RenderedHTMLCommon"); 


  /* ============================================= 
    Add code buttons
  ============================================== */
  function setCodeToShow(inputContainer, inputButton, speed = 200) {
    inputContainer.show(speed);
    inputButton.html("Hide");
    inputButton.attr("cshown", "true");
  }

  function setCodeToHide(inputContainer, inputButton, speed = 200) {
    inputContainer.hide(speed);
    inputButton.html("Code");
    inputButton.attr("cshown", "false");
  }

  $(".code-fold-div").remove();

  /* Code Buttons for each section */
  var code_button_str = '<div class="code-fold-div">' + 
                            '<button class="btn btn-default btn-xs code-fold-btn" cshown="true">Hide</button>' +
                        '</div>';

  $(".jp-CodeCell > .jp-Cell-inputWrapper").parent().prepend(code_button_str);
  
  $(".code-fold-btn").on("click", function () {
    var tag = $(this).attr("cshown");
    var toggle_function = tag == "false" ? setCodeToShow : setCodeToHide;
    toggle_function($(this).parent().siblings(".jp-Cell-inputWrapper"), $(this));
  });

  /* Code Buttons for show all hide all */
  var code_overall_str = '<div class="jp-Cell jp-MarkdownCell jp-Notebook-cell"><div class="jp-Cell-inputWrapper" tabindex="0"><div class="code-fold-div"><div class="jp-InputArea jp-Cell-inputArea">' + 
                            '<button class="btn btn-default btn-xs code-hide-all">Hide All Code</button>' +
                            '<button class="btn btn-default btn-xs code-show-all">Show All Code</button>' +
                        '</div></div></div></div>'
  $("main").prepend(code_overall_str)

  var section_inputs = $(".jp-CodeCell > .jp-Cell-inputWrapper");
  var section_buttons = $(".code-fold-btn");
  $(".code-hide-all").on("click", function() {
      setCodeToHide(section_inputs, section_buttons);  
  })
  $(".code-show-all").on("click", function() {
      setCodeToShow(section_inputs, section_buttons);  
  })

  /* Default view is hidden */

  if (is_notebook) {
    setCodeToShow(section_inputs, section_buttons, 0);
  } else {
    setCodeToHide(section_inputs, section_buttons, 0);
  }
  
  /* ============================================= 
    Prevent autoscrolling of output divs
  ============================================== */
  IPython.OutputArea.prototype._should_scroll = function(lines) {
    return false;
  }
});