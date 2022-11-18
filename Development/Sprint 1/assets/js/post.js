$("#post-button").click(function (event) {
  event.preventDefault();
  document.getElementById("post-loader").style.visibility = "visible";
  document.getElementById("post-button").disabled = true;
  document.getElementById("post-fill-fail").classList.add("d-none");
  document.getElementById("post-fail").classList.add("d-none");
  document.getElementById("post-success").classList.add("d-none");
  if ($("#form-post")[0].checkValidity()) {
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
          var username = localStorage.username;
          var title = document.getElementById("title-post").value;
          var link = document.getElementById("link-post").value;
          var time = document.getElementById("time-post").value;
          var desc = document.getElementById("description-post").value;
          $.ajax({
            type: "POST",
            url: "/post_upload",
            datatype: "html",
            data: {
              username: username,
              title: title,
              link: link,
              time: time,
              desc: desc,
            },
            success: function (response) {
              // console.log(response);
              if (response == "failed") {
                document.getElementById("post-fail").classList.remove("d-none");
                document.getElementById("post-button").disabled = false;
                document.getElementById("post-loader").style.visibility =
                  "hidden";
              } else {
                document
                  .getElementById("post-success")
                  .classList.remove("d-none");
                document.getElementById("post-button").disabled = false;
                document.getElementById("post-loader").style.visibility =
                  "hidden";
              }
            },
            error: function (error) {},
          });
        } else {
          window.location.pathname = "/logout.html";
          localStorage.clear;
        }
      },

      error: function (error) {},
    });
  } else {
    document.getElementById("post-fill-fail").classList.remove("d-none");
    document.getElementById("post-button").disabled = false;
    document.getElementById("post-loader").style.visibility = "hidden";
  }
});
