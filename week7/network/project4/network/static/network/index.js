document.addEventListener("DOMContentLoaded", function(){

    //Default load index page 
    all_post();
    //document.querySelector("#all_posts").innerHTML = "All posts ...";
});

function all_post(){
    fetch('/all_post')
    .then(response => response.json())
    .then(posts => {
        posts.forEach(function(post){
            
            const owner = post["owner"];
            const content = post["content"];
            const timestamp = post["timestamp"];
            const likes = post["likes"];
            const number_of_likes = likes.length;
            
            const post_element = document.createElement('div');
            post_element.className ="card";


            const owner_header_post_element = document.createElement('div');
            owner_header_post_element.className = "card-header";
            owner_header_post_element.innerHTML =`${owner}`;
            post_element.appendChild(owner_header_post_element);

            const body_post_element = document.createElement('div');
            body_post_element.className = "card-body";

            const content_post_element = document.createElement('div');
            content_post_element.className = "card-text";
            content_post_element.innerHTML = `
            ${content}
            <br>
            ${timestamp}
            <br>
            Number of likes: ${number_of_likes}
            `;
            body_post_element.appendChild(content_post_element);

            post_element.appendChild(body_post_element);

            document.querySelector("#all_posts").append(post_element);
        });
    });
}



