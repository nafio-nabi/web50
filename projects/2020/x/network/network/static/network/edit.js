let edit = document.querySelectorAll(".edit");
let textarea = document.querySelectorAll(".textarea");

edit.forEach(function(element) {
    element.addEventListener("click", function(e) {
        e.preventDefault();
        edit_handler(element);
    });
});

function editPost(id, post) {
    let form = new FormData();
    form.append("id", id);
    form.append("post", post.trim());

    fetch("/edit_post/", {
        method: "POST",
        body: form,
    })
    .then((response) => {
        document.querySelector(`#post-content-${id}`).textContent = post;
        document.querySelector(`#post-content-${id}`).style.display = "block";
        document.querySelector(`#post-edit-${id}`).style.display = "none";
        document.querySelector(`#post-edit-${id}`).value = post.trim();
    });
}

function edit_handler(element) {
    let id = element.getAttribute("data-id");
    let editBtn = document.querySelector(`#edit-btn-${id}`);
    if (editBtn.textContent === "Edit") {
        document.querySelector(`#post-content-${id}`).style.display = "none";
        document.querySelector(`#post-edit-${id}`).style.display = "block";
        document.querySelector(`#post-edit-${id}`).value = document.querySelector(`#post-content-${id}`).innerHTML;
        editBtn.textContent = "Save";
        editBtn.setAttribute("class", "btn btn-success edit");
    } else if (editBtn.textContent === "Save") {
        let postContent = document.querySelector(`#post-edit-${id}`).value;
        editPost(id, postContent);
        editBtn.textContent = "Edit";
        editBtn.setAttribute("class", "btn btn-primary edit");   
    }
}