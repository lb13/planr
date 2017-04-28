$('td:contains("True")').closest('tr').css('background-color','orange');

function calcGlh(){
    hrs = document.getElementById("id_wk_hrs").value;
    wks = document.getElementById("id_number_wks").value;
    document.getElementById("rec_glh").innerHTML = hrs * wks;
}

function showAss(){
  if ( document.getElementById("id_course_type").value == 'N' | document.getElementById("id_course_type").value == 'C') {
    document.getElementById("ass_aim").style.display = "block";
  }
  else {
    document.getElementById("ass_aim").style.display = "none";
  }
}

$("*").filter(function() { return !$(this).children().length; })
      .html(function(index, old) { return old.replace('True', '<span style="color: red" class="glyphicon glyphicon-exclamation-sign">'); });

$("*").filter(function() { return !$(this).children().length; })
      .html(function(index, old) { return old.replace('False', ''); });

      (function(document) {
      	'use strict';

      	var LightTableFilter = (function(Arr) {

      		var _input;

      		function _onInputEvent(e) {
      			_input = e.target;
      			var tables = document.getElementsByClassName(_input.getAttribute('data-table'));
      			Arr.forEach.call(tables, function(table) {
      				Arr.forEach.call(table.tBodies, function(tbody) {
      					Arr.forEach.call(tbody.rows, _filter);
      				});
      			});
      		}

      		function _filter(row) {
      			var text = row.textContent.toLowerCase(), val = _input.value.toLowerCase();
      			row.style.display = text.indexOf(val) === -1 ? 'none' : 'table-row';
      		}

      		return {
      			init: function() {
      				var inputs = document.getElementsByClassName('light-table-filter');
      				Arr.forEach.call(inputs, function(input) {
      					input.oninput = _onInputEvent;
      				});
      			}
      		};
      	})(Array.prototype);

      	document.addEventListener('readystatechange', function() {
      		if (document.readyState === 'complete') {
      			LightTableFilter.init();
      		}
      	});

      })(document);
