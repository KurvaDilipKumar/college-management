let index = 1;
const container = document.querySelector(".testimonial-container");
const testimonials = document.querySelectorAll(".testimonial");
const totalTestimonials = testimonials.length;

// Clone first and last elements for smooth looping
const firstClone = testimonials[0].cloneNode(true);
const lastClone = testimonials[totalTestimonials - 1].cloneNode(true);

container.appendChild(firstClone);
container.insertBefore(lastClone, testimonials[0]);

container.style.transform = `translateX(-100%)`;

function updateTestimonial() {
  container.style.transition = "transform 0.6s ease-in-out";
  container.style.transform = `translateX(-${index * 100}%)`;
}

function nextTestimonial() {
  if (index >= totalTestimonials) {
    index++;
    updateTestimonial();
    setTimeout(() => {
      container.style.transition = "none";
      index = 1;
      container.style.transform = `translateX(-${index * 100}%)`;
    }, 600);
  } else {
    index++;
    updateTestimonial();
  }
}

function prevTestimonial() {
  if (index <= 0) {
    index--;
    updateTestimonial();
    setTimeout(() => {
      container.style.transition = "none";
      index = totalTestimonials;
      container.style.transform = `translateX(-${index * 100}%)`;
    }, 600);
  } else {
    index--;
    updateTestimonial();
  }
}

setInterval(nextTestimonial, 3000); // Auto-slide every 5 seconds
