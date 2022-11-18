$(document).ready(function () {
  $.ajax({
    type: "POST",
    url: "/auth_status",
    datatype: "html",
    data: {
      username: localStorage.username,
      auth_token: localStorage.auth_token,
    },
    success: function (response) {
      if (response != "false") {
        localStorage.username = response[0][0];
        document.getElementById("user-name").innerHTML =
          response[0][3].toUpperCase();
        document.getElementById("user-username").innerHTML = response[0][0];
        document.getElementById("user-email").innerHTML =
          response[0][2].toLowerCase();
        document.getElementById("user-phone").innerHTML = response[0][4];
      } else {
        window.location.pathname = "/logout.html";
        localStorage.clear;
      }
    },

    error: function (error) {},
  });
});
$(".toggle-button").on("click", function () {
  $(".left-sidebar").toggleClass("minimize");
});
