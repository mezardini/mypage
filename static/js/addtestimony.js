
var counter = 1;

function addNewElement() {
var elementContainer = document.getElementById("testimonyContainer");

// Create a new div element with the desired classes
var newDiv = document.createElement("div");
newDiv.className = "input-group mb-3";

// Create the span element for the Name
var newTitleSpan = document.createElement("span");
newTitleSpan.className = "input-group-text";
newTitleSpan.textContent = "Name " + (++counter);

// Create the input element for the Name
var newTitleInput = document.createElement("input");
newTitleInput.type = "text";
newTitleInput.className = "form-control";
newTitleInput.setAttribute("aria-label", "With textarea");
newTitleInput.name = "testimony_name";
newTitleInput.rows = "3";

// Create the span element for the testimony
var newDescriptionSpan = document.createElement("span");
newDescriptionSpan.className = "input-group-text";
newDescriptionSpan.textContent = "Testimony " + counter;

// Create the textarea element for the testimony
var newDescriptionTextarea = document.createElement("textarea");
newDescriptionTextarea.className = "form-control";
newDescriptionTextarea.setAttribute("aria-label", "With textarea");
newDescriptionTextarea.name = "testimony";
newDescriptionTextarea.rows = "6";

// Append the elements to the new div
newDiv.appendChild(newTitleSpan);
newDiv.appendChild(newTitleInput);
newDiv.appendChild(newDescriptionSpan);
newDiv.appendChild(newDescriptionTextarea);

// Append the new div to the container
elementContainer.appendChild(newDiv);
}
document.getElementById("myForm").addEventListener("submit", function(event) {
event.preventDefault();

var form = new FormData(this);

// Send the form data to the server using AJAX or other methods...
});

