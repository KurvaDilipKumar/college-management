let hasAnimated = false; // Flag to track if animation has already run

function countUp() {
    const counters = document.querySelectorAll(".count-up");
    const duration = 2000; // Duration for the entire animation in milliseconds (default 2 seconds)
  
    counters.forEach((counter) => {
        const target = +counter.getAttribute("data-count");
        const startValue = 0;
        const increment = (target / duration) * 100; // Increment per 100ms for smooth animation
  
        let currentValue = startValue;
        const intervalTime = 100; // Update every 100ms
  
        const interval = setInterval(() => {
            currentValue += increment;
            if (currentValue >= target) {
                currentValue = target;
                clearInterval(interval); // Stop the interval once we reach the target
            }
            counter.innerText = Math.ceil(currentValue); // Update the displayed number
        }, intervalTime);
    });
}

function handleIntersection(entries, observer) {
    if (hasAnimated) return; // Prevent multiple executions
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            countUp(); // Trigger count-up when the grid enters the viewport
            hasAnimated = true; // Set flag to true to prevent re-triggering
            observer.disconnect(); // Stop observing once the animation is triggered
        }
    });
}

// Set up Intersection Observer to watch for the grid section
const observerOptions = {
    root: null, // Viewport
    rootMargin: "0px 0px -40% 0px", // Trigger when 40% of the element is in view
    threshold: 0.7, // Trigger when the element comes into view
};

const observer = new IntersectionObserver(handleIntersection, observerOptions);

// Observe only the first grid item to trigger the animation once
const firstItem = document.querySelector(".glance-card-item");
if (firstItem) observer.observe(firstItem);
