window.addEventListener('load', function() {
    console.log('Page loaded');
    main();
});

const API_BASE = "http://127.0.0.1:5000";
const CURRENT_ENDPOINT = API_BASE + "/current_weather/";
const FORCAST_ENDPOINT = API_BASE + "/forcast_weather/";
const INDOORS_ENDPOINT = API_BASE + "/indoors_weather/";
const API_IMAGE = "https://openweathermap.org/img/wn/";

var indoor_temp_max = -99999;
var indoor_temp_min = 99999;


async function main(){
    // first init
    displayDate();
    get_current_weather();
    get_indoors_weather();

    // timers
    var dateTimer = setInterval(displayDate,1000);
    var currentWeatherTimer = setInterval(get_current_weather,10000);
    var indoorsWeatherTimer = setInterval(get_indoors_weather,10000);

    // get_forcast_weather();
    
}

async function get_current_weather(){
    console.log("checking for current weather");
    const data = await getApi(CURRENT_ENDPOINT);
    // console.log(data)
    setHtml("current_temp", data.temp + " ");
    setHtml("current_description", data.description)
    setHtml("current_pressure", data.pressure);
    setHtml("current_humidity", data.humidity);
    setHtml("current_wind_speed", data.wind_speed);
    setHtml("current_wind_direction", data.wind_direction);
    setHtml("current_temp_max", data.temp_max);
    setHtml("current_temp_min", data.temp_min);
    
    document.getElementById("current_weather_icon").src = API_IMAGE + data.img_id + "@2x.png";
}

async function get_indoors_weather(){
    console.log("checking for indoors weather");
    const data = await getApi(INDOORS_ENDPOINT);
    console.log(data)

    if(data.temp > indoor_temp_max){
        indoor_temp_max = data.temp;
    }
    if(data.temp < indoor_temp_min){
        indoor_temp_min = data.temp;
    }

    setHtml("indoor_temp", data.temp);
    setHtml("indoor_humidity", data.humidity);
    setHtml("indoor_pressure", data.pressure);
    setHtml("indoor_temp_max", indoor_temp_max);
    setHtml("indoor_temp_min", indoor_temp_min);
}

// async function get_forcast_weather(){
//     console.log("checking for forcast weather");
//     const data = await getApi(FORCAST_ENDPOINT);
//     console.log(data)
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
