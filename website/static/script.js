let date = new Date();
let year = date.getFullYear();

let copyright = document.getElementById("copyright");
if (copyright) {
  copyright.innerHTML = "&copy; " + year;
}

function deletePost(postId) {
    fetch("/delete-post", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }

// Enabling bootstrap tooltip
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})