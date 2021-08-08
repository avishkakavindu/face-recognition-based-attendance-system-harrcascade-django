
const url = window.location.href.split('/');
const protocol = url[0];
const domain = url[2];


// register
$("#take_images").on("click", function(){
    var reg_no = $("#reg_no").val();
    var name = $("#std_name").val();
    var token = $('input[name="csrfmiddlewaretoken"]').val();

    let payload = {
        "url": `${$(location).attr('protocol')}//${domain}/register/`,
        "method": "POST",
        "timeout": 0,
        "dataType": "json",
        "data": {
            "csrfmiddlewaretoken": token,
            'reg_no': reg_no,
            'name': name
        }
    };

    // console.log('BTN CLICKED!');
     $.ajax(payload)
         .done(function (response) {
            var id = response['id'];
            // get 30 pics
            for(i=0; i<30; i++){
                take_snapshot(id, token);
            }
        })
         .error(function(){
             console.log('Error')
         });
});

// mark attendance
$("#mark_attendance").on("click", function(){
    var token = $('input[name="csrfmiddlewaretoken"]').val();
    var subject = $('#subject').val();

    console.log(subject)
    // call mark_attendance function
    mark_attendance(subject, token);

});


// camera register
Webcam.set({
    width: 350,
    height: 350,
    image_format: "jpg",
    jpeg_quality: 90
})
Webcam.attach("#camera")

function take_snapshot(id, token){

    Webcam.snap(function(data_uri){
        let payload = {
            "url": `${$(location).attr('protocol')}//${domain}/student_image/`,
            "method": "POST",
            "timeout": 0,
            "dataType": "json",
            "data": {
                "csrfmiddlewaretoken": token,
                'student': id,
                'image': data_uri
            }
        };

        $.ajax(payload)
         .done(function (response) {
            console.log(response);
        })
         .error(function(){
             console.log('Error')
         });
    })
}

// attendance camera
Webcam.attach("#camera_attendance")

function mark_attendance(subject, token){

    Webcam.snap(function(data_uri){
        let payload = {
            "url": `${$(location).attr('protocol')}//${domain}/mark_attendance/`,
            "method": "POST",
            "timeout": 0,
            "dataType": "json",
            "data": {
                "csrfmiddlewaretoken": token,
                'subject': subject,
                'image': data_uri
            }
        };
        // console.log(payload)
        $.ajax(payload)
         .done(function (response) {
            console.log(response);

            
        })
         .error(function(){
             console.log('Error')
         });
    })
}

