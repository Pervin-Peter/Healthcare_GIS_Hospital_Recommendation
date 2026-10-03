// ======================================
// AI Healthcare GIS Project
// app.js
// ======================================


// ======================================
// CREATE MAP
// ======================================

var map = L.map("map").setView(
    [13.0827, 80.2707],
    13
);
// ======================================
// MAP DISPLAY PRIORITY
// ======================================

map.createPane("hospitalPane");
map.getPane("hospitalPane").style.zIndex = 650;

map.createPane("facilityPane");
map.getPane("facilityPane").style.zIndex = 500;

map.createPane("recommendationPane");
map.getPane("recommendationPane").style.zIndex = 700;

// ======================================
// OPEN STREET MAP
// ======================================

L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution: "© OpenStreetMap contributors"
    }
).addTo(map);


// ======================================
// CREATE LAYERS
// ======================================

var hospitalLayer = L.layerGroup();

var busStopLayer = L.layerGroup();

var clinicLayer = L.layerGroup();

var pharmacyLayer = L.layerGroup();

var railwayLayer = L.layerGroup();

var recommendationLayer = L.layerGroup();


// Add layers to map

map.addLayer(hospitalLayer);
map.addLayer(busStopLayer);
map.addLayer(clinicLayer);
map.addLayer(pharmacyLayer);
map.addLayer(railwayLayer);
map.addLayer(recommendationLayer);


// ======================================
// LAYER CONTROL
// ======================================

L.control.layers(
    null,
    {
        "🏥 Hospitals": hospitalLayer,
        "🚌 Bus Stops": busStopLayer,
        "🏥 Clinics": clinicLayer,
        "💊 Pharmacies": pharmacyLayer,
        "🚉 Railway Stations": railwayLayer,
        "🟢 Recommended Hospitals": recommendationLayer
    }
).addTo(map);


// ======================================
// PATIENT MARKER
// ======================================

var patientMarker = null;

// ======================================
// GET DIRECTIONS TO HOSPITAL
// ======================================

window.openDirections = function(hospitalLat, hospitalLon) {

    if (patientMarker === null) {

        alert(
            "Please click on the map to select your patient location first."
        );

        return;
    }

    var patientLocation = patientMarker.getLatLng();

    var patientLat = patientLocation.lat;
    var patientLon = patientLocation.lng;

    var directionsUrl =
        "https://www.google.com/maps/dir/?api=1" +
        "&origin=" +
        encodeURIComponent(
            patientLat + "," + patientLon
        ) +
        "&destination=" +
        encodeURIComponent(
            hospitalLat + "," + hospitalLon
        );

    window.open(
        directionsUrl,
        "_blank"
    );
};

// ======================================
// HELPER FUNCTION
// FIND LATITUDE
// ======================================

function getLatitude(item) {

    return parseFloat(
        item.Latitude ||
        item.latitude ||
        item.LATITUDE ||
        item.lat ||
        item.Lat
    );
}


// ======================================
// HELPER FUNCTION
// FIND LONGITUDE
// ======================================

function getLongitude(item) {

    return parseFloat(
        item.Longitude ||
        item.longitude ||
        item.LONGITUDE ||
        item.lon ||
        item.lng ||
        item.Lng
    );
}


// ======================================
// HELPER FUNCTION
// FIND NAME
// ======================================

function getName(item, type) {

    if (type === "hospital") {

        return (
            item.Hospital_Name ||
            item.Hospital ||
            "Hospital"
        );

    }

    return (
        item.Name ||
        item.name ||
        item.Clinic_Name ||
        item.Pharmacy_Name ||
        item.Station_Name ||
        item.Bus_Stop_Name ||
        item["Hospital_Name"] ||
        "Location"
    );
}


// ======================================
// LOAD ALL HOSPITALS
// ======================================

