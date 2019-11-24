window.addEventListener('load', function() {
    console.log('Page loaded');
    main();
});

API_BASE = "http://127.0.0.1:5000";
CURRENT_ENDPOINT = API_BASE + "/current_weather/";


async function main(){

    get_current_weather();
}

async function get_current_weather(){
    const data = await getApi(CURRENT_ENDPOINT);
    for(const [key, value] of Object.entries(data)) {
        console.log(key, value);
        document.getElementById("current_" + key).innerHTML = value;
    }
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
