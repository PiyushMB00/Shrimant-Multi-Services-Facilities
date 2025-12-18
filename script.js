'use strict';

// ---------------------------------------------------------
// DATA (Service Details)
// ---------------------------------------------------------
const servicesData = [
  {
    id: 'vastu',
    title: 'Vastu Consultant',
    image: 'images/vastu-consultant.jpg',
    intro: 'Professional Vastu Consultation for Homes and Offices',
    description: `
      <p>Our Vastu Consultant service helps improve harmony, balance, and energy flow in residential and commercial spaces. We connect you with experienced Vastu professionals who analyze layouts, directions, and spatial planning to provide practical guidance based on Vastu principles.</p>
      <p>Our approach focuses on realistic solutions without unnecessary structural changes. Whether you are planning a new property, renovating an existing space, or facing challenges in your workplace, our consultants offer clear and actionable recommendations.</p>
    `,
    featuresTitle: 'What We Offer',
    features: [
      'Home and apartment Vastu consultation',
      'Office and commercial Vastu guidance',
      'Layout correction suggestions',
      'Direction and space optimization'
    ],
    note: 'Consultations are assigned based on availability and project requirements.'
  },
  {
    id: 'interior',
    title: 'Interior Designer',
    image: 'images/interior-design.jpg',
    intro: 'Interior Design Solutions for Residential and Commercial Spaces',
    description: `
      <p>We offer professional Interior Design services tailored to your space, budget, and lifestyle. Our network of interior designers specializes in space planning, material selection, lighting design, and functional layouts.</p>
      <p>Whether you need complete interior design or selective design assistance, we ensure practical execution with long-term usability in mind. Each project is handled by a designer best suited to the scope and requirements.</p>
    `,
    featuresTitle: 'Our Interior Design Services',
    features: [
      'Home interior design',
      'Office and commercial interiors',
      'Space planning and layout design',
      'Material and color selection'
    ],
    note: 'Projects are assigned based on availability and expertise.'
  },
  {
    id: 'printing',
    title: 'Design & Printing',
    image: 'images/logo.jpg',
    intro: 'Creative Design and High-Quality Printing Solutions',
    description: `
      <p>Our Design & Printing service provides end-to-end solutions for branding, marketing, and promotional needs. From creative design to professional printing, we ensure consistency and quality across all materials.</p>
      <p>We handle both digital and physical design requirements with clear specifications and approval processes.</p>
    `,
    featuresTitle: 'Services Include',
    features: [
      'Graphic design and branding',
      'Visiting cards, brochures, banners',
      'Posters and marketing materials',
      'Custom printing solutions'
    ],
    note: 'All work is delivered as per agreed timelines and specifications.'
  },
  {
    id: 'event',
    title: 'Event Management',
    image: 'images/event-management.jpg',
    intro: 'End-to-End Event Planning and Management',
    description: `
      <p>Our Event Management service covers planning, coordination, and execution of events with structured workflows and reliable professionals. We manage logistics, vendors, scheduling, and on-site coordination to ensure smooth execution.</p>
      <p>Each event is handled based on its type, scale, and requirements.</p>
    `,
    featuresTitle: 'Types of Events We Manage',
    features: [
      'Corporate events',
      'Private functions and celebrations',
      'Social and cultural events'
    ],
    note: 'Event teams are assigned strictly on a project basis.'
  },
  {
    id: 'photography',
    title: 'Photography',
    image: 'images/photography.jpg',
    intro: 'Professional Photography for Events and Commercial Use',
    description: `
      <p>We offer Photography services focused on clarity, composition, and purpose-driven visuals. Our photographers handle events, portraits, product shoots, and commercial photography with professional planning and execution.</p>
      <p>Every assignment is scoped clearly to meet client expectations and delivery timelines.</p>
    `,
    featuresTitle: 'Photography Services Offered',
    features: [
      'Event photography',
      'Portrait photography',
      'Product and commercial shoots'
    ],
    note: 'Photographers are assigned based on availability and style requirements.'
  },
  {
    id: 'prewedding',
    title: 'Pre Wedding Shoots',
    image: 'images/prewedding.jpg',
    intro: 'Creative and Natural Pre-Wedding Photography',
    description: `
      <p>Our Pre-Wedding Shoot service captures genuine moments and personal stories in a relaxed and creative environment. We focus on natural expressions, storytelling, and well-planned locations rather than forced poses.</p>
      <p>From concept discussion to final delivery, every shoot is planned in advance to ensure a smooth experience.</p>
    `,
    featuresTitle: 'What We Cover',
    features: [
      'Concept-based pre-wedding shoots',
      'Outdoor and location shoots',
      'Theme planning and coordination'
    ],
    note: 'Shoot assignments depend on availability and requirements.'
  },
  {
    id: 'residence-painting',
    title: 'Residence Painting',
    image: 'images/residential-painting.jpg',
    intro: 'Professional House Painting Services',
    description: `
      <p>Our Residence Painting service provides skilled painters for homes, apartments, and residential properties. We focus on surface preparation, clean execution, and durable finishes.</p>
      <p>Projects are planned to minimize disruption while ensuring timely and quality completion.</p>
    `,
    featuresTitle: 'Residential Painting Solutions',
    features: [
      'Interior house painting',
      'Exterior home painting',
      'Repainting and touch-up services'
    ],
    note: 'Painters are assigned based on location and project size.'
  },
  {
    id: 'commercial-painting',
    title: 'Commercial Painting',
    image: 'images/commercial-painting.jpg',
    intro: 'Reliable Painting Solutions for Commercial Properties',
    description: `
      <p>Our Commercial Painting service is designed for offices, shops, buildings, and industrial spaces. We understand the importance of timelines, safety, and minimal operational disruption.</p>
      <p>Large-scale projects are handled with proper planning, workforce coordination, and quality control.</p>
    `,
    featuresTitle: 'Commercial Painting Coverage',
    features: [
      'Office and corporate spaces',
      'Shops and retail outlets',
      'Buildings and industrial units'
    ],
    note: 'All work is executed strictly as per scope and schedule.'
  },
  {
    id: 'legal',
    title: 'Legal Advice',
    image: 'images/legal-advice.jpg',
    intro: 'Professional Legal Consultation and Guidance',
    description: `
      <p>Our Legal Advice service connects clients with qualified legal professionals for general consultation and guidance. This includes assistance with documentation, property matters, agreements, and compliance-related queries.</p>
      <p>The focus is on clear, practical legal advice without unnecessary complexity.</p>
    `,
    featuresTitle: 'Legal Services Include',
    features: [
      'Property and documentation advice',
      'Agreement and contract guidance',
      'General legal consultation'
    ],
    note: 'This service is advisory in nature and assigned based on query type and availability.'
  }
];

