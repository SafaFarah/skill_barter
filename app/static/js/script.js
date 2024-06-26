let slideIndex = 0;
const slides = document.querySelectorAll('.slides img');
const totalSlides = slides.length;

// Function to show slides
const showSlides = () => {
    slides.forEach((slide) => {
        slide.style.display = 'none';
    });
    slides[slideIndex].style.display = 'block';
};

// Initial display of slides
showSlides();

// Function to go to the previous slide
const prevSlide = () => {
    slideIndex--;
    if (slideIndex < 0) {
        slideIndex = totalSlides - 1;
    }
    showSlides();
};

// Function to go to the next slide
const nextSlide = () => {
    slideIndex++;
    if (slideIndex >= totalSlides) {
        slideIndex = 0;
    }
    showSlides();
};
