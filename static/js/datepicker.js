document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('draw_date');
    const today = new Date();
    const todayStr = today.toISOString().split('T')[0];

    const maxDate = new Date(today);
    maxDate.setDate(today.getDate() + 2);
    const maxDateStr = maxDate.toISOString().split('T')[0];

    // Disable past dates and dates beyond three days from today
    dateInput.setAttribute('min', todayStr);
    dateInput.setAttribute('max', maxDateStr);

    // Add input event listener
    dateInput.addEventListener('input', function() {
        const selectedDate = new Date(this.value);
        const day = selectedDate.getUTCDay();

        // Check if the selected date is a Tuesday or Friday
        if (day !== 2 && day !== 5) {
            alert('Please select a Tuesday or Friday.');
            this.value = '';
        } else if (selectedDate < today || selectedDate > maxDate) {
            alert('Please select a date within the next three days.');
            this.value = '';
        }
    });
});
