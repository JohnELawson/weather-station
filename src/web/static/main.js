window.addEventListener('load', function() {
    console.log('Page loaded');
    main();
});

API_BASE = "http://127.0.0.1:5000";
CURRENT_ENDPOINT = API_BASE + "/current_weather/";


async function main(){

    const data = await getApi(CURRENT_ENDPOINT);
    document.getElementById("temp").innerHTML = data.temp + "°C";
    document.getElementById("pressure").innerHTML = data.pressure + " hPa";
    document.getElementById("humidity").innerHTML = data.humidity + "%";
    document.getElementById("wind_speed").innerHTML = data.wind_speed + "km/h";
    document.getElementById("wind_dir").innerHTML = data.wind_direction;
    document.getElementById("temp_min").innerHTML = data.temp_min + "°C";
    document.getElementById("temp_max").innerHTML = data.temp_max + "°C";
}

async function getApi(url){
    const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Access-Control-Allow-Origin':'*'
        }
    })
    const data = await response.json();
    console.log(data);
    return data;
}
