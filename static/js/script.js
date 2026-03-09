document.addEventListener('DOMContentLoaded', function () {
    // Barcode validation
    const barcodeForm = document.getElementById('barcodeForm');
    if (barcodeForm) {
        barcodeForm.addEventListener('submit', function (e) {
            const barcodeInput = document.getElementById('barcode');
            if (barcodeInput.value.length < 5) {
                alert('Please enter a valid barcode number.');
                e.preventDefault();
            }
        });
    }

    // Interactive elements
    const clickableRows = document.querySelectorAll('.store-row');
    clickableRows.forEach(row => {
        row.addEventListener('click', function () {
            const store = this.dataset.store;
            console.log('Clicked store:', store);
        });
    });
});
