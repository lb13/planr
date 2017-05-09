$('td:contains("True")').closest('tr').css('background-color','#f7df72');

function calcGlh(){
    hrs = document.getElementById("id_wk_hrs").value;
    wks = document.getElementById("id_number_wks").value;
    document.getElementById("rec_glh").innerHTML = hrs * wks;
}

function show(id){
  document.getElementById(id).style.display = 'block';
}

function toggle(id){
  if ( document.getElementById(id).style.display == 'block' ) {
    document.getElementById(id).style.display = 'none';
  }
  else {
    document.getElementById(id).style.display = 'block';
  }
}

function clearSearch(){
  document.getElementById("search-results").innerHTML = "--type a qual aim to begin--";
}

function showTimes(){
  if ( document.getElementById("id_course_delivery").value == 'FT' | document.getElementById("id_course_delivery").value == 'APP') {
    document.getElementById("times").style.display = "none";
  }
  else {
    document.getElementById("times").style.display = "block";
  }
}

function showDetails(){
  if ( document.getElementById("id_course_delivery").value == 'L2L' ) {
    document.getElementById("qualDetails").style.display = "none";
    document.getElementById("id_course_type").value = "S";
  }
  else {
    document.getElementById("qualDetails").style.display = "block";
  }
}

function showDay() {
  if ( document.getElementById("id_course_delivery").value == 'FT' | document.getElementById("id_course_delivery").value == 'APP') {
    document.getElementById("day").style.display = "none";
  }
  else {
    document.getElementById("day").style.display = "block";
  }
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
