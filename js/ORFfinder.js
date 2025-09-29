// this function executes our search via an AJAX call
function orfSearch( term ) {
    // hide and clear the previous results, if any
    $('#results').hide();
    $('tbody').empty();
    
    // transforms all the form parameters into a string we can send to the server
    var frmStr = $('#orf_search').serialize();
    
    $.ajax({
        url: './orf_search.cgi',
        dataType: 'json',
        data: frmStr,
        success: function(data, textStatus, jqXHR) {
            processJSON(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert("Failed to perform orf search! textStatus: (" + textStatus +
                  ") and errorThrown: (" + errorThrown + ")");
        }
    });
}

// this processes a passed JSON structure representing orfs found and draws it
//  to the result table
function processJSON( data ) {
    // set the span that lists the orf count
    $('#orf_count').text( data.orf_count );
    
    // this will be used to keep track of row identifiers
    var next_row_num = 1;
    
    // iterate over each orf and add a row to the result table for each
    $.each( data.orfs, function(i, item) {
        var this_row_id = 'result_row_' + next_row_num++;
    
        // create a row and append it to the body of the table
        $('<tr/>', { "id" : this_row_id } ).appendTo('tbody');
        
        $('<td/>', { "text" : item.orf_id } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.start } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.end } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.strand } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.frame } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.seq_len } ).appendTo('#' + this_row_id);
        $('<td/>', { "text" : item.description } ).appendTo('#' + this_row_id);

    });
    
    // now show the result section that was previously hidden, hide search form, and enable table sorting
    $('#results').show();
    $('#orf_search').hide();
    $("#myTable").tablesorter();
}

// run our javascript once the page is ready
$(document).ready( function() {

  $('#submit').click( function() {
        orfSearch();
        return false;  // prevents 'normal' form submission
  });
})
