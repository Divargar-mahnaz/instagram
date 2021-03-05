var followers_modal = document.getElementById("my-followers-Modal");
var followers_btn = document.getElementById("my-followers-Btn");
var followers_span = document.getElementsByClassName("close")[0];
followers_btn.onclick = function () {
    followers_modal.style.display = "block";
}
followers_span.onclick = function () {
    followers_modal.style.display = "none";
}
window.onclick = function (event) {
    if (event.target == followers_modal) {
        followers_modal.style.display = "none";
    }
}
// **************************************************************
var following_modal = document.getElementById("my-following-Modal");
var following_btn = document.getElementById("my-following-Btn");
var following_span = document.getElementsByClassName("close")[1];
following_btn.onclick = function () {
    following_modal.style.display = "block";
}
following_span.onclick = function () {
    following_modal.style.display = "none";
}
window.onclick = function (event) {
    if (event.target == following_modal) {
        following_modal.style.display = "none";
    }
}