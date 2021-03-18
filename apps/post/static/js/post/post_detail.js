var likemodal = document.getElementById("Like_Modal")
var likebtn = document.getElementById("like_Btn");
var likespan = document.getElementsByClassName("close")[0];
console.log(likespan)
likebtn.onclick = function () {
    likemodal.style.display = "block";
}
likespan.onclick = function () {
    likemodal.style.display = "none";
}

// *****************************************************
var comment_modal = document.getElementById("comment_Modal");
var comment_btn = document.getElementById("comment_Btn");
var comment_span = document.getElementsByClassName("close")[1];
comment_btn.onclick = function () {
    comment_modal.style.display = "block";
}
comment_span.onclick = function () {
    comment_modal.style.display = "none";
}
// ************************************************************
window.onclick = function (event) {
    if (event.target == comment_modal) {
        comment_modal.style.display = "none";
    }
    if (event.target == likemodal) {
        likemodal.style.display = "none";
    }
}
// ************************************************
