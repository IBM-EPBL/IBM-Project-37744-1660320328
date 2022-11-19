$(document).ready(function () {
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/plasma",
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