fetch("/hospitals")
    .then(function(response) {

        console.log(
            "Hospital API Status:",
            response.status
        );

        if (!response.ok) {
            throw new Error(
                "Hospital API failed: " +
                response.status
            );
        }

        return response.json();
    })

    .then(function(data) {

        console.log(
            "TOTAL HOSPITALS RECEIVED:",
            data.length
        );

        if (!Array.isArray(data)) {

            throw new Error(
                "Hospital API did not return an array."
            );
        }

        var validHospitals = 0;

        data.forEach(function(hospital) {

            var lat = parseFloat(
                hospital.Latitude
            );

            var lon = parseFloat(
                hospital.Longitude
            );

            if (
                isNaN(lat) ||
                isNaN(lon)
            ) {

                console.warn(
                    "Hospital skipped - invalid coordinates:",
                    hospital
                );

                return;
            }

            var hospitalName =
                hospital.Hospital_Name ||
                hospital.Hospital ||
                "Hospital";

            // ----------------------------------
            // HOSPITAL MARKER
            // ----------------------------------

            var marker = L.circleMarker(
                [lat, lon],
                {
                    radius: 6,
                    color: "#8B0000",
                    fillColor: "#FF0000",
                    fillOpacity: 1,
                    weight: 2
                }
            );

           marker.bindPopup(

                "<div style='min-width:240px;'>" +

                "<h3 style='margin:0 0 10px 0;'>" +
                "🏥 " +
                hospitalName +
                "</h3>" +

                "<hr>" +

                "📍 <b>Latitude:</b> " +
                lat.toFixed(6) +

                "<br>" +

                "📍 <b>Longitude:</b> " +
                lon.toFixed(6) +

                "<br><br>" +

                "<button type='button' " +
                "onclick='window.openDirections(" +
                lat +
                "," +
                lon +
                ")' " +

                "style='width:100%; " +
                "padding:10px; " +
                "background:#1976d2; " +
                "color:white; " +
                "border:none; " +
                "border-radius:6px; " +
                "cursor:pointer; " +
                "font-size:14px;'>" +

                "🧭 Get Directions" +

                "</button>" +

                "</div>"

            );

            hospitalLayer.addLayer(marker);

            validHospitals++;
        });

        console.log(
            "VALID HOSPITALS DISPLAYED:",
            validHospitals
        );

        console.log(
            "Hospital layer count:",
            hospitalLayer.getLayers().length
        );

    })

    .catch(function(error) {

        console.error(
            "HOSPITAL LOADING ERROR:",
            error
        );

    });


// ======================================
// LOAD BUS STOPS
// ======================================

fetch("/busstops")

.then(function(response) {

    if (!response.ok) {

        throw new Error(
            "Bus Stop API failed: " +
            response.status
        );

    }

    return response.text();

})

.then(function(data) {
    data = JSON.parse(data.replace(/\bNaN\b/g, "null"));

    console.log(
        "Bus Stops Loaded:",
        data.length
    );
    var busStopDisplayed = 0;


    data.forEach(function(item) {

        var lat = getLatitude(item);

        var lon = getLongitude(item);


        if (
            isNaN(lat) ||
            isNaN(lon)
        ) {

            return;

        }


        var marker = L.circleMarker(
            [lat, lon],
            {
                radius: 2,
                color: "#FF8C00",
                fillColor: "#FFA500",
                fillOpacity: 0.8,
                weight: 1
            }
        );


        marker.bindPopup(

            "<b>🚌 Bus Stop</b><br>" +
            getName(item, "bus")

        );


        busStopLayer.addLayer(marker);
        busStopDisplayed++;

    });

})

.catch(function(error) {

    console.error(
        "Bus Stop Loading Error:",
        error
    );

});


// ======================================
// LOAD CLINICS
// ======================================

fetch("/clinics")

.then(function(response) {

    if (!response.ok) {

        throw new Error(
            "Clinic API failed: " +
            response.status
        );

    }

    return response.text();

})

.then(function(data) {
    data = JSON.parse(data.replace(/\bNaN\b/g, "null"));

    console.log(
        "Clinics Loaded:",
        data.length
    );
    var clinicDisplayed = 0;


    data.forEach(function(item) {

        var lat = getLatitude(item);

        var lon = getLongitude(item);


        if (
            isNaN(lat) ||
            isNaN(lon)
        ) {

            return;

        }


        var marker = L.circleMarker(
            [lat, lon],
            {
                radius: 3,
                color: "#800080",
                fillColor: "#BA55D3",
                fillOpacity: 0.8,
                weight: 1
            }
        );


        marker.bindPopup(

            "<b>🏥 Clinic</b><br>" +
            getName(item, "clinic")

        );


        clinicLayer.addLayer(marker);
        clinicDisplayed++;

    });

})

