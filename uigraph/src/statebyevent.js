$(document).ready(function () {
    //
    // Autocomplete
    //
    var availableTags = ["ActionScript", "AppleScript", "Asp", "BASIC", "C", "C++", "Clojure", "COBOL", "ColdFusion", "Erlang", "Fortran", "Groovy", "Haskell", "Java", "JavaScript", "Lisp", "Perl", "PHP", "Python", "Ruby", "Scala", "Scheme"];

    var counties = ["ALL"];

    var measue

    var eventTypes = ['Astronomical Low Tide',
        'Avalanche',
        'Blizzard',
        'Coastal Flood',
        'Cold/Wind Chill',
        'Debris Flow',
        'Dense Fog',
        'Dense Smoke',
        'Drought',
        'Dust Devil',
        'Dust Storm',
        'Excessive Heat',
        'Extreme Cold/Wind Chill',
        'Flash Flood',
        'Flood',
        'Frost/Freeze',
        'Funnel Cloud',
        'Freezing Fog',
        'Hail',
        'Heat',
        'Heavy Rain',
        'Heavy Snow',
        'High Surf',
        'High Wind',
        'Hurricane (Typhoon)',
        'Ice Storm',
        'Lake-Effect Snow',
        'Lakeshore Flood',
        'Lightning',
        'Marine Hail',
        'Marine High Wind',
        'Marine Strong Wind',
        'Marine Thunderstorm Wind',
        'Rip Current',
        'Seiche',
        'Sleet',
        'Storm Surge/Tide',
        'Strong Wind',
        'Thunderstorm Wind',
        'Tornado',
        'Tropical Depression',
        'Tropical Storm',
        'Tsunami',
        'Volcanic Ash',
        'Waterspout',
        'Wildfire',
        'Winter Storm',
        'Winter Weather'
    ];

    var states = [
        'WISCONSIN',
        'VIRGINIA',
        'TENNESSEE',
        'OKLAHOMA',
        'MASSACHUSETTS',
        'RHODE ISLAND',
        'MARYLAND',
        'LOUISIANA',
        'GEORGIA',
        'FLORIDA',
        'MISSOURI',
        'NEW YORK',
        'PENNSYLVANIA',
        'WEST VIRGINIA',
        'KANSAS',
        'KENTUCKY',
        'CALIFORNIA',
        'MONTANA',
        'SOUTH DAKOTA',
        'MINNESOTA',
        'NORTH CAROLINA',
        'ARKANSAS',
        'WYOMING',
        'ATLANTIC NORTH',
        'NEW JERSEY',
        'INDIANA',
        'E PACIFIC',
        'MICHIGAN',
        'GULF OF MEXICO',
        'IOWA',
        'MAINE',
        'TEXAS',
        'IDAHO',
        'ATLANTIC SOUTH',
        'PUERTO RICO',
        'DISTRICT OF COLUMBIA',
        'ALABAMA',
        'NEBRASKA',
        'COLORADO',
        'SOUTH CAROLINA',
        'WASHINGTON',
        'OHIO',
        'OREGON',
        'HAWAII',
        'ALASKA',
        'NEVADA',
        'NEW MEXICO',
        'VERMONT',
        'ILLINOIS',
        'LAKE ST CLAIR',
        'MISSISSIPPI',
        'LAKE ERIE',
        'CONNECTICUT',
        'ARIZONA',
        'UTAH',
        'NORTH DAKOTA',
        'AMERICAN SAMOA',
        'DELAWARE',
        'NEW HAMPSHIRE',
        'LAKE SUPERIOR',
        'HAWAII WATERS',
        'GUAM',
        'LAKE MICHIGAN',
        'LAKE HURON'
    ];

    var years = [
        '1951',
        '1952',
        '1953',
        '1954',
        '1955',
        '1956',
        '1957',
        '1958',
        '1959',
        '1960',
        '1961',
        '1962',
        '1963',
        '1964',
        '1965',
        '1966',
        '1967',
        '1968',
        '1969',
        '1970',
        '1971',
        '1972',
        '1973',
        '1974',
        '1975',
        '1976',
        '1977',
        '1978',
        '1979',
        '1980',
        '1981',
        '1982',
        '1983',
        '1984',
        '1985',
        '1986',
        '1987',
        '1988',
        '1989',
        '1990',
        '1991',
        '1992',
        '1993',
        '1994',
        '1995',
        '1996',
        '1997',
        '1998',
        '1999',
        '2000',
        '2001',
        '2002',
        '2003',
        '2004',
        '2005',
        '2006',
        '2007',
        '2008',
        '2009',
        '2010',
        '2011',
        '2012',
        '2013',
        '2014',
        '2015',
        '2016'
    ]


    $("#eventTypesField1").autocomplete({
        source: eventTypes,
        response: function (event, ui) {
            if (ui.content.length === 0) {
                $("#empty-message-1").text("  No results found");
            } else {
                $("#empty-message-1").empty();
            }
        }
    });

    $("#eventTypesField2").autocomplete({
        source: eventTypes,
        response: function (event, ui) {
            if (ui.content.length === 0) {
                $("#empty-message-2").text("  No results found");
            } else {
                $("#empty-message-2").empty();
            }
        }
    });

    $("#eventTypesField3").autocomplete({
        source: eventTypes,
        response: function (event, ui) {
            if (ui.content.length === 0) {
                $("#empty-message-3").text("  No results found");
            } else {
                $("#empty-message-3").empty();
            }
        }
    });

    $("#eventTypesField4").autocomplete({
        source: eventTypes,
        response: function (event, ui) {
            if (ui.content.length === 0) {
                $("#empty-message-4").text("  No results found");
            } else {
                $("#empty-message-4").empty();
            }
        }
    });

    $("#eventTypesField5").autocomplete({
        source: eventTypes,
        response: function (event, ui) {
            if (ui.content.length === 0) {
                $("#empty-message-5").text("  No results found");
            } else {
                $("#empty-message-5").empty();
            }
        }
    });

    $("#eventTypesField6").autocomplete({
        source: eventTypes,
        response: function (event, ui) {
            if (ui.content.length === 0) {
                $("#empty-message-6").text("  No results found");
            } else {
                $("#empty-message-6").empty();
            }
        }
    });

    $("#eventTypesField7").autocomplete({
        source: eventTypes,
        response: function (event, ui) {
            if (ui.content.length === 0) {
                $("#empty-message-7").text("  No results found");
            } else {
                $("#empty-message-7").empty();
            }
        }
    });

    $("#eventTypesField8").autocomplete({
        source: eventTypes,
        response: function (event, ui) {
            if (ui.content.length === 0) {
                $("#empty-message-8").text("  No results found");
            } else {
                $("#empty-message-8").empty();
            }
        }
    });

    $("#eventTypesField9").autocomplete({
        source: eventTypes,
        response: function (event, ui) {
            if (ui.content.length === 0) {
                $("#empty-message-9").text("  No results found");
            } else {
                $("#empty-message-9").empty();
            }
        }
    });

    $("#eventTypesField10").autocomplete({
        source: eventTypes,
        response: function (event, ui) {
            if (ui.content.length === 0) {
                $("#empty-message-10").text("  No results found");
            } else {
                $("#empty-message-10").empty();
            }
        }
    });



    $("#statesField").autocomplete({
        source: states,
        select: function (event, ui) {
            $.getJSON("counties.json", function (data) {
                $.each(data, function (key, val) {
                    if (key == ui.item.value) {
                        var temp = val.Z;
                        temp.concat(val.Z);
                        temp.concat(val.M);
                        temp.concat(val.C);
                        $("#countiesField").autocomplete('option', 'source', temp);
                        return false;
                    }
                });
            });
        },
        response: function (event, ui) {
            if (ui.content.length === 0) {
                $("#empty-message-11").text("  No results found");
            } else {
                $("#empty-message-11").empty();
            }
        }
    });

    $("#countiesField").autocomplete({
        source: counties,
        response: function (event, ui) {
            if (ui.content.length === 0) {
                $("#empty-message-12").text("  No results found");
            } else {
                $("#empty-message-12").empty();
            }
        }
    });

    $("#startYearField").autocomplete({
        source: years,
        response: function (event, ui) {
            if (ui.content.length === 0) {
                $("#empty-message-13").text("  No results found");
            } else {
                $("#empty-message-13").empty();
            }
        }
    });

    $("#endYearField").autocomplete({
        source: years,
        response: function (event, ui) {
            if (ui.content.length === 0) {
                $("#empty-message-14").text("  No results found");
            } else {
                $("#empty-message-14").empty();
            }
        }
    });


});
