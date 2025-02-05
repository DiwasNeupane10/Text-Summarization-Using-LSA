
function loader(){
    let button=document.getElementById("summarizebutton");
    let span=document.createElement("span");
    // check if the button has a child with the given class name
    if (!button.querySelector(".spinner-border")) {
        // add the class name to the span so that it will be a bootstrap spinner
        span.classList.add("spinner-border","spinner-border-sm");
        span.setAttribute("role","status");
        span.setAttribute("aria-hidden","true");
        button.appendChild(span);
        // disable the button on form submittion
        button.disabled=true;
}
};
// pageshow is a event that is fired when the page is visible 
window.addEventListener('pageshow', function(event) {
    // Check if the page is being loaded from cache
    if (event.persisted) {
        resetbutton();
    }
});
// domcontentloaded is a event that fires when the html content has been parsed by the browser
window.addEventListener('DOMContentLoaded', function() {
    resetbutton();
});

function resetbutton() {
    let button = document.getElementById("summarizebutton");
    let spinner = button.querySelector(".spinner-border");
    button.disabled=false;
    // Remove the spinner if it exists
    if (spinner) {
        spinner.remove();
    }
};