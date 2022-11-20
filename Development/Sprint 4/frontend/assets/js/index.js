$(document).ready(function () {
  document.getElementById("user-name").innerHTML = localStorage.getItem("name");
  document.getElementById("user-head").classList.remove("d-none");
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/userplasma",
    datatype: "html",
    data: {
      email: localStorage.getItem("email"),
    },
    success: function (response) {
      var table = document.getElementById("hostable");
      for (var i in response) {
        var row = document.createElement("tr");
        var name = document.createElement("td");
        var contact = document.createElement("td");
        var plasma = document.createElement("td");
        var hospital = document.createElement("td");
        var maps = document.createElement("td");
        var status = document.createElement("td");
        var nameTextNode = document.createTextNode(response[i]["NAME"]);
        name.appendChild(nameTextNode);
        var contactTextNode = document.createTextNode(
          response[i]["CONTACT_NO"]
        );
        contact.appendChild(contactTextNode);
        var plasmaTextNode = document.createTextNode(
          response[i]["PLASMA_REQUIRED"]
        );
        plasma.appendChild(plasmaTextNode);
        var hospitalTextNode = document.createTextNode(response[i]["HOSPITAL"]);
        hospital.appendChild(hospitalTextNode);
        var mapsTextNode = document.createTextNode(response[i]["GMAPS_LINK"]);
        maps.appendChild(mapsTextNode);
        var statusTextNode = document.createTextNode("Active");
        status.appendChild(statusTextNode);
        row.appendChild(name);
        row.appendChild(contact);
        row.appendChild(plasma);
        row.appendChild(hospital);
        row.appendChild(maps);
        row.appendChild(status);
        table.appendChild(row);
      }
    },
    error: function (error) {},
  });
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
