document.addEventListener("DOMContentLoaded", function(){

    // Upload a post
    document.querySelector("#new_post_form").addEventListener("submit", upload_post);
});

function upload_post(event)
{
    
    // Prevent the event to be submitted and show the result in console 
    event.preventDefault();

    // Select the element from the HTML
    content = document.querySelector("#post_content");

    fetch("/post", {
        method: "POST",
        body: JSON.stringify({
            content: content.value
        })
    })
    .then(response => response.json())
    .then(result => {
        //Print the reuslt 
        console.log(result);
    })
}
