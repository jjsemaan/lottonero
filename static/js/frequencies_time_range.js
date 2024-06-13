document.getElementById('timeRangeSelect').addEventListener('change', function() {
    const selectedTimeRange = this.value;
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('time_range', selectedTimeRange);
    window.location.search = urlParams.toString();
});