.catch(function(error) {

    console.error(
        "Clinic Loading Error:",
        error
    );

});


// ======================================
// LOAD PHARMACIES
// ======================================

fetch("/pharmacy")

.then(function(response) {

    if (!response.ok) {

        throw new Error(
            "Pharmacy API failed: " +
            response.status
        );

    }

    return response.json();

})

.then(function(data) {

    console.log(
        "Pharmacies Loaded:",
        data.length
    );
    var pharmacyDisplayed = 0;


    data.forEach(function(item) {

        var lat = getLatitude(item);

        var lon = getLongitude(item);


        if (
            isNaN(lat) ||
            isNaN(lon)
        ) {

            return;

        }


        var marker = L.circleMarker(
            [lat, lon],
            {
                radius: 3,
                color: "#0000FF",
                fillColor: "#00BFFF",
                fillOpacity: 0.8,
                weight: 1
            }
        );


        marker.bindPopup(

            "<b>💊 Pharmacy</b><br>" +
            getName(item, "pharmacy")

        );


        pharmacyLayer.addLayer(marker);
        pharmacyDisplayed++;

    });

})

.catch(function(error) {

    console.error(
        "Pharmacy Loading Error:",
        error
    );

});

// ======================================
// LOAD RAILWAY STATIONS
// ======================================

fetch("/railway")

.then(function(response) {

    if (!response.ok) {

        throw new Error(
            "Railway API failed: " +
            response.status
        );

    }

    return response.json();

})

.then(function(data) {

    console.log(
        "Railway Stations Loaded:",
        data.length
    );
    var railwayDisplayed = 0;


    data.forEach(function(item) {

        var lat = getLatitude(item);

        var lon = getLongitude(item);


        if (
            isNaN(lat) ||
            isNaN(lon)
        ) {

            return;

        }


        var marker = L.circleMarker(
            [lat, lon],
            {
                radius: 4,
                color: "#000000",
                fillColor: "#4169E1",
                fillOpacity: 0.9,
                weight: 2
            }
        );


        marker.bindPopup(

            "<b>🚉 Railway Station</b><br>" +
            getName(item, "railway")

        );


        railwayLayer.addLayer(marker);
        railwayDisplayed++;
    });

})

.catch(function(error) {

    console.error(
        "Railway Loading Error:",
        error
    );

});


// ======================================
// MAP CLICK
// ======================================

