document.addEventListener('DOMContentLoaded', function () {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const groups = document.querySelectorAll('.group-content');

    function filterContent(selectedGroup) {
        // Remove active class from all buttons and groups
        filterButtons.forEach(btn => btn.classList.remove('active'));
        groups.forEach(group => group.classList.remove('active'));

        // Add active class to selected elements
        document.querySelector(`.filter-btn[data-filter="${selectedGroup}"]`).classList.add('active');
        document.querySelector(`.group-content[data-group="${selectedGroup}"]`).classList.add('active');
    }

    filterButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            filterContent(btn.dataset.filter);
            handleShowMore(btn.dataset.filter);
        });
    });

    function handleShowMore(filter) {
        const container = document.querySelector('.grid-container');
        const showBtn = container.nextElementSibling;
        const allItems = container.querySelectorAll('.item');
        let visibleItems = [];

        allItems.forEach(item => {
            const match = item.dataset.group === filter;
            item.style.display = match ? 'block' : 'none';
            if (match) visibleItems.push(item);
        });

        container.classList.add('collapsed');
        visibleItems.forEach((item, index) => {
            if (index >= 3) item.style.display = 'none';
        });

        showBtn.classList.toggle('hidden', visibleItems.length <= 3);
        showBtn.innerHTML = 'Show More <i class="fas fa-chevron-down"></i>';
    }

    document.querySelectorAll('.show-more-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const container = this.previousElementSibling;
            container.classList.toggle('collapsed');
            this.innerHTML = container.classList.contains('collapsed')
                ? 'Show More <i class="fas fa-chevron-down"></i>'
                : 'Show Less <i class="fas fa-chevron-up"></i>';
        });
    });

    // Initialize with first group active
    if (filterButtons.length) {
        filterContent(filterButtons[0].dataset.filter);
    }
});
