$(document).ready(function () {
  document.getElementById("user-name").innerHTML = localStorage.getItem("name");
  document.getElementById("user-head").classList.remove("d-none");
});

$("#post-button").click(function (event) {
  event.preventDefault();
  $("#post-fail").addClass("d-none");
  $("#post-success").addClass("d-none");
  document.getElementById("post-button").innerHTML =
    ' <div class="spinner-dot"><div class="dot1"></div><div class="dot2"></div></div>';
  document.getElementById("post-button").disabled = true;
  var name = document.getElementById("name").value;
  var email = localStorage.getItem("email");
  var ph_no = document.getElementById("number").value;
  var plasma = document.getElementById("plasma").value;
  var hospital = document.getElementById("hospital").value;
  var gmaps = document.getElementById("gmaps").value;

  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/addplasma",
    datatype: "html",
    data: {
      name: name,
      email: email,
      ph_no: ph_no,
      plasma: plasma,
      hospital: hospital,
      gmaps: gmaps,
    },
    success: function (response) {
      if (response != "failed") {
        document.getElementById("post-success").classList.remove("d-none");
        setTimeout(() => {
          location.reload;
        }, 600);
      } else {
        document.getElementById("post-fail").classList.remove("d-none");
        document.getElementById("post-button").innerHTML = "Submit";
        document.getElementById("post-button").disabled = false;
      }
    },
    error: function (error) {},
  });
});
