/*Terrible code writen by Joe 10/6/16*/


/* test JSON file, modified slightly so that there is an array of events. Probably will change this in the future */
/*var data = [{
    "state": "Connecticut",
    "cz_name": "New Haven",
    "time": { "begin_datetime": "1994-11-28 00:00:00", "end_datetime": "2016-10-1 23:59:59"}
}, {
    "state": "Florida",
    "cz_name": "Duval",
    "time": {"begin_datetime": "1953-12-13 17:50:00", "end_datetime": "1953-12-13 17:50:00"}
}, {
    "state": "Florida",
    "cz_name": "Inland PA",
    "time": {"begin_datetime": "2000-12-31 06:00:00", "end_datetime": "2000-12-31 09:00:00"}
}, {
    "state": "Texas",
    "cz_name": "Haskell",
    "time": {"begin_datetime": "2000-02-25 00:00:00", "end_datetime": "2000-02-28 18:00:00"}
}];*/

var data = {
    "result": [
        ["Begin_DateTime", "End_DateTime", "EventID", "EpisodeID", "State", "County", "InjuriesDirect", "InjuriesIndirect", "DeathsDirect", "DeathsIndirect"],
        ["1994-11-28 00:00:00", "2016-10-1 23:59:59", 500, 1000, "Connecticut", "New Haven", 0, 20, 0, 0],
        ["1953-12-13 17:50:00", "1953-12-13 17:50:00", 9991475, , "Florida", "Duval", 0, 0, 0, 0],
        ["2000-12-31 06:00:00", "2000-12-31 09:00:00", 5165377, 1104812, "Florida", "Inland PA", 0, 0, 0, 0],
        ["2000-02-25 00:00:00", "2000-02-28 18:00:00", 5129018, 1090451, "Texas", "Haskell", 0, 0, 0, 0],
        ["1953-04-23 15:31:00", "1953-04-23 15:31:00", 10099786, , "Oklahoma", "Okmulgee", 0, 0, 0, 0],
        ["1951-06-26 18:00:00", "1951-06-26 18:00:00", 10039192, , "Michigan", "Midland", 0, 0, 0, 0]
               ]
};

/*locate table*/
var table = document.getElementById("table");

/*for each element in the data array, create a new row*/
/*
var row = [];
var i = 0;


for (i = 0; i < data.length; i += 1) {
    row.push(table.insertRow(i + 1));
}

for each new row, add a cell for each variable in the data object and put said variable into the cell
var cell1 = [];
var cell2 = [];
var cell3 = [];
var cell4 = [];
for (i = 0; i < row.length; i += 1) {
    
    cell1.push(row[i].insertCell(0));
    cell2.push(row[i].insertCell(1));
    cell3.push(row[i].insertCell(2));
    cell4.push(row[i].insertCell(3));
    
    cell1[i].innerHTML = data[i].state;
    cell2[i].innerHTML = data[i].cz_name;
    cell3[i].innerHTML = data[i].time.begin_datetime;
    cell4[i].innerHTML = data[i].time.end_datetime;
}
*/

// Removes all elements from the table. Will be used in ajax call to recreate the table for each new query.
function DestroyTable(){
    while(table.rows.length > 0){
        table.deleteRow(-1);
    }
}

var i = 0;
var j = 0;
function CreateTable(tableData){
    var row;
    var cell;
    var event_narrative_column = 10000;
    var episode_narrative_column = 10000;

    for(i=0; i < tableData.result.length; i++){
        row = table.insertRow(i);
        for(j=0; j < tableData.result[i].length; j++){
            if(tableData.result[i][j] === "event_narrative"){
                event_narrative_column = j;
            } 
            if(tableData.result[i][j] === "episode_narrative"){
                episode_narrative_column = j;
            }
            if(j != event_narrative_column || j != episode_narrative_column){
                cell = row.insertCell(j);
                cell.innerHTML = tableData.result[i][j];
            }
            
            
        }
        
    }
    
    for(i=0; i<table.rowslength; i++){
        if(episode_narrative_column > event_narrative_column){
            table.rows[i].deleteCell(episode_narrative_column);
            table.rows[i].deleteCell(event_narrative_column);
        }else{
            table.rows[i].deleteCell(event_narrative_column);
            table.rows[i].deleteCell(episode_narrative_column);
        }
    }
    data = tableData;
}

/* create an event listener for each column */
function createActionListeners(){
    document.getElementById("table").rows[0].cells[0].addEventListener('click', function() {
    Sort(0);
    });

    document.getElementById("table").rows[0].cells[1].addEventListener('click', function() {
        Sort(1);
    });

    document.getElementById("table").rows[0].cells[2].addEventListener('click', function() {
        Sort(2);
    });

    document.getElementById("table").rows[0].cells[3].addEventListener('click', function() {
        Sort(3);
    });

}

CreateTable(data);
createActionListeners();

