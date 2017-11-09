var map;
var heatmap_data = [
    {begin_lat: 32.94, begin_lon: -82.2, end_lat: 32.94, end_lon: -82.2, radius: 2},
    {begin_lat: 33.9872, begin_lon: -81.0437, end_lat: 34.0057, end_lon: -81.0135, radius: 1},
    {begin_lat: 34.09, begin_lon: -80.95, end_lat: 34.101, end_lon: -80.9493, radius: 2},
    {begin_lat: 27.79, begin_lon: -82.59, end_lat: 27.8, end_lon: -82.59, radius: 4},
    {begin_lat: 36.1609, begin_lon: -86.6054, end_lat: 36.1723, end_lon: -86.6008, radius: 1},
    {begin_lat: 37.78, begin_lon: -98.02, end_lat: 37.7801, end_lon: -98.0082, radius: 1}/*,
    {begin_lat: 32.94,begin_lon: -82.2,end_lat: 32.94 ,end_lon: -82.2, radius: 2},
    {begin_lat: 32.94,begin_lon: -82.2,end_lat: 32.94 ,end_lon: -82.2, radius: 2},
    {begin_lat: 32.94,begin_lon: -82.2,end_lat: 32.94 ,end_lon: -82.2, radius: 2},
    {begin_lat: 32.94,begin_lon: -82.2,end_lat: 32.94 ,end_lon: -82.2, radius: 2},
    {begin_lat: 32.94,begin_lon: -82.2,end_lat: 32.94 ,end_lon: -82.2, radius: 2}*/
];
/*
function getSlope(data){
    var stuff = ((data.end_lat - data.begin_lat) / (data.end_lon - data.begin_lon));
    return stuff;
}

function getOffset(data, slope){
    var stuff = (data.begin_lat - (slope * data.begin_lon));
    return stuff;
}
*/
function getLine(data){
    var return_data = [];
    var _slope = getSlope(data);
    var _offset = getOffset(data, _slope);
    for(var j = 0; j < 11; j++){
        var x = data.begin_lon + (data.end_lon - data.begin_lon)*(j/10);
        var y = (_slope * x) + _offset;
        var data_object = {location: new google.maps.LatLng(y,x), weight: data.radius};
        return_data.push(data_object);
    }
    return return_data;
}

function initMap() {
    var table = document.getElementById("table");
    var coordinate_array = [];
    var line = [];
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: {lat: 41.850033, lng: -87.6500523},
        mapTypeId: 'terrain'
    });
    /*for(var i = 0; i < heatmap_data.length; i++){
        coordinate_array = coordinate_array.concat(getLine(heatmap_data[i]));
    }*/
    
    /*
    var object = {begin_lat: null, begin_lon: null, end_lat: null; end_lon: null: radius: null}
    heatmap_data = [];
    for(var i = 1; i < table.rows.length; i++){
        object_array.push(object);
    }
    
    for(var i = 0; i<table.rows[0].cells.length; i++){
        switch(table.rows[0].cells[i].innerHTML){
            case "BEGIN_LAT":
                for(var j = 1; j < table.rows.length; j++){
                    heatmap_data[j].begin_lat = table.rows[j].cells[i].innerHTML;
                }
                break;
            case "BEGIN_LON":
                for(var j = 1; j < table.rows.length; j++){
                    heatmap_data[j].begin_lon = table.rows[j].cells[i].innerHTML;
                }
                break;
            case "END_LAT":
                for(var j = 1; j < table.rows.length; j++){
                    heatmap_data[j].end_lat = table.rows[j].cells[i].innerHTML;
                }
                break;
            case "END_LAT":
                for(var j = 1; j < table.rows.length; j++){
                    heatmap_data[j].end_lat = table.rows[j].cells[i].innerHTML;
                }
                break;
            case "BEGIN_RANGE" || "END_RANGE":
                for(var j = 1; j < table.rows.length; j++){
                    heatmap_data[j].radius = table.rows[j].cells[i].innerHTML;
                }
                break;
            default:
                break;
        }
        
        
        
    }
    */
    
    for(var i = 0; i<heatmap_data.length; i++){
        coordinate_array.push({location: new google.maps.LatLng(heatmap_data[i].begin_lat, heatmap_data[i].begin_lon), weight: heatmap_data[i].radius});
        coordinate_array.push({location: new google.maps.LatLng(heatmap_data[i].end_lat, heatmap_data[i].end_lon), weight: heatmap_data[i].radius});
        
    }
    var heatmap = new google.maps.visualization.HeatmapLayer({
        data: coordinate_array,
        map: map,
        dissipating: false,
        opacity: .75,
        radius: 0.1
    });
    //heatmap.setMap(map);
}