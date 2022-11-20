$(document).ready(function () {
  if (localStorage.getItem("user_type") != 0) {
    document.getElementById("drive-upload").classList.remove("d-none");
  }
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/drive",
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
        var venue = document.createElement("td");
        var maps = document.createElement("td");
        var date = document.createElement("td");
        var nameTextNode = document.createTextNode(
          response[i]["DONATION_DRIVE_NAME"]
        );
        name.appendChild(nameTextNode);
        var contactTextNode = document.createTextNode(
          response[i]["CONTACT_NO"]
        );
        contact.appendChild(contactTextNode);
        var dateTextNode = document.createTextNode(response[i]["DATE"]);
        date.appendChild(dateTextNode);
        var venueTextNode = document.createTextNode(response[i]["VENUE"]);
        venue.appendChild(venueTextNode);
        var mapsTextNode = document.createTextNode(response[i]["GMAPS_LINK"]);
        maps.appendChild(mapsTextNode);
        row.appendChild(name);
        row.appendChild(contact);
        row.appendChild(venue);
        row.appendChild(maps);
        row.appendChild(date);
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
  var date = document.getElementById("date").value;
  var venue = document.getElementById("venue").value;
  var gmaps = document.getElementById("gmaps").value;

  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/adddrive",
    datatype: "html",
    data: {
      name: name,
      email: email,
      ph_no: ph_no,
      date: date,
      venue: venue,
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
