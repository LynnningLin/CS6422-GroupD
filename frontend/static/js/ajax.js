function fetch_data(){ 
    // Using AJAX to update the browser with the JSON data 
    $.ajax({
        url: "/homepage", // This targets which route to update
        type: "GET", // The method being used
        headers: { // Just to check to see whether actual json data from the shared_data dict is being given rather than the whole HTML page
            "X-Requested-With": "XMLHttpRequest"},
        
            success: function(data){
            console.log("Received Data: ", data);  // Sensors data debug log, Check console in browser to see
            console.log("Fire Alarm Status:", data.fire_alarm);

            // $('#test2').text(data.target_temperature + "°C");

            // $('#test').text(data.current_temperature + "°C"); // #test is the id i added for the current temp in /homepage  <p id="test">{{current_temperature}}°C</p>, this refreshes the number on the browser
           
            $('#current_section').text(data.current_temperature + "°C");


            if(data.current_temperature >= 50 && data.fire_alarm == "y"){
                alert("ATTENTION\nTemperature At Dangerous Levels\nPlease Vacate Immediately\nSystem Will Stop");
            };

            if (data.is_occupied){ // Shows whether the Stay or Away is diaplayed based on the JSON data 
                $("#occupancy img").attr('src', 'static/images/stay.png');
            } else{
                $("#occupancy img").attr('src', 'static/images/away.png');
            }
            // if (data.is_increasing){
            if (data.HVAC_movement){
                $("#target_section img:first-of-type").attr('src', 'static/images/temperature_up.png'); // Still working on this
            } else {
                $("#target_section img:first-of-type").attr('src', 'static/images/temperature_down.png');
            } // Had some trouble with checking whether the temp is increasing or not, but shouldn't be hard to iron out later on
            if (data.is_HVAC_on){
                $("#target_section img:last-of-type").attr('src', 'static/images/HVAC_on.png');
            } else {
                $("#target_section img:last-of-type").attr('src', 'static/images/HVAC_off.png');
            }
        },
        error: function(error){
            console.warn("Can't Fetch /homepage Data!", error); // Error Handling
        } 
    })
    
    $.ajax({ // Identical Format to the previous AJAX method
        url: "/rooms",
        type: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest"}, // Mark the request as an AJAX one
            
        success: function(data){
            console.log("Received Data: ", data);  // Debug log
            $('#section-1').text("Living Room: " + data.room1_temperature + "°C");
            $('#section-2').text("Bathroom: " + data.room2_temperature + "°C");
            $('#section-3').text("Bedroom: " + data.room3_temperature + "°C");
            $('#section-4').text("Kitchen:" + data.room4_temperature + "°C");
            $('#fifth-section').text("Current: " + data.current_temperature + "°C")

        },
        error: function(error){
            console.warn("Can't Fetch /rooms Data!", error);
        } 
    })
}
setInterval(fetch_data, 450); // If you want to change how fast AJAX is updating the browser then swtich it here, it doesn't affect the simpy env speed. 


