function destroyGraph(){
    var a = document.getElementsByClassName("container");
    a[a.length - 1].outerHTML = "";
    delete a;
    
    var div1 = document.createElement('div');
    div1.setAttribute("class", "container");
    var div2 = document.createElement('div');
    div2.setAttribute("class", "jumbotron");
    var svg = document.createElement('svg');
    svg.setAttribute("id", "visualisation");
    svg.setAttribute("width", 1000);
    svg.setAttribute("height", 500);
    div2.appendChild(svg);
    div1.appendChild(div2);
    document.body.appendChild(div1);
    
    console.log("you destroyed the graph!");
}

destroyGraph();