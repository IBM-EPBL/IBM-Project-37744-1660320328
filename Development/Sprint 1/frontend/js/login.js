$("#login-button").click(function (event) {
  event.preventDefault();
  $("#in-user").addClass("d-none");
  $("#in-pass").addClass("d-none");
  document.getElementById("login-button").innerHTML =
    ' <div class="spinner-dot"><div class="dot1"></div><div class="dot2"></div></div>';
  document.getElementById("login-button").disabled = true;
  var username = document.getElementById("user-log").value;
  var pass = document.getElementById("pass-log").value;
  $.ajax({
    type: "POST",
    url: "/login",
    datatype: "html",
    data: {
      username: username,
      pass: pass,
    },
    success: function (response) {
      // console.log(response);
      if (response == "false") {
        document.getElementById("in-user").classList.remove("d-none");
        document.getElementById("login-button").innerHTML = "LOGIN";
        document.getElementById("login-button").disabled = false;
      } else {
        if (response == "failed") {
          document.getElementById("in-pass").classList.remove("d-none");
          document.getElementById("login-button").innerHTML = "LOGIN";
          document.getElementById("login-button").disabled = false;
        } else {
          localStorage.setItem("username", username);
          localStorage.setItem("auth_token", response);
          $("#form-login").fadeOut(500);
          $(".wrapper").addClass("form-success");
          setTimeout(() => {
            window.location.pathname = "/home.html";
          }, 5000);
        }
      }
    },
    error: function (error) {},
  });
});
$("#signup-button").click(function (event) {
  event.preventDefault();
  $("#field-check").addClass("d-none");
  $("#sign-unav").addClass("d-none");
  document.getElementById("signup-button").innerHTML =
    ' <div class="spinner-dot"><div class="dot1"></div><div class="dot2"></div></div>';
  document.getElementById("signup-button").disabled = true;
  if ($("#form-signup")[0].checkValidity()) {
    var username = document.getElementById("user-sign").value;
    var name = document.getElementById("user-name").value;
    var email = document.getElementById("user-email").value;
    var ph_no = document.getElementById("user-phone").value;
    var pass = document.getElementById("pass-sign").value;
    var re_pass = document.getElementById("re-pass").value;
    if (pass === re_pass && pass.length >= 8) {
      $.ajax({
        type: "POST",
        url: "/signup",
        datatype: "html",
        data: {
          username: username,
          name: name,
          email: email,
          ph_no: ph_no,
          pass: pass,
        },
        success: function (response) {
          if (response != "failed") {
            localStorage.setItem("username", username);
            localStorage.setItem("auth_token", response);
            $("#form-signup").fadeOut(500);
            $(".wrapper").addClass("form-success");
            setTimeout(() => {
              window.location.pathname = "/home.html";
            }, 5000);
          } else {
            document.getElementById("sign-unav").classList.remove("d-none");
            document.getElementById("signup-button").innerHTML = "SIGNUP";
            document.getElementById("signup-button").disabled = false;
          }
        },
        error: function (error) {},
      });
    } else {
      document.getElementById("signup-button").innerHTML = "SIGNUP";
      document.getElementById("signup-button").disabled = false;
      $("#pass-fail").removeClass("d-none");
    }
  } else {
    $("#field-check").removeClass("d-none");
    document.getElementById("signup-button").innerHTML = "SIGNUP";
    document.getElementById("signup-button").disabled = false;
  }
});
$("#user-sign").change(function (event) {
  document.getElementById("loader-user").classList.remove("d-none");
  $.ajax({
    type: "POST",
    url: "/username_check",
    datatype: "html",
    data: {
      username: document.getElementById("user-sign").value,
    },
    success: function (response) {
      if (response == "success") {
        document.getElementById("loader-user").classList.add("d-none");
        document.getElementById("user-unav").classList.add("d-none");
        document.getElementById("user-ava").classList.remove("d-none");
        document.getElementById("signup-button").disabled = false;
      } else if (response == "failed") {
        document.getElementById("loader-user").classList.add("d-none");
        document.getElementById("user-ava").classList.add("d-none");
        document.getElementById("user-unav").classList.remove("d-none");
        document.getElementById("signup-button").disabled = true;
      } else {
        document.getElementById("loader-user").classList.add("d-none");
        document.getElementById("sign-unav").classList.add("d-none");
        document.getElementById("signup-button").disabled = true;
      }
    },

    error: function (error) {},
  });
});

$("#signup-link").click(function (event) {
  event.preventDefault();
  $("#form-login").fadeOut(500);
  setTimeout(() => {
    document.getElementById("form-signup").style.display = "block";
  }, 600);
});
$("#login-link").click(function (event) {
  event.preventDefault();
  $("#form-signup").fadeOut(500);
  setTimeout(() => {
    document.getElementById("form-login").style.display = "block";
  }, 600);
});
