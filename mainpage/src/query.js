var queryString = {
    "and": [],
    "or": []
}


var query = [];
var isEmpty = false;

document.getElementById("SubmitButton").addEventListener("click", function(){
    
    query = [
        {"name" : "injuries_direct", "type" : "=", "value" : null},
        {"name" : "injuries_indirect", "type" : "=", "value" : null},
        {"name" : "death_direct", "type" : "=", "value" : null},
        {"name" : "deaths_indirect", "type" : "=", "value" : null},
        {"name" : "event_type", "type" : "=", "value" : ""},
        {"name" : "state", "type" : "=", "value" : ""},
        {"name" : "cz_name", "type" : "=", "value" : ""},
        {"name" : "year", "type" : "=", "value" : null},
        {"name" : "month_name", "type" : "=", "value" : ""}
    ];
    
    stuff = {"query": query};
    
    if(document.getElementById("InjuriesDirect1").value != ""){
        query[0].value = Number(document.getElementById("InjuriesDirect1").value);
    }
    if(document.getElementById("operator1").value != ""){
        query[0].type = document.getElementById("operator1").value;
    }
    if(document.getElementById("InjuriesIndirect1").value != ""){
        query[1].value = Number(document.getElementById("InjuriesIndirect1").value);
    }
    if(document.getElementById("operator2").value != ""){
        query[1].type = document.getElementById("operator2").value;
    }
    if(document.getElementById("DeathsDirect1").value != ""){
        query[2].value = Number(document.getElementById("DeathsDirect1").value);
    }
    if(document.getElementById("operator3").value != ""){
        query[2].type = document.getElementById("operator3").value;
    }
    if(document.getElementById("DeathsIndirect1").value != ""){
        query[3].value = Number(document.getElementById("DeathsIndirect1").value);
    }
    if(document.getElementById("operator4").value != ""){
        query[3].type = document.getElementById("operator4").value;
    }
    
    query[4].value = document.getElementById("eventTypesField1").value;
    query[5].value = document.getElementById("statesField").value;
    query[6].value = document.getElementById("countiesField").value;
    if(document.getElementById("startYearField").value != ""){
        query[7].value = Number(document.getElementById("startYearField").value);
    }
    if(document.getElementById("operator5").value != ""){
        query[7].type = document.getElementById("operator5").value;
    }
    query[8].value = documents.getElementById("MonthField1").value;
    
    for(i=(query.length - 1); i >= 0; i--){
        if(query[i].value == null || query[i].value == ""){
            query.splice(i,1);
        }
    }
    
    if(query.length == 0){
        alert("You need to enter at least 1 search field to obtain a table.");
        isEmpty = true;
    }
    
    console.log(query);
    var stuffx = {
            "query" :
                [
	               
                ]
            };
    
    $.ajax({
        url: "http://cs-sdp7.engr.uconn.edu:5000/api/test_code",
        type: "POST",
        data: JSON.stringify(stuff),
        dataType: "json",
        contentType: "application/json",
        success: function(data){
            console.log(data);
            DestroyTable();
            CreateTable(data);
            createActionListeners();
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