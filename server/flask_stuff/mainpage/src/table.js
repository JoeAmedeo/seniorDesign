/*Terrible code writen by Joe 10/6/16*/


/* test JSON file, modified slightly so that there is an array of events. Probably will change this in the future */
var data = [{
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
}];

/*locate table*/
var table = document.getElementById("table");

/*for each element in the data array, create a new row*/
var row = [];
var i = 0;


for (i = 0; i < data.length; i += 1) {
    row.push(table.insertRow(i + 1));
}

/*for each new row, add a cell for each variable in the data object and put said variable into the cell*/
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



function StringSort(elements, k) {
    /* case 1: given list is size greater than 2 */
    if (elements.length > 2) {
        /* split the array in half and then sort each half */
        var array1 = [], array2 = [];
        console.log("this array is greater than size 2");
        for (i = 0; i < elements.length / 2; i += 1) {
            array1[i] = elements[i];
        }
        for (i = (elements.length / 2) + 1; i < elements.length; i += 1) {
            array2[i - elements.length - 1] = elements[i];
        }
        var newArray1 = StringSort(array1), newArray2 = StringSort(array2), finalArray = [];
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
            finalArray.push(newArray1);
        } else {
            finalArray.push(newArray2);
        }
        return finalArray;
        
    } else if (elements.length === 2) {
        /* case 2: list is of size 2, then see which element in the list is smaller, put it first in the list then return it */
        console.log("this array is size 2");
        if (elements[0].content.localeCompare(elements[1].content) < 0) {
            return elements;
        } else {
            var temp = elements[1];
            elements[1] = elements[0];
            elements[0] = temp;
            return elements;
        }
    } else {
        /* case 3: the list is size 1, then just return the list */
        console.log("this array is size 1");
        return elements;
    }
    
}

/* Merge Sort functions */
function Sort(column) {
    var words = [];
    for (i = 0; i < document.getElementById('table').rows.length; i += 1) {
        words.push({"content": document.getElementById('table').rows[i].cells[column].innerHTML, "row": i});
    }
    words = StringSort(words, column);
    
    for (i = 0; i < words.length; i += 1) {
        console.log(words[i].content);
        /*document.getElementById('table').rows[i] = words[i].row;*/
    }
    
}


/* create an event listener for each column */

document.getElementById('State').addEventListener('click', function() {
    Sort(0);
});

document.getElementById('County').addEventListener('click', function() {
    Sort(1);
});

document.getElementById('Begin_time').addEventListener('click', function() {
    Sort(2);
});

document.getElementById('End_time').addEventListener('click', function() {
    Sort(3);
});

/*
$("#State").on(Sort(0));
$("#County").click(Sort(1));
$("#Begin_time").click(Sort(2));
$("#End_time").click(Sort(3));
*/
