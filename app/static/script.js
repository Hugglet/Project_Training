document.addEventListener('DOMContentLoaded', () => {
    const filterButton = document.getElementById('filter-button');
    const filterForm = document.getElementById('filter-form');

    if (filterButton) {
        filterButton.addEventListener('click', () => {
            filterForm.submit();
        });
    }

    // Пример валидации
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', (e) => {
            const rating = document.getElementById('rating').value;
            if (rating < 1 || rating > 5) {
                e.preventDefault();
                alert('Rating must be between 1 and 5.');
            }
        });
    }
});

// Всплывающие сообщения
function showToast(message) {
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.position = 'fixed';
    toast.style.bottom = '10px';
    toast.style.right = '10px';
    toast.style.backgroundColor = '#007bff';
    toast.style.color = '#fff';
    toast.style.padding = '10px';
    toast.style.borderRadius = '5px';
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// Пример вызова:
showToast('Event created successfully!');
