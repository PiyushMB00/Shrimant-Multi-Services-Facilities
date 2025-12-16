'use strict';

/**
 * Service Data
 */
const servicesData = [
  {
    id: 'vastu',
    title: 'Vastu Consultant',
    image: 'images/vastu co.jpg',
    intro: 'Vastu Consultant Services',
    description: `
      <p>At Shrimant Multi Facilities & Services 79, our Vastu consulting services are designed to bring balance, harmony, and positive energy into residential, commercial, and industrial spaces. Vastu Shastra is not about superstition; it is about scientific alignment of space, direction, and natural elements to improve well-being, productivity, and peace of mind.</p>
      <p>We provide complete Vastu guidance for homes, flats, bungalows, offices, shops, factories, and commercial establishments. Our approach focuses on practical corrections, not demolition-heavy changes.</p>
    `
  },
  {
    id: 'interior',
    title: 'Interior Designer',
    image: 'images/interior-design shrimant.jpg',
    intro: 'Interior Design Services',
    description: `
      <p>Our interior design services focus on creating spaces that are functional, elegant, and aligned with the client’s lifestyle or business needs. At Shrimant Multi Facilities & Services 79, we believe good design should improve daily living, not complicate it.</p>
      <p>We offer complete interior solutions for homes, offices, retail spaces, and commercial properties.</p>
    `
  },
  {
    id: 'printing',
    title: 'Design & Printing',
    image: 'images/logo.jpg',
    intro: 'Design & Printing Services',
    description: `
      <p>Our design and printing services cater to businesses, events, and individuals who require high-quality visual communication. From concept to final print, we manage the entire process to ensure consistency and clarity.</p>
      <p>We provide graphic design services for visiting cards, banners, brochures, posters, flyers, hoardings, invitations, and promotional materials.</p>
    `
  },
  {
    id: 'event',
    title: 'Event Management',
    image: 'images/Event M.jpg',
    intro: 'Event Management Services',
    description: `
      <p>We provide end-to-end event management services for personal, social, and corporate events. Our responsibility is simple: manage everything smoothly so clients can focus on enjoying the event.</p>
      <p>Our services include planning, coordination, vendor management, decoration, scheduling, and on-ground supervision.</p>
    `
  },
  {
    id: 'photography',
    title: 'Photography',
    image: 'images/photography 2.jpg',
    intro: 'Photography Services',
    description: `
      <p>Our photography services focus on capturing moments with clarity, emotion, and professional quality. We understand that photographs are long-term memories, not temporary visuals.</p>
      <p>We offer photography services for events, corporate needs, personal shoots, and special occasions.</p>
    `
  },
  {
    id: 'prewedding',
    title: 'Pre Wedding Shooting',
    image: 'images/photography im.jpg',
    intro: 'Pre Wedding Shooting Services',
    description: `
      <p>Pre-wedding shoots are about storytelling. Our approach focuses on capturing genuine emotions, comfort, and connection between couples.</p>
      <p>We assist with location selection, concept planning, outfit coordination, and shoot scheduling.</p>
    `
  },
  {
    id: 'residence-painting',
    title: 'Residence Painting',
    image: 'images/residantal.jpg',
    intro: 'Residence Painting Services',
    description: `
      <p>Our residence painting services are designed to enhance the beauty and durability of homes. We handle both interior and exterior painting with professional execution.</p>
      <p>We assist clients in selecting suitable colors, finishes, and materials based on lighting, room usage, and maintenance needs.</p>
    `
  },
  {
    id: 'commercial-painting',
    title: 'Commercial Painting',
    image: 'images/commercial.jpg',
    intro: 'Commercial Painting Services',
    description: `
      <p>Commercial painting requires speed, precision, and durability. We provide painting solutions for offices, shops, buildings, and industrial spaces.</p>
      <p>Our team follows safety standards, project timelines, and professional execution methods.</p>
    `
  },
  {
    id: 'legal',
    title: 'Legal Advice',
    image: 'images/legal-advisor_cover_web.jpg',
    intro: 'Legal Advice Services',
    description: `
      <p>We provide basic legal guidance and advisory support to individuals and businesses through trusted legal professionals.</p>
      <p>Our service focuses on clarity, documentation support, and initial legal direction.</p>
    `
  }
];


/**
 * PRELOADER
 */
const preloader = document.querySelector("[data-preload]");

window.addEventListener("load", function () {
  if (preloader) {
    preloader.classList.add("loaded");
    document.body.classList.add("loaded");
  }
  
  // Handle Detail Page Load
  const params = new URLSearchParams(window.location.search);
  const serviceId = params.get('id');
  if (serviceId) {
    loadServiceDetails(serviceId);
  }
});


/**
 * CAROUSEL LOGIC
 */
const sliderTrack = document.querySelector("[data-slider-track]");
const prevBtn = document.querySelector("[data-prev-btn]");
const nextBtn = document.querySelector("[data-next-btn]");

if (sliderTrack && prevBtn && nextBtn) {
  let currentSlide = 0;
  // We want to show 3 items. 
  // 9 items total.
  // Max Slide Index should be such that the last 3 are visible.
  // 33.33% width.
  // Total Slides = 9.
  // Max Index = 9 - 3 = 6. (0 to 6)
  
  const moveSlider = () => {
    // If mobile, card width is 100%, so we behave differently?
    // For now, assume simplified uniform approach or rely on CSS media queries
    // Actually JS needs to know how much to translate.
    // Let's assume 33.33% shift for Desktop.
    // Ideally we detect window width.
    
    const cardWidth = sliderTrack.children[0].getBoundingClientRect().width;
    sliderTrack.style.transform = `translateX(-${currentSlide * cardWidth}px)`;
  };

  const nextSlide = () => {
    // Determine visible items based on window width
    let visibleItems = window.innerWidth < 768 ? 1 : 3;
    let maxSlide = servicesData.length - visibleItems;

    if (currentSlide >= maxSlide) {
      currentSlide = 0; // Loop back
    } else {
      currentSlide++;
    }
    moveSlider();
  };

  const prevSlide = () => {
    let visibleItems = window.innerWidth < 768 ? 1 : 3;
    let maxSlide = servicesData.length - visibleItems;

    if (currentSlide <= 0) {
      currentSlide = maxSlide; // Loop to end
    } else {
      currentSlide--;
    }
    moveSlider();
  };

  nextBtn.addEventListener("click", nextSlide);
  prevBtn.addEventListener("click", prevSlide);

  // Auto Slide
  let autoSlideInterval = setInterval(nextSlide, 5000);
  
  const stopAutoSlide = () => clearInterval(autoSlideInterval);
  const startAutoSlide = () => autoSlideInterval = setInterval(nextSlide, 5000);

  [nextBtn, prevBtn, sliderTrack].forEach(el => {
    el.addEventListener("mouseover", stopAutoSlide);
    el.addEventListener("mouseout", startAutoSlide);
  });
  
  // Update on resize
  window.addEventListener('resize', moveSlider);
}


/**
 * DETAILS PAGE LOGIC
 */
function loadServiceDetails(id) {
  const service = servicesData.find(s => s.id === id);
  if (service) {
    const titleEl = document.getElementById('service-title');
    const imgEl = document.getElementById('service-image');
    const introEl = document.getElementById('service-intro');
    const descEl = document.getElementById('service-desc');

    if (titleEl) titleEl.innerText = service.title;
    if (imgEl) imgEl.src = service.image;
    if (introEl) introEl.innerText = service.intro;
    if (descEl) descEl.innerHTML = service.description;
  }
}
