/*
  Style changes to Python iNotebook
  Copyright 2018: Lemuel Kumarga
*/

$(document).ready(function(){

  /* ============================================= 
    Remove unnecessary classes
  ============================================== */
    
  $(".rendered_html").removeClass("rendered_html");


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
                            '<button class="code-fold-btn" cshown="true">Hide</button>' +
                        '</div>';

  $(".input").parent().prepend(code_button_str);
  
  $(".code-fold-btn").on("click", function () {
    var tag = $(this).attr("cshown");
    var toggle_function = tag == "false" ? setCodeToShow : setCodeToHide;
    toggle_function($(this).parent().siblings(".input"), $(this));
  });

  /* Code Buttons for show all hide all */
  var code_overall_str = '<div class="code-fold-div">' + 
                            '<button class="code-hide-all">Hide All Code</button>' +
                            '<button class="code-show-all">Show All Code</button>' +
                        '</div>'
  $("#notebook-container").prepend(code_overall_str)

  var section_inputs = $(".input");
  var section_buttons = $(".code-fold-btn");
  $(".code-hide-all").on("click", function() {
      setCodeToHide(section_inputs, section_buttons);  
  })
  $(".code-show-all").on("click", function() {
      setCodeToShow(section_inputs, section_buttons);  
  })

  /* Default view is hidden */
  setCodeToHide(section_inputs, section_buttons, 0);

});