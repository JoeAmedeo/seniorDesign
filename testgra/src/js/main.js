function toTitleCase(str)
{
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

function InitChart() {

    d3.json("test2.json", function(error, json){

        var oldData = json.result;
        var columns = json.result[0];

        console.log(oldData);
        console.log(columns);

        var data = [];

        for (var i = 1; i < oldData.length; i++){
            var row = oldData[i];
            var obj ={};
            obj[columns[0]] = row[0];
            obj[columns[1]] = row[1];
            obj[columns[2]] = row[2];
            obj[columns[3]] = row[3];
            data.push(obj)

        }

        var stateTitle = oldData[0][0];

        console.log(oldData.length);
        console.log(columns[1]);
        console.log(JSON.stringify(data));
        console.log(JSON.stringify(columns[1]));

        if(columns[1] == "stormType") {
            document.getElementById("title").innerHTML = "Frequency of Various Storms in " + oldData[1][0] + " from " + oldData[1][2] + "-" + oldData[oldData.length - 1][2];
        } else if(columns[1] == "state"){
            document.getElementById("title").innerHTML = "Frequency of " + oldData[0][0] + " Storms in Various Locations from " + oldData[0][2] + "-" + oldData[oldData.length - 1][2];
        }

        var dataGroup = d3.nest()
            .key(function(d) {
                if(columns[1] == "stormType"){
                    return d.stormType;
                } else {
                    return d.state;
                }
            })
            .entries(data);
        console.log(JSON.stringify(dataGroup));
        var color = d3.scale.category10();
        var vis = d3.select("#visualisation"),
            WIDTH = 1000,
            HEIGHT = 500,
            MARGINS = {
                top: 50,
                right: 20,
                bottom: 50,
                left: 50
            },
            lSpace = WIDTH/dataGroup.length;
        xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([d3.min(data, function(d) {
            return d.year;
        }), d3.max(data, function(d) {
            return d.year;
        })]),
            yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([d3.min(data, function(d) {
                return 0;
            }), d3.max(data, function(d) {
                return d.count;
            })]),
            xAxis = d3.svg.axis()
                .scale(xScale)
                .tickFormat(d3.format("d"));
        yAxis = d3.svg.axis()
            .scale(yScale)
            .orient("left");

        vis.append("svg:g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")")
            .call(xAxis);
        vis.append("svg:g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + (MARGINS.left) + ",0)")
            .call(yAxis);
        vis.append("svg:text")
            .attr("transform", "rotate(-90)")
            .attr("x", 0 - (HEIGHT / 2))
            .attr("y", 0 + 15)
            .style("text-anchor", "middle")
            .style('font-size', '20px')
            .text("Frequency");

        var lineGen = d3.svg.line()
            .x(function(d) {
                return xScale(d.year);
            })
            .y(function(d) {
                return yScale(d.count);
            })
            .interpolate("linear");
        dataGroup.forEach(function(d,i) {
            //var col = "hsl(" + Math.random() * 360 + ",100%,50%)";
            var col = "hsl(" + i/10 * 360 + ",100%,50%)";
            console.log(col);
            vis.append('svg:path')
                .attr('d', lineGen(d.values))
                .attr('stroke', function(d,j) {
                    return col;
                })
                .attr('stroke-width', 2)
                .attr('id', 'line_'+d.key)
                .attr('fill', 'none');
            vis.append("text")
                .attr("x", (lSpace/2)+i*lSpace)
                .attr("y", HEIGHT - 5)
                .style("fill", function(d,j) {
                    return col;
                })

                .attr("class","legend")
                .on('click',function(){
                    var active   = d.active ? false : true;
                    var opacity = active ? 0 : 1;
                    d3.select("#line_" + d.key).style("opacity", opacity);
                    d.active = active;
                })
                //.text(d.key);
                .text(toTitleCase(d.key));



        });






    });
}

InitChart();
