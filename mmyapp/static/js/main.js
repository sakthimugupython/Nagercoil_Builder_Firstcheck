/**
 * Nagercoil Builders - Main JavaScript
 * Interactive features and animations
 */

// ========== Document Ready ==========
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functions
    initNavbar();
    initScrollAnimations();
    initSmoothScroll();
    initFormValidation();
    initCounter();
});

// ========== Navbar Scroll Effect ==========
function initNavbar() {
    const navbar = document.getElementById('mainNav');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Change navbar style on scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // Update active nav link based on scroll position
        updateActiveNavLink();
    });
    
    // Mobile menu close on link click
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            const navbarCollapse = document.querySelector('.navbar-collapse');
            if (navbarCollapse.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                bsCollapse.hide();
            }
        });
    });
}

// ========== Update Active Nav Link ==========
function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        if (window.pageYOffset >= sectionTop - 150) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

// ========== Smooth Scroll ==========
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Check if it's a valid section ID
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                
                const target = document.querySelector(href);
                const offsetTop = target.offsetTop - 80;
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ========== Scroll Animations with Intersection Observer ==========
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                
                // Add animation classes
                if (entry.target.hasAttribute('data-aos')) {
                    entry.target.classList.add('aos-animate');
                }
            }
        });
    }, observerOptions);
    
    // Observe all elements with data-aos attribute
    const animatedElements = document.querySelectorAll('[data-aos]');
    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'all 0.6s ease';
        observer.observe(element);
    });
}

// ========== Animated Counter ==========
function initCounter() {
    const counters = document.querySelectorAll('.stat-number');
    const speed = 200;
    let hasAnimated = false;
    
    const animateCounters = () => {
        if (hasAnimated) return;
        
        counters.forEach(counter => {
            const target = parseInt(counter.innerText.replace(/\D/g, ''));
            const suffix = counter.innerText.replace(/[0-9]/g, '');
            const increment = target / speed;
            let current = 0;
            
            const updateCounter = () => {
                current += increment;
                if (current < target) {
                    counter.innerText = Math.ceil(current) + suffix;
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.innerText = target + suffix;
                }
            };
            
            updateCounter();
        });
        
        hasAnimated = true;
    };
    
    // Trigger counter animation when stats section is visible
    const statsSection = document.querySelector('.hero-stats');
    if (statsSection) {
        const statsObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounters();
                }
            });
        }, { threshold: 0.5 });
        
        statsObserver.observe(statsSection);
    }
}

// ========== Form Validation ==========
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form inputs
            const inputs = form.querySelectorAll('input, textarea');
            let isValid = true;
            
            inputs.forEach(input => {
                if (input.hasAttribute('required') && !input.value.trim()) {
                    isValid = false;
                    showError(input, 'This field is required');
                } else {
                    removeError(input);
                }
                
                // Email validation
                if (input.type === 'email' && input.value.trim()) {
                    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailPattern.test(input.value)) {
                        isValid = false;
                        showError(input, 'Please enter a valid email address');
                    }
                }
            });
            
            if (isValid) {
                showSuccessMessage();
                form.reset();
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.hasAttribute('required') && !this.value.trim()) {
                    showError(this, 'This field is required');
                } else {
                    removeError(this);
                }
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    removeError(this);
                }
            });
        });
    });
}

// ========== Form Error Handling ==========
function showError(input, message) {
    input.classList.add('is-invalid');
    
    // Remove existing error message
    const existingError = input.parentElement.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
    
    // Create new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback d-block';
    errorDiv.textContent = message;
    input.parentElement.appendChild(errorDiv);
}

function removeError(input) {
    input.classList.remove('is-invalid');
    const errorDiv = input.parentElement.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// ========== Success Message ==========
function showSuccessMessage() {
    // Create success alert
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show position-fixed';
    alert.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
    alert.innerHTML = `
        <strong><i class="fas fa-check-circle me-2"></i>Success!</strong>
        Your message has been sent successfully. We'll get back to you soon!
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alert);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// ========== Card Hover Effects ==========
document.querySelectorAll('.service-card, .project-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-10px)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

// ========== Parallax Effect ==========
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.hero-content');
    
    parallaxElements.forEach(element => {
        const speed = 0.5;
        element.style.transform = `translateY(${scrolled * speed}px)`;
    });
});

// ========== Button Ripple Effect ==========
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
        `;
        
        this.style.position = 'relative';
        this.style.overflow = 'hidden';
        this.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    });
});

// Add ripple animation to CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ========== Back to Top Button ==========
const createBackToTopButton = () => {
    const button = document.createElement('button');
    button.innerHTML = '<i class="fas fa-arrow-up"></i>';
    button.className = 'back-to-top';
    button.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #dd613d, #f1da6f);
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 999;
        box-shadow: 0 4px 15px rgba(221, 97, 61, 0.3);
    `;
    
    button.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            button.style.opacity = '1';
            button.style.visibility = 'visible';
        } else {
            button.style.opacity = '0';
            button.style.visibility = 'hidden';
        }
    });
    
    button.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1) translateY(-5px)';
    });
    
    button.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1) translateY(0)';
    });
    
    document.body.appendChild(button);
};

createBackToTopButton();

// ========== Loading Animation ==========
window.addEventListener('load', function() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// ========== Console Message ==========
console.log('%c🏗️ Nagercoil Builders', 'font-size: 20px; font-weight: bold; color: #dd613d;');
console.log('%cBuilding Dreams Into Reality', 'font-size: 14px; color: #f1da6f;');
console.log('%cWebsite powered by modern web technologies', 'font-size: 12px; color: #6c757d;');
