
// Get the modal
var folder_modal = document.getElementById('add_folder_modal');

// Get the button that opens the modal
var folder_btn = document.getElementById("add_folder_btn");

// Get the <span> element that closes the modal
var folder_span = document.getElementsByClassName("folder_close_btn")[0];

// When the user clicks the button, open the modal 
folder_btn.onclick = function() {
  folder_modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
folder_span.onclick = function() {
  folder_modal.style.display = "none";
}


// Get the modal
var file_modal = document.getElementById('add_file_modal');

// Get the button that opens the modal
var file_btn = document.getElementById("add_file_btn");

// Get the <span> element that closes the modal
var file_span = document.getElementsByClassName("file_close_btn")[0];

// When the user clicks the button, open the modal 
file_btn.onclick = function() {
  file_modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
file_span.onclick = function() {
  file_modal.style.display = "none";
}



// Get the modal
var del_modal = document.getElementById('del_modal');

// Get the button that opens the modal
var del_btn = document.getElementById("del_btn");

// Get the <span> element that closes the modal
var del_span = document.getElementsByClassName("del_close_btn")[0];

// When the user clicks the button, open the modal 
del_btn.onclick = function() {
  del_modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
del_span.onclick = function() {
  del_modal.style.display = "none";
}