let edit = document.querySelectorAll(".edit");
let textarea = document.querySelectorAll(".textarea");
let textInput = document.querySelectorAll(".input")

edit.forEach(function(element) {
    element.addEventListener("click", function(e) {
        e.preventDefault();
        edit_handler(element);
    });
});

function editPost(id, post, post_title) {
    let form = new FormData();
    form.append("id", id);
    form.append("post", post.trim());
    form.append("post_title", post_title.trim());

    fetch("/edit_post/", {
        method: "POST",
        body: form,
    })
    .then((response) => {
        document.querySelector(`#post-content-${id}`).textContent = post;
        document.querySelector(`#post-content-${id}`).style.display = "block";
        document.querySelector(`#post-edit-${id}`).style.display = "none";
        document.querySelector(`#post-edit-${id}`).value = post.trim();
        document.querySelector(`#post-title-${id}`).textContent = post_title;
        document.querySelector(`#post-title-${id}`).style.display = "block";
        document.querySelector(`#post-title-edit-${id}`).style.display = "none";
        document.querySelector(`#post-title-edit-${id}`).value = post_title.trim();
    });
}

function edit_handler(element) {
    let id = element.getAttribute("data-id");
    let editBtn = document.querySelector(`#edit-btn-${id}`);
    if (editBtn.textContent === "Edit") {
        document.querySelector(`#post-title-${id}`).style.display = "none";
        document.querySelector(`#post-title-edit-${id}`).style.display = "block";
        document.querySelector(`#post-title-edit-${id}`).value = document.querySelector(`#post-title-${id}`).innerHTML;
        document.querySelector(`#post-content-${id}`).style.display = "none";
        document.querySelector(`#post-edit-${id}`).style.display = "block";
        document.querySelector(`#post-edit-${id}`).value = document.querySelector(`#post-content-${id}`).innerHTML;
        editBtn.textContent = "Save";
        editBtn.setAttribute("class", "btn btn-success mt-2 edit");
    } else if (editBtn.textContent === "Save") {
        let postContent = document.querySelector(`#post-edit-${id}`).value;
        let titleContent = document.querySelector(`#post-title-edit-${id}`).value;
        editPost(id, postContent, titleContent);
        editBtn.textContent = "Edit";
        editBtn.setAttribute("class", "btn btn-primary mt-2 edit");   
    }
}