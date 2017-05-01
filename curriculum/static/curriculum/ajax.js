$(function(){

  $('#id_qual_aim').keyup(function() {

    $.ajax({
      type: "POST",
      url: "/search/",
      data: {
        'search_text' : $('#id_qual_aim').val(),
        'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
      },
      success: searchSuccess,
      dataType: 'html'
    });

  });

});

function searchSuccess(data, textStatus, jqXHR)
{
  $('#search-results').html(data);
}
