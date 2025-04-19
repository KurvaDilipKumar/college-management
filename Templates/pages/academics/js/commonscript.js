



document.addEventListener('DOMContentLoaded', function() {
    // Initialize all grids
    function initGrids() {
        document.querySelectorAll('.grid-container').forEach(container => {
            const items = container.querySelectorAll('.item');
            const showBtn = container.nextElementSibling;
            
            // Start collapsed
            container.classList.add('collapsed');
            showBtn.classList.toggle('hidden', items.length <= 3);
        });
    }

    // Show More button handler
    document.querySelectorAll('.show-more-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const container = this.previousElementSibling;
            container.classList.toggle('collapsed');
            this.innerHTML = container.classList.contains('collapsed') 
                ? 'Show More <i class="fas fa-chevron-down"></i>' 
                : 'Show Less <i class="fas fa-chevron-up"></i>';
        });
    });

    // Faculty Filter
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const filter = this.dataset.filter;
            const container = this.closest('.container').querySelector('.grid-container');
            const showBtn = container.nextElementSibling;

            // Update active state
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            // Filter items
            const allItems = container.querySelectorAll('.item');
            let visibleItems = [];
            
            allItems.forEach(item => {
                const role = item.querySelector('.designation').textContent.toLowerCase();
                const match = 
                    filter === 'all' ||
                    (filter === 'professor' && role.includes('professor') && 
                     !role.includes('assistant') && !role.includes('associate')) ||
                    (filter === 'associate' && role.includes('associate')) ||
                    (filter === 'assistant' && role.includes('assistant'));
                
                item.style.display = match ? 'block' : 'none';
                if (match) visibleItems.push(item);
            });

            // Reset to collapsed state
            container.classList.add('collapsed');
            
            // Hide items beyond first 3
            visibleItems.forEach((item, index) => {
                if (index >= 3) item.style.display = 'none';
            });

            // Update show more button
            showBtn.classList.toggle('hidden', visibleItems.length <= 3);
            showBtn.innerHTML = 'Show More <i class="fas fa-chevron-down"></i>';
        });
    });

    // Initial setup
    initGrids();
});





// document.querySelectorAll(".show-more-btn").forEach((btn) => {
//   btn.addEventListener("click", function () {
//     const container = this.previousElementSibling;
//     const isCollapsed = container.classList.contains("collapsed");
//     const visibleItems = Array.from(
//       container.querySelectorAll(".item:not(.hidden)")
//     );
//     visibleItems.forEach((item, index) => {
//       item.classList.toggle("collapsed-hidden", index >= 3);
//     });

//     if (isCollapsed) {
//       visibleItems.forEach((item) => item.classList.remove("collapsed-hidden"));
//       container.classList.remove("collapsed");
//       this.textContent = "Show Less ";
//     } else {
//       visibleItems.forEach((item, index) => {
//         item.classList.toggle("collapsed-hidden", index >= 3);
//       });
//       container.classList.add("collapsed");
//       this.textContent = "Show More ";
//     }
//     this.querySelector("i").style.transform = isCollapsed
//       ? "rotate(180deg)"
//       : "rotate(0deg)";
//   });
// });
// const filterBtns = document.querySelectorAll(".filter-btn");
// const facultyItems = document.querySelectorAll(
//   ".faculty .grid-container .item"
// );

// filterBtns.forEach((btn) => {
//   btn.addEventListener("click", () => {
//     const filter = btn.dataset.filter;

//     filterBtns.forEach((b) => b.classList.remove("active"));
//     btn.classList.add("active");

//     facultyItems.forEach((item) => {
//       const designation = item
//         .querySelector(".designation")
//         .textContent.toLowerCase();
//       let shouldShow = false;

//       if (filter === "all") {
//         shouldShow = true;
//       } else if (
//         filter === "professor" &&
//         designation.includes("professor") &&
//         !designation.includes("assistant") &&
//         !designation.includes("associate")
//       ) {
//         shouldShow = true;
//       } else if (
//         filter === "associate" &&
//         designation.includes("associate professor")
//       ) {
//         shouldShow = true;
//       } else if (
//         filter === "assistant" &&
//         designation.includes("assistant professor")
//       ) {
//         shouldShow = true;
//       }

//       item.classList.toggle("hidden", !shouldShow);
//     });

//     const container = btn
//       .closest(".container")
//       .querySelector(".grid-container");
//     const showBtn = btn.closest(".container").querySelector(".show-more-btn");
//     container.classList.add("collapsed");
//     showBtn.textContent = "Show More ";
//     showBtn.querySelector("i").style.transform = "rotate(0deg)";

//     const visibleItems = Array.from(
//       container.querySelectorAll(".item:not(.hidden)")
//     );
//     visibleItems.forEach((item, index) => {
//       item.classList.toggle("collapsed-hidden", index >= 3);
//     });
//   });
// });

// document.querySelectorAll(".grid-container.collapsed").forEach((container) => {
//   const visibleItems = Array.from(
//     container.querySelectorAll(".item:not(.hidden)")
//   );
//   visibleItems.forEach((item, index) => {
//     item.classList.toggle("collapsed-hidden", index >= 3);
//   });
// });

// const observer = new IntersectionObserver((entries) => {
//   entries.forEach((entry) => {
//     if (entry.isIntersecting) {
//       entry.target.style.opacity = 1;
//       entry.target.style.transform = "translateY(0)";
//     }
//   });
// });

// document.querySelectorAll(".card").forEach((el) => {
//   el.style.opacity = 0;
//   el.style.transform = "translateY(20px)";
//   el.style.transition = "all 0.4s ease-out";
//   observer.observe(el);
// });