function StringSort(elements, k) {
    /* case 1: given list is size greater than 2 */
    if (elements.length > 2) {
        /* split the array in half and then sort each half */
        var array1 = [];
        var array2 = [];
        console.log("this array is greater than size 2");
        console.log("first array: ");
        for (i = 0; i < elements.length / 2; i += 1) {
            array1[i] = elements[i];
            console.log(array1[i].content);
        }
        console.log(i);
        console.log("second array: ");
        var k = 0;
        while ( i < elements.length) {
            array2[k] = elements[i];
            console.log(array2[k].content);
            k++;
            i++;
        }
        var newArray1 = StringSort(array1); 
        var newArray2 = StringSort(array2);
        var finalArray = [];
        console.log("content of newArray1: ");
        for ( i=0; i<newArray1.length; i++) {
            console.log(newArray1[i].content);
        }
        console.log("content of newArray2: ");
        for ( i=0; i<newArray2.length; i++) {
            console.log(newArray2[i].content);
        }
        /* take each returned array and see which has the lower value, then push that onto the final returned array and remove the array element  */
        while (newArray1.length > 0 && newArray2.length > 0) {
            if (newArray1[0].content.localeCompare(newArray2[0].content) < 0) {
                finalArray.push(newArray1[0]);
                newArray1.splice(0, 1);
            } else {
                finalArray.push(newArray2[0]);
                newArray2.splice(0, 1);
            }
            
        }
        /* once one array is empty, add the remainder of the other array to the final array */
        if (newArray1.length > 0) {
            for(i=0; i<newArray1.length; i++){
                finalArray.push(newArray1[i]);
            }
            finalArray.push(newArray1);
        } else {
            for(i=0; i<newArray2.length; i++){
                finalArray.push(newArray2[i]);
            }
        }
        console.log("content of finalArray: ");
        for(i=0; i<finalArray.length; i++){
            console.log(finalArray[i].content);
        }
        return finalArray;
        
    } else if (elements.length === 2) {
        /* case 2: list is of size 2, then see which element in the list is smaller, put it first in the list then return it */
        console.log("this array is size 2");
        if (elements[0].content.localeCompare(elements[1].content) < 0) {
            console.log(elements[0]);
            console.log(elements[1]);
            return elements;
        } else {
            var temp = elements[1];
            elements[1] = elements[0];
            elements[0] = temp;
            console.log(elements[0].content);
            console.log(elements[1].content);
            return elements;
        }
    } else {
        /* case 3: the list is size 1, then just return the list */
        console.log("this array is size 1");
        console.log(elements[0].content);
        return elements;
    }
    
}

/* Merge Sort functions */
function Sort(column) {
    var words = [];
    var orderedWords = [];
    var orderedRows = [];
    for (i = 1; i < document.getElementById('table').rows.length; i += 1) {
        words.push({"content": document.getElementById('table').rows[i].cells[column].innerHTML, "row": i});
    }
    orderedWords = StringSort(words, column);
    
    console.log("Final array:");

    for (i = 0; i < orderedWords.length; i += 1) {
        console.log(orderedWords[i].content + ", " + orderedWords[i].row);
        /*document.getElementById('table').rows[i] = words[i].row;*/
    }
    var newData = [];
    
    for(j=0; j<orderedWords.length; j++){
        console.log(data.rows[orderedWords[j].row - 1]);
        newData.push(data.rows[orderedWords[j].row - 1]);
    }
    data.rows = newData;
    DestroyTable();
    CreateTable(data);
    createActionListeners();
    
}


/* create an event listener for each column 
function createActionListeners(){
    document.getElementById("table").rows[0].cells[0].addEventListener('click', function() {
    Sort(0);
    });

    document.getElementById("table").rows[0].cells[1].addEventListener('click', function() {
        Sort(1);
    });

    document.getElementById("table").rows[0].cells[2].addEventListener('click', function() {
        Sort(2);
    });

    document.getElementById("table").rows[0].cells[3].addEventListener('click', function() {
        Sort(3);
    });

}*/

function create_HideShow_listeners(){
    document.getElementById("hide_show_box_1").addEventListener('click', function() {
       console.log("look at you go you clicked the first box!");
       var left_content = document.getElementsByClassName("left")[0];
       var right_content = document.getElementsByClassName("right")[0];
       if( left_content.style.visibility === 'hidden' ){
           left_content.style.visibility = 'visible';
           left_content.style.height = "auto";
           right_content.style.visibility = 'visible';
           right_content.style.height = "auto";
           var str1 = "Hide---";
           var str2 = "Show".bold();
           document.getElementById("hide_show_box_1").innerHTML = str1+str2;
       }else{
           left_content.style.visibility = 'hidden';
           left_content.style.height = "0px";
           right_content.style.visibility = 'hidden';
           right_content.style.height = "0px";
           
           var str1 = "Hide".bold();
           var str2 = "---Show";
           document.getElementById("hide_show_box_1").innerHTML = str1+str2;
       }
    });
}

create_HideShow_listeners();

 $(document).ready(function () {
    $('table').each(function () {
        var $table = $(this);

        var $button = $("<button type='button'>");
        $button.text("Download Table Data");
        $button.insertAfter($table);

        $button.click(function () {
            var csv = $table.table2CSV({
                delivery: 'value'
            });
            window.location.href = 'data:text/csv;charset=UTF-8,' 
            + encodeURIComponent(csv);
        });
    });
});
/*
$("#State").on(Sort(0));
$("#County").click(Sort(1));
$("#Begin_time").click(Sort(2));
$("#End_time").click(Sort(3));
*/