const commonNote = "Services are provided through verified professionals. Work is assigned only when available and based on project requirements. Payment terms and scope of work are finalized before project initiation.";

// ---------------------------------------------------------
// HERO SLIDER LOGIC
// ---------------------------------------------------------
const heroSliderItems = document.querySelectorAll("[data-hero-slider-item]");
const heroSliderPrevBtn = document.querySelector("[data-prev-btn]");
const heroSliderNextBtn = document.querySelector("[data-next-btn]");

let currentSlidePos = 0;
let lastActiveSliderItem = heroSliderItems[0];

const updateSliderPos = function() {
    if(!lastActiveSliderItem) return;
    lastActiveSliderItem.classList.remove("active");
    heroSliderItems[currentSlidePos].classList.add("active");
    lastActiveSliderItem = heroSliderItems[currentSlidePos];
}

const slideNext = function() {
    if (currentSlidePos >= heroSliderItems.length - 1) {
        currentSlidePos = 0;
    } else {
        currentSlidePos++;
    }
    updateSliderPos();
}

const slidePrev = function() {
    if (currentSlidePos <= 0) {
        currentSlidePos = heroSliderItems.length - 1;
    } else {
        currentSlidePos--;
    }
    updateSliderPos();
}

if (heroSliderNextBtn) heroSliderNextBtn.addEventListener("click", slideNext);
if (heroSliderPrevBtn) heroSliderPrevBtn.addEventListener("click", slidePrev);

// Auto Slide
let autoSlideInterval;
const autoSlide = function() {
    autoSlideInterval = setInterval(function () {
        slideNext();
    }, 7000);
}

if(heroSliderItems.length > 0) {
  window.addEventListener("load", autoSlide);
}


// ---------------------------------------------------------
// SERVICE DETAILS PAGE LOGIC
// ---------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  const serviceId = params.get('id');
  const serviceTitleEl = document.getElementById('service-title');

  if (serviceId && serviceTitleEl) {
    const service = servicesData.find(s => s.id === serviceId);
    if (service) {
      document.getElementById('service-title').innerText = service.title;
      document.getElementById('service-intro').innerText = service.intro;
      document.getElementById('service-desc').innerHTML = service.description;

      // Inject Features
      const featuresTitleEl = document.getElementById('service-features-title');
      const featuresListEl = document.getElementById('service-features');
      if (featuresTitleEl && featuresListEl) {
        featuresTitleEl.innerText = service.featuresTitle;
        featuresListEl.innerHTML = service.features.map(f => `<li><i class="fas fa-check-circle" style="color:var(--accent-gold); margin-right:10px;"></i> ${f}</li>`).join('');
      }

      // Inject specific note
      const serviceNoteEl = document.getElementById('service-note');
      if (serviceNoteEl) {
        serviceNoteEl.innerText = service.note;
      }

      // Inject Common Note
      const commonNoteEl = document.getElementById('common-note');
      if (commonNoteEl) {
        commonNoteEl.innerText = commonNote;
      }
    } else {
      document.getElementById('service-desc').innerHTML = '<div class="container" style="padding:50px;"><h2 style="text-align:center">Service not found.</h2></div>';
    }
  }
});