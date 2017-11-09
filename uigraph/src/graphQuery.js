
var query = [];
var columns = [];
var isEmpty = false;

document.getElementById("SubmitButton").addEventListener("click", function(){
    
    query = [
        {"name" : "year", "type" : ">=", "value" : null},
        {"name" : "year", "type" : "<=", "value" : null},
        {"name" : "event_type", "params" : [
            {"type" : "=", "value" : ""},
            {"type" : "=", "value" : ""},
            {"type" : "=", "value" : ""},
            {"type" : "=", "value" : ""},
            {"type" : "=", "value" : ""},
            {"type" : "=", "value" : ""},
            {"type" : "=", "value" : ""},
            {"type" : "=", "value" : ""},
            {"type" : "=", "value" : ""},
            {"type" : "=", "value" : ""}
         ]},
        {"name" : "state", "type" : "=", "value" : ""}
    ];
    
    columns = [
	   "year", "event_type"
    ];
    
    
    if(document.getElementById("startYearField").value != ""){
        query[0].value = document.getElementById("startYearField").value;
    }
    
    if(document.getElementById("endYearField").value != ""){
        query[1].value = document.getElementById("endYearField").value;
    }
    
    if(document.getElementById("eventTypesField1").value != ""){
        query[3].params[0].value = document.getElementById("eventTypesField1").value;
    }
    
    if(document.getElementById("eventTypesField2").value != ""){
        query[2].params[1].value = document.getElementById("eventTypesField2").value;
    }
    
    if(document.getElementById("eventTypesField3").value != ""){
        query[2].params[2].value = document.getElementById("eventTypesField3").value;
    }
    
    if(document.getElementById("eventTypesField4").value != ""){
        query[2].params[3].value = document.getElementById("eventTypesField4").value;
    }
    
    if(document.getElementById("eventTypesField5").value != ""){
        query[2].params[4].value = document.getElementById("eventTypesField5").value;
    }
    
    if(document.getElementById("eventTypesField6").value != ""){
        query[2].params[5].value = document.getElementById("eventTypesField6").value;
    }
    
    if(document.getElementById("eventTypesField7").value != ""){
        query[2].params[6].value = document.getElementById("eventTypesField7").value;
    }
    
    if(document.getElementById("eventTypesField8").value != ""){
        query[2].params[7].value = document.getElementById("eventTypesField8").value;
    }
    
    if(document.getElementById("eventTypesField9").value != ""){
        query[2].params[8].value = document.getElementById("eventTypesField9").value;
    }
    if(document.getElementById("eventTypesField10").value != ""){
        query[2].params[9].value = document.getElementById("eventTypesField10").value;
    }
    
    if(document.getElementById("statesField1").value != ""){
        query[3].value = document.getElementById("statesField1").value;
    }
    
    for(i=(query.length - 1); i >= 0; i--){
        if(query[i].value == null || query[i].value == ""){
            query.splice(i,1);
        }
    }
    
    for(i=(query.length - 1); i >= 0; i--){
        if(i == 2){
            for(j = (query[2].params.length - 1); j >= 0; j--){
                if(query[2].params[j].value == ""){
                    query.params.splice(j,1);
                }
            }
            if(query[2].params.length == 0){
                query.splice(2,1);
            }
        }else{
            if(query[i].value == ""){
                query.splice(i,1);
            }
        }
    }
    
    
    if(query.length == 0){
        alert("You need to enter at least 1 search field to obtain a table.");
        isEmpty = true;
    }
    
    var stuff = {"query": query, "columns" : columns};
    
    console.log(query);
    /* for test cases */
    var stuffx = {
            "query" :
                [
	               
                ]
            };
    
    $.ajax({
        url: "http://cs-sdp7.engr.uconn.edu:5000/api/test_code_graph",
        type: "POST",
        data: JSON.stringify(stuff),
        dataType: "json",
        contentType: "application/json",
        success: function(data){
            console.log(data);
            /* insert functions that requirethe JSON here */
            
        },
        error: function(xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
        }
        
    });
    /* reference for post request
      var text = $("input").val();
      var data = {"query" : [{"name" : "state", "type" : "=", "value" : text}]}
      $.ajax({
      type: "POST",
      url: "http://cs-sdp7.engr.uconn.edu:5000/api/test_code",
      contentType: "application/json",
      dataType: "json",
      data: JSON.stringify(data),
      success: function(data) { $("#result").html(JSON.stringify(data)); }
      }); */
    
    
    
});