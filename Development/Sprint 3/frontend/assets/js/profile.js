$(document).ready(function () {
  document.getElementById("name-prof").innerHTML = localStorage.getItem("name");
  document.getElementById("type").innerHTML = localStorage.getItem("plasma");

  if (localStorage.getItem("user_type") == 2) {
    document.getElementById("user-verify").classList.remove("d-none");
    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:5000/user",
      datatype: "html",
      data: {
        email: localStorage.getItem("email"),
      },
      success: function (response) {
        var table = document.getElementById("hostable");
        for (var i in response) {
          var row = document.createElement("tr");
          var name = document.createElement("td");
          var email = document.createElement("td");
          var type = document.createElement("td");
          var verify = document.createElement("td");
          var nameTextNode = document.createTextNode(response[i]["NAME"]);
          name.appendChild(nameTextNode);
          var emailTextNode = document.createTextNode(response[i]["EMAIL"]);
          email.appendChild(emailTextNode);
          if (response[i]["USER_TYPE"] == 0) {
            var typeTextNode = document.createTextNode("Individual");
          }
          if (response[i]["USER_TYPE"] == 1) {
            var typeTextNode = document.createTextNode("Hospital");
          }
          type.appendChild(typeTextNode);
          var verbtn = document.createElement("button");
          verbtn.innerHTML = "Verify";
          verbtn.classList.add("ver-btn");
          verify.appendChild(verbtn);
          row.appendChild(name);
          row.appendChild(email);
          row.appendChild(type);
          row.appendChild(verify);
          table.appendChild(row);
        }
      },
      error: function (error) {},
    });
  }
});
