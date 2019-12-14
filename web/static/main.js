window.addEventListener('load', function() {
    console.log('Page loaded');
    main();
});

API_BASE = "http://127.0.0.1:5000";
CURRENT_ENDPOINT = API_BASE + "/current_weather/";
FORCAST_ENDPOINT = API_BASE + "/forcast_weather/";
INDOORS_ENDPOINT = API_BASE + "/indoors_weather/";


async function main(){
    // first init
    displayDate();
    get_current_weather();
    get_indoors_weather();

    // timers
    var dateTimer = setInterval(displayDate,1000);
    var currentWeatherTimer = setInterval(get_current_weather,10000);

    // get_forcast_weather();
    
}

async function get_current_weather(){
    console.log("checking for current weather");
    const data = await getApi(CURRENT_ENDPOINT);
    // console.log(data)
    setHtml("current_temp", data.temp + " ");
    setHtml("current_description", data.description)
    setHtml("current_pressure", "Pressure: " + data.pressure);
    setHtml("current_humidity", "Humidity: " + data.humidity);
    setHtml("current_wind_speed", "Wind: " + data.wind_speed);
    setHtml("current_wind_direction", data.wind_direction);
    setHtml("current_temp_max", "Max: " + data.temp_max);
    setHtml("current_temp_min", "Min: " + data.temp_max);
}

async function get_indoors_weather(){
    console.log("checking for indoors weather");
    const data = await getApi(INDOORS_ENDPOINT);
    setHtml("indoor_temp", data.temp);
    setHtml("indoor_pressure", data.pressure);
}

// async function get_forcast_weather(){
    // console.log("checking for forcast weather");
//     const data = await getApi(FORCAST_ENDPOINT);

//     let forcast_html = "";
//     for(const [key, value] of Object.entries(data)) {
//         console.log(key, value);
//         forcast_html += "<div class='forcast_container'>" + value.temp + " °C</div>";
//     }
//     document.getElementById("forcast_weather_container").innerHTML = forcast_html;
// }

async function getApi(url){
    const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Access-Control-Allow-Origin':'*'
        }
    })
    const data = await response.json();
    // console.log(data);
    return data;
}

function displayDate(){
    const d = new Date();
    setHtml("current_time", d.toLocaleTimeString() + " - " + d.toDateString());
}

function setHtml(id, html){
    document.getElementById(id).innerHTML = html;
}