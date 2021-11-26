// Global variable calendar
var CALENDAR;

// TUI Calendar
document.addEventListener('DOMContentLoaded', function() {
    // Create an emtpy calendar
    CALENDAR = new tui.Calendar('#calendar', {
        defaultView: 'month',
        isReadOnly: true,
        useDetailPopup: true,
        template: {
            allday: function(schedule) {

                if (schedule.raw && schedule.raw["workoutType"]) {
                    if (schedule.raw.workoutType == "Cardio") {
                        iconClass = "fa-solid fa-heart-pulse";
                    } else if (schedule.raw.workoutType == "Strength") {
                        iconClass = "fa-solid fa-dumbbell";
                    } else if (schedule.raw.workoutType == "Flexibility") {
                        iconClass = "fa-solid fa-spa";
                    } else {
                        iconClass = "fa-solid fa-icons"
                    }
                }
                // Alternative: '<i class="' + iconClass + "></i> " + schedule.title;
                return `<i class="${iconClass}"></i> ${schedule.title}`;
            },
        },
    });
    // Create schedules into the calendar
    if (typeof WORKOUT_SCHEDULES !== undefined) {
        CALENDAR.createSchedules(WORKOUT_SCHEDULES);
    }

    calHeader();
});

// Get current month and year
function calHeader() {
    var calHeader = document.getElementById("calHeader");
    currentDate = CALENDAR.getDate();
    calHeader.innerHTML = `${currentDate.getFullYear()}.${currentDate.getMonth() + 1}`;
}

// Move to today
function today() {
    CALENDAR.today();
    calHeader();
}

// Move to previous month
function prev() {
    CALENDAR.prev();
    calHeader();
}

// Move to next month
function next() {
    CALENDAR.next();
    calHeader();
}