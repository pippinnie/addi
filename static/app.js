document.addEventListener('DOMContentLoaded', function() {
    // When an alert is dismissed, change focus to brand
    var alert = document.getElementById('alert');
    if (!!alert) {
        alert.addEventListener('closed.bs.alert', function () {
            document.getElementById('brand').focus();
        })
    }
    
    // Get today date 
    // source=https://teamtreehouse.com/community/html-input-date-field-how-to-set-default-value-to-todays-date
    function getDate() {
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth()+1; //January is 0!
        var yyyy = today.getFullYear();

        if(dd<10) {
            dd = '0'+dd
        } 

        if(mm<10) {
            mm = '0'+mm
        } 

        today = yyyy + '-' + mm + '-' + dd;
        console.log(today);
        document.getElementById("date").value = today;
        }


        window.onload = function() {
            getDate();
        };

    // Search database
    // let input = document.querySelector('input');
    // input.addEventListener('keyup', function() {
    //     $.get('/search?q=' + input.value, function(titles) {
    //       let html = '';
    //       for (let id in titles)
    //       {
    //           let title = titles[id].title;
    //           html += '<li>' + title + '</li>';
    //       }

    //       document.querySelector('ul').innerHTML = html;
    //     });
    // });
});          