// TUI Calendar
document.addEventListener('DOMContentLoaded', function() {
    var calendar = new tui.Calendar('#calendar', {
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
    if (typeof WORKOUT_SCHEDULES !== undefined) {
        calendar.createSchedules(WORKOUT_SCHEDULES);
    }
});