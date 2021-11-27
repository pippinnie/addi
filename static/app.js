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
        if (document.getElementById("date")) {
            document.getElementById("date").value = today;
        }
    }

    window.onload = function() {
        getDate();
    };


    // Sticky navbar
    // When the user scrolls the page, execute myFunction
    window.onscroll = function() {myFunction()};

    // Get the header
    var header = document.getElementById("myHeader");

    // Get the offset position of the navbar
    var sticky = header.offsetTop;

    // Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
    function myFunction() {
    if (window.pageYOffset > sticky) {
        header.classList.add("sticky");
    } else {
        header.classList.remove("sticky");
    }}


    // Search box on workout log
    // source=https://www.w3schools.com/jquery/jquery_filters.asp
    $(document).ready(function(){
        $("#myInput").on("keyup", function() {
            var value = $(this).val().toLowerCase();
            $("#myTable tr").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
        });
    });


    // Tooltip
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

});