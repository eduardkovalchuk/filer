// AJAX for posting
function search() {
  console.log("search is working!") // sanity check
  $.ajax({
    url : "/ajax_search/", // the endpoint
    type : "POST", // http method
    data : { search_text : $('#search-text').val() }, // data sent with the post request

    // handle a successful response
    success : function(json) {
        $('#search-text').val(''); // remove the value from the input
        console.log(json); // log the returned json to the console
        console.log("success"); // another sanity check
    },

    // handle a non-successful response
    error : function(xhr,errmsg,err) {
        $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
});
};


// Submi search on submit
$('#search-form').on('submit', function(event){
  event.preventDefault();
  console.log("form submitted!")  // sanity check
  search();
});
