document.addEventListener('DOMContentLoaded', function() {
    var calendar = new tui.Calendar('#calendar', {
        defaultView: 'month',
        isReadOnly: true,
        useDetailPopup: true,
    });
    if (typeof WORKOUT_SCHEDULES !== undefined) {
        calendar.createSchedules(WORKOUT_SCHEDULES);
    }
});