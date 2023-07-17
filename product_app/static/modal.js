// Get the modal element
var modal = document("myModal");

// Get the button that opens the modal
var btn = document("updateBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Submit the form using AJAX
var form = document("updateForm");
form.addEventListener("submit", function(event) {
    event();
    
    var formData = new FormData(form);
    var xhr = new();
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState ===.DONE) {
            if (xhr.status === 200) {
 // Success message or redirect to another page
 console.log(xhr.responseText);
                modal.style.display = "none";
            } else {
 // Error handling
                console.error(xhr.responseText);
            }
        }
    };
    
    xhr.open(form.method, form.action, true);
    xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
    xhr.send(formData);
});