map.on("click", function(e) {


    console.log(
        "MAP CLICKED:",
        e.latlng.lat,
        e.latlng.lng
    );


    var latitude = e.latlng.lat;

    var longitude = e.latlng.lng;

    // ==================================
    // GET SELECTED MEDICAL SPECIALTY
    // ==================================

    var specialtySelect = document.getElementById("specialty");

    var selectedSpecialty = "";

    if (specialtySelect) {
        selectedSpecialty = specialtySelect.value;
    }

    console.log("Selected Specialty:", selectedSpecialty);

    // ==================================
    // GET SELECTED MEDICAL SPECIALTY
    // ==================================

    var specialtySelect =
        document.querySelector(
            "#specialty, #medicalSpecialty, select[name='specialty']"
        );

    var selectedSpecialty = "";

    if (specialtySelect) {

        selectedSpecialty =
            specialtySelect.value
            .trim()
            .toLowerCase();

    }

    console.log(
        "Selected Specialty:",
        selectedSpecialty
    );


    // ==================================
    // REMOVE OLD PATIENT MARKER
    // ==================================

    if (patientMarker !== null) {

        map.removeLayer(patientMarker);

    }


    // ==================================
    // REMOVE OLD RECOMMENDATIONS
    // ==================================

    recommendationLayer.clearLayers();


    // ==================================
    // ADD PATIENT MARKER
    // ==================================

    patientMarker = L.circleMarker(

        [
            latitude,
            longitude
        ],

        {

            radius: 10,

            color: "blue",

            fillColor: "blue",

            fillOpacity: 1,

            weight: 3

        }

    );


    patientMarker.addTo(map);


    patientMarker.bindPopup(

        "<b>📍 Patient Location</b><br>" +

        "Latitude: " +
        latitude.toFixed(6) +

        "<br>" +

        "Longitude: " +
        longitude.toFixed(6)

    );


    patientMarker.openPopup();


    // ==================================
    // RIGHT PANEL
    // ==================================

    var list =
        document.getElementById(
            "hospitalList"
        );


    if (list) {

        list.innerHTML = `

            <div class="instruction">

                ⏳ Finding nearest hospitals...

            </div>

        `;

    }


    // ==================================
    // CALL FLASK API
    // ==================================

    fetch(

        "/recommend",

        {

            method: "POST",

            headers: {

                "Content-Type":
                    "application/json"

            },

            body: JSON.stringify({

                latitude: latitude,

                longitude: longitude,

                specialty: selectedSpecialty

            })

        }

    )

    .then(function(response) {

        if (!response.ok) {

            throw new Error(
                "Recommendation API failed: " +
                response.status
            );

        }

        return response.json();

    })

    .then(function(data) {


        console.log(
            "Recommendations:",
            data
        );


        // ==================================
        // CHECK ERROR
        // ==================================

        if (data.error) {

            throw new Error(
                data.error
            );

        }


        // ==================================
        // CLEAR OLD RECOMMENDATIONS
        // ==================================

        recommendationLayer.clearLayers();


        if (list) {

            list.innerHTML = "";

        }


        // ==================================
        // TOP 5
        // ==================================

        var top5 =
            data.slice(0, 5);


        // ==================================
        // DISPLAY TOP 5
        // ==================================

        top5.forEach(function(
            hospital,
            index
        ) {


            var lat =
                getLatitude(hospital);


            var lon =
                getLongitude(hospital);


            // ==================================
            // GREEN RECOMMENDED MARKER
            // ==================================

            if (
                !isNaN(lat) &&
                !isNaN(lon)
            ) {

                var recommendedMarker =
                    L.circleMarker(
                        [lat, lon],
                        {
                            radius: 13,
                            color: "green",
                            fillColor: "lime",
                            fillOpacity: 1,
                            weight: 4
                        }
                    );


                // ==================================
                // RECOMMENDED HOSPITAL POPUP
                // ==================================

                var hospitalName =
                    hospital.Hospital || "Hospital";

                var hospitalDistance =
                    hospital["Distance (km)"] ?? "-";

                var distanceScore =
                    hospital["Distance Score"] ?? "-";

                var accessibilityScore =
                    hospital["Accessibility Score"] ?? "-";

                var specialtyScore =
                    hospital["Specialty Match Score"] ?? "-";

                var emergencyScore =
                    hospital["Emergency Score"] ?? "-";

                var healthcareTypeScore =
                    hospital["Healthcare Type Score"] ?? "-";

                var aiScore =
                    hospital["AI Score"] ?? "-";


                recommendedMarker.bindPopup(

                    "<div style='min-width:280px;'>" +

                        "<h3 style='margin:0 0 10px 0;'>" +
                            "🟢 #" +
                            (index + 1) +
                            " " +
                            hospitalName +
                        "</h3>" +

                        "<hr>" +

                        "📍 <b>Distance:</b> " +
                        hospitalDistance +
                        " km<br><br>" +

                        "📊 <b>Distance Score:</b> " +
                        distanceScore +
                        "<br>" +

                        "♿ <b>Accessibility:</b> " +
                        accessibilityScore +
                        "<br>" +

                        "🩺 <b>Specialty Match:</b> " +
                        specialtyScore +
                        "<br>" +

                        "🚑 <b>Emergency Score:</b> " +
                        emergencyScore +
                        "<br>" +

                        "🏥 <b>Healthcare Type:</b> " +
                        healthcareTypeScore +
                        "<br>" +

                        "🤖 <b>AI Score:</b> " +
                        aiScore +

                        "<br><br>" +

                        "<button " +
                            "onclick=\"openDirections(" +
                                lat +
                                "," +
                                lon +
                            ")\" " +

                            "style='" +
                                "width:100%;" +
                                "padding:10px;" +
                                "background:#1976d2;" +
                                "color:white;" +
                                "border:none;" +
                                "border-radius:6px;" +
                                "font-size:14px;" +
                                "font-weight:bold;" +
                                "cursor:pointer;" +
                            "'" +

                        ">" +

                            "🧭 Get Directions" +

                        "</button>" +

                    "</div>"

                );


                // ==================================
                // HOVER TOOLTIP
                // ==================================

                recommendedMarker.bindTooltip(

                    "#" +
                    (index + 1) +
                    " " +
                    hospital.Hospital,

                    {
                        direction: "top",
                        offset: [0, -10]
                    }

                );


                // ==================================
                // ADD TO RECOMMENDATION LAYER
                // ==================================

                recommendationLayer.addLayer(recommendedMarker);

            }


            // ==================================
            // RIGHT PANEL CARD
            // ==================================

            if (list) {

                var card =
                    document.createElement(
                        "div"
                    );

                card.className =
                    "hospital-card";

                card.style.cursor = "pointer";
                card.title = "Click to locate this hospital on the map";

                card.innerHTML = `

                    <div class="hospital-name">

                        🏥 ${index + 1}.
                        ${hospital.Hospital}

                    </div>


                    <div class="hospital-distance">

                        📍 Distance:
                        <b>
                            ${hospital["Distance (km)"]}
                            km
                        </b>

                    </div>


                    <div class="hospital-distance">

                        📊 Distance Score:
                        <b>
                            ${hospital["Distance Score"] ?? "-"}
                        </b>

                    </div>


                    <div class="hospital-distance">

                        ♿ Accessibility:
                        <b>
                            ${hospital["Accessibility Score"] ?? "-"}
                        </b>

                    </div>


                    <div class="hospital-distance">

                        🩺 Specialty Match:
                        <b>
                            ${hospital["Specialty Match Score"] ?? "-"}
                        </b>

                    </div>


                    <div class="hospital-distance">

                        🚑 Emergency Score:
                        <b>
                            ${hospital["Emergency Score"] ?? "-"}
                        </b>

                    </div>


                    <div class="hospital-distance">

                        🏥 Healthcare Type:
                        <b>
                            ${hospital["Healthcare Type Score"] ?? "-"}
                        </b>

                    </div>


                    <div class="hospital-distance">

                        🤖 AI Score:
                        <b>
                            ${hospital["AI Score"] ?? "-"}
                        </b>

                    </div>

                                `;


                // ==================================
                // CLICK CARD → FOCUS HOSPITAL
                // ==================================

                card.addEventListener("click", function() {

                    if (
                        !isNaN(lat) &&
                        !isNaN(lon)
                    ) {

                        map.setView(
                            [lat, lon],
                            15,
                            {
                                animate: true
                            }
                        );

                        if (recommendedMarker) {
                            recommendedMarker.openPopup();
                        }

                    }

                });


                list.appendChild(card);

                

            }

        }); 
        // ==================================
        // NO RESULTS
        // ==================================

        if (top5.length === 0 && list) {

            list.innerHTML = `

                <div class="instruction">

                    ❌ No hospitals found.

                </div>

            `;

        }

    })

    

    .catch(function(error) {


        console.error(
            "Recommendation Error:",
            error
        );

        // ==================================
        // GET DIRECTIONS
        // ==================================

        window.openDirections = function (
            hospitalLat,
            hospitalLon
        ) {

            console.log("Get Directions clicked");

            // Check patient location
            if (
                typeof patientMarker === "undefined" ||
                !patientMarker
            ) {

                alert(
                    "Please select a patient location first."
                );

                return;
            }

            // Get patient coordinates
            var patientLocation =
                patientMarker.getLatLng();

            var patientLat =
                patientLocation.lat;

            var patientLon =
                patientLocation.lng;

            console.log(
                "Patient:",
                patientLat,
                patientLon
            );

            console.log(
                "Hospital:",
                hospitalLat,
                hospitalLon
            );


            // Google Maps Directions URL
            var directionsUrl =
                "https://www.google.com/maps/dir/?api=1" +
                "&origin=" +
                encodeURIComponent(
                    patientLat + "," + patientLon
                ) +
                "&destination=" +
                encodeURIComponent(
                    hospitalLat + "," + hospitalLon
                );


            console.log(
                "Directions URL:",
                directionsUrl
            );


            // Open Google Maps
            window.location.href =
                directionsUrl;
        };
        if (list) {

            list.innerHTML = `

                <div class="instruction">

                    ❌ Unable to get recommendations.

                    <br><br>

                    ${error.message}

                </div>

            `;

        }

    });

});