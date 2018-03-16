/*
  Style changes to Python iNotebook
  Copyright 2018: Lemuel Kumarga
*/

$(document).ready(function(){

  /* ============================================= 
    CSS Styles
  ============================================== */
    
  var is_notebook = $(".notebook_app").length;

  var css_files = [{'link': 'shared/css/defaults.css' },
                   {'link': '../../shared/css/definitions.css'},
                   {'link': '../../shared/css/general.css'},
                   {'link': 'shared/css/python.css'}]

  var js_files = [{'link': 'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js' },
                  {'link': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js', html_only : true},
                  {'link': 'shared/js/popover.js', html_only: true}];

  var h = $('head')
  $.each(css_files, function(i, css_file) {
    if (!("html_only" in css_file && css_file['html_only'] && !is_notebook)) {
      h.append('<link href="' + css_file['link'] + '" rel="stylesheet">')
    }
  })
  $.each(js_files, function(i, js_file) {
    if (!("html_only" in js_file && js_file['html_only'] && !is_notebook)) {
      h.append('<script src="' + js_file['link'] + '"></script>')
    }
  })

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