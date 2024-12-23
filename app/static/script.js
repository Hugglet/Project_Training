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
