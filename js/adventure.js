var Adventures = {};
//currentAdventure is used for the adventure we're currently on (id). This should be determined at the beginning of the program
Adventures.currentAdventure = 0;
//currentStep is used for the step we're currently on (id). This should be determined at every crossroad, depending on what the user chose
Adventures.currentStory = 0;
Adventures.currentUser = 1;
Adventures.current_story_answer = 0;


//TODO: remove for production
Adventures.debugMode = true;
Adventures.DEFAULT_IMG = "./images/choice.jpg";


//Handle Ajax Error, animation error and speech support
Adventures.bindErrorHandlers = function () {
    //Handle ajax error, if the server is not found or experienced an error
    $(document).ajaxError(function (event, jqxhr, settings, thrownError) {
        Adventures.handleServerError(thrownError);
    });

    //Making sure that we don't receive an animation that does not exist
    $("#situation-image").error(function () {
        Adventures.debugPrint("Failed to load img: " + $("#situation-image").attr("src"));
        Adventures.setImage(Adventures.DEFAULT_IMG);
    });
};


//The core function of the app, sends the user's choice and then parses the results to the server and handling the response
Adventures.chooseOption = function(){
    Adventures.current_story_answer = $(this).val();

    $.ajax("/story",{
        type: "POST",
        data: {"user": Adventures.currentUser,
            "adventure": Adventures.currentAdventure,
            "current_story": Adventures.currentStory,
            "current_story_answer": Adventures.current_story_answer},
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            console.log(data);
            Adventures.currentStory = data["story_id"];
            $(".greeting-text").hide();

            if(data["complete"] == 0){
                Adventures.write(data)}
            else if(data["complete"] == 1) {
                alert("You won")
            }
            else if(data["complete"] == -1) {
                alert("You're dead and/or broke")
            }
            else {
                alert("Error")
            };
        }
    });
};

//Update the questions
Adventures.write = function (message) {
    //Writing new choices and image to screen
    $(".situation-text").text(message["text"]).show();

    for(var i=0;i<message['options'].length;i++){
        var opt = $("#option_" + (i+1));
        opt.text(message['options'][i]['option_text']);
        opt.prop("value", message['options'][i]['id']);
    }
    Adventures.setImage(message["image"]);
};

//functions to initiate frontend
Adventures.start = function(){
    $(document).ready(function () {

        // add event listener to buttons
        $(".game-option").click(Adventures.chooseOption);

        // when name is entered update start game button state
        $("#nameField").keyup(Adventures.checkName);

        // add event listener to start game
        $(".adventure-button").click(Adventures.initAdventure);

        // Hide the adventure section, will be visible when the game starts and show welcome screen
        $(".adventure").hide();
        $(".welcome-screen").show();
    });
};

//Setting the relevant image according to the server response
Adventures.setImage = function (img_name) {
    $("#situation-image").attr("src", "./images/" + img_name);
};

//Function to enable or disable start game button
Adventures.checkName = function(){
    if($(this).val() !== undefined && $(this).val() !== null && $(this).val() !== ""){
        $(".adventure-button").prop("disabled", false);
    }
    else{
        $(".adventure-button").prop("disabled", true);
    }
};

//get new adventure and initiate
Adventures.initAdventure = function(){

    $.ajax("/start",{
        type: "POST",
        data: {"user":
            $("#nameField").val(),
            "adventure_id": $(this).val()
        },
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            Adventures.write(data);
            Adventures.currentUser = data['user'];
            Adventures.currentAdventure = data['adventure'];
            Adventures.currentStory = data["current"];
            $(".adventure").show();
            $(".welcome-screen").hide();
        }
    });
};

//function in case server connection error
Adventures.handleServerError = function (errorThrown) {
    Adventures.debugPrint("Server Error: " + errorThrown);
    var actualError = "";
    if (Adventures.debugMode) {
        actualError = " ( " + errorThrown + " ) ";
    }
    Adventures.write("Sorry, there seems to be an error on the server. Let's talk later. " + actualError);

};

//function to print when in debug mode
Adventures.debugPrint = function (msg) {
    if (Adventures.debugMode) {
        console.log("Adventures DEBUG: " + msg)
    }
};

Adventures.start();
