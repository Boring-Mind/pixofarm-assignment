const city_names = ["Helsinki", "Sydney", "Los Angeles", "Zhangjiajie"];
const continent_colors = {
  1: "#15449e",
  2: "#d48b62",
  3: "#6c4eb0",
  4: "#fef301",
  5: "#e50163",
  6: "#00a6d6",
};

const dates_labels = new Set();

var currentChart = undefined;

var city_temp_data = {
  Helsinki: {
    min_temp: [],
    mean_temp: [],
    max_temp: [],
    temperature: [],
    color: "",
    lat: 0,
    lng: 0,
  },
  Sydney: {
    min_temp: [],
    mean_temp: [],
    max_temp: [],
    temperature: [],
    color: "",
    lat: 0,
    lng: 0,
  },
  "Los Angeles": {
    min_temp: [],
    mean_temp: [],
    max_temp: [],
    temperature: [],
    color: "",
    lat: 0,
    lng: 0,
  },
  Zhangjiajie: {
    min_temp: [],
    mean_temp: [],
    max_temp: [],
    temperature: [],
    color: "",
    lat: 0,
    lng: 0,
  },
};

var currentCity = "";

function getCorrelation() {
  $.ajax({
    url: "http://0.0.0.0:8080/temperature/correlation/",
    dataType: "json",
    contentType: "application/json; charset=UTF-8",
  }).done(function (data) {
    $("#correlation-data").html(data["correlation"]);
  });
}

function findCityByLatLng(lat, lng) {
  for (city in city_temp_data) {
    if (city_temp_data[city].lat == lat && city_temp_data[city].lng == lng) {
      return city;
    }
  }
}

function getCityTemperature() {
  let queryParam = "?";
  for (const city in city_names) {
    if (queryParam != "?") {
      queryParam += `&city_names=${city_names[city]}`;
    } else {
      queryParam += `city_names=${city_names[city]}`;
    }
  }

  $.ajax({
    url: "http://0.0.0.0:8080/temperature/cities/" + queryParam,
    dataType: "json",
    contentType: "application/json; charset=UTF-8",
  }).done(function (data) {
    for (entry in data) {
      let city_name = data[entry].city.name;
      city_temp_data[city_name].min_temp.push(data[entry].min);
      city_temp_data[city_name].mean_temp.push(data[entry].mean);
      city_temp_data[city_name].max_temp.push(data[entry].max);
      city_temp_data[city_name].temperature.push(data[entry].min);
      city_temp_data[city_name].temperature.push(data[entry].mean);
      city_temp_data[city_name].temperature.push(data[entry].max);

      dates_labels.add(new Date(data[entry].date).toLocaleDateString("en-US"));

      city_temp_data[city_name].color =
        continent_colors[data[entry].city.continent_id.toString()];

      city_temp_data[city_name].lat = data[entry].city.latitude;
      city_temp_data[city_name].lng = data[entry].city.longitude;
    }

    setupGraph();
    initMap();
  });
}

function getData() {
  getCorrelation();
  getCityTemperature();
}

function setupGraph() {
  if (currentCity == "") {
    $(".weather-data-container").hide();
    return;
  }

  if (currentChart != undefined) {
    currentChart.destroy();
  }

  $(".weather-data-container").css("display", "flex");

  const labels = Array.from(dates_labels);
  const data = {
    labels: labels,
    datasets: [
      {
        label: "Temperature (min)",
        backgroundColor: "#264B96",
        borderColor: "#264B96",
        data: city_temp_data[currentCity].min_temp,
      },
      {
        label: "Temperature (mean)",
        backgroundColor: "#F9A73E",
        borderColor: "#F9A73E",
        data: city_temp_data[currentCity].mean_temp,
      },
      {
        label: "Temperature (max)",
        backgroundColor: "rgb(255, 99, 132)",
        borderColor: "rgb(255, 99, 132)",
        data: city_temp_data[currentCity].max_temp,
      },
    ],
  };

  const config = {
    type: "line",
    data: data,
    options: { responsive: true },
  };

  currentChart = new Chart(document.getElementById("chart"), config);
}

function initMap() {
  var mymap = L.map("map").setView([36.0, 14.1], 2);

  L.tileLayer(
    "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
    {
      attribution:
        'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: "mapbox/streets-v11",
      tileSize: 512,
      zoomOffset: -1,
      accessToken:
        "pk.eyJ1Ijoic29tZXVzZXIxMjMiLCJhIjoiY2t3ZGI2eXRiMjVoMzJ2cGFpOTNjcnhocCJ9.nH74RwC0XZc_XAIggzervg",
    }
  ).addTo(mymap);

  for (const city in city_names) {
    let circle = L.circle(
      [
        city_temp_data[city_names[city]].lat,
        city_temp_data[city_names[city]].lng,
      ],
      {
        color: city_temp_data[city_names[city]].color,
        fillColor: city_temp_data[city_names[city]].color,
        fillOpacity: 0.5,
        radius: 50000,
      }
    )
      .addTo(mymap)
      .on("click", function (e) {
        currentCity = findCityByLatLng(e.latlng.lat, e.latlng.lng);
        setupGraph();
      });
  }
}

function main() {
  getData();
}

document.addEventListener("DOMContentLoaded", main, false);
