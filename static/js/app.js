/* Enhanced JavaScript for AI Generator Web App */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the app
    initializeApp();
});

function initializeApp() {
    // Add animations to elements
    animateOnScroll();
    
    // Initialize theme toggle
    initializeThemeToggle();
    
    // Enhanced form handling
    enhanceFormSubmissions();
    
    // Add loading overlays
    setupLoadingOverlays();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Add particle background effect
    createParticleBackground();
    
    // Initialize copy to clipboard functionality
    initializeCopyToClipboard();
    
    // Add keyboard shortcuts
    setupKeyboardShortcuts();
    
    // Initialize image gallery enhancements
    initializeImageGallery();
}

// Animate elements on scroll
function animateOnScroll() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe cards and other elements
    document.querySelectorAll('.card, .jumbotron, .feature-card').forEach(el => {
        observer.observe(el);
    });
}

// Theme toggle functionality
function initializeThemeToggle() {
    // Create theme toggle button
    const toggleButton = document.createElement('button');
    toggleButton.className = 'theme-toggle';
    toggleButton.innerHTML = '<i class="bi bi-moon-fill"></i>';
    toggleButton.setAttribute('aria-label', 'Toggle dark mode');
    document.body.appendChild(toggleButton);
    
    // Get stored theme preference
    const currentTheme = localStorage.getItem('theme') || 'light';
    setTheme(currentTheme);
    
    toggleButton.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Animate the toggle
        toggleButton.style.transform = 'scale(0.8) rotate(180deg)';
        setTimeout(() => {
            toggleButton.style.transform = 'scale(1) rotate(0deg)';
        }, 150);
    });
    
    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        const icon = theme === 'dark' ? 'bi-sun-fill' : 'bi-moon-fill';
        toggleButton.innerHTML = `<i class="bi ${icon}"></i>`;
    }
}

// Enhanced form submissions
function enhanceFormSubmissions() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                // Store original content
                const originalContent = submitBtn.innerHTML;
                
                // Add loading state
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Generating...';
                submitBtn.disabled = true;
                submitBtn.classList.add('generating');
                
                // Show loading overlay
                showLoadingOverlay();
                
                // Add progress simulation
                simulateProgress();
                
                // Restore button after form submission (in case of errors)
                setTimeout(() => {
                    if (submitBtn.disabled) {
                        submitBtn.innerHTML = originalContent;
                        submitBtn.disabled = false;
                        submitBtn.classList.remove('generating');
                        hideLoadingOverlay();
                    }
                }, 30000); // 30 second timeout
            }
        });
    });
}

// Loading overlay functionality
function setupLoadingOverlays() {
    // Create loading overlay
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.id = 'loadingOverlay';
    overlay.innerHTML = `
        <div class="text-center">
            <div class="loading-spinner"></div>
            <div class="mt-3">
                <h5>Generating your content...</h5>
                <p class="text-muted">This may take a few moments</p>
                <div class="progress mt-3" style="width: 300px;">
                    <div class="progress-bar" id="progressBar" style="width: 0%"></div>
                </div>
                <small class="text-muted mt-2 d-block" id="progressText">Initializing...</small>
            </div>
        </div>
    `;
    document.body.appendChild(overlay);
}

function showLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.add('show');
    }
}

function hideLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.remove('show');
    }
}

function simulateProgress() {
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    
    if (!progressBar || !progressText) return;
    
    const stages = [
        { progress: 10, text: 'Loading model...' },
        { progress: 30, text: 'Processing prompt...' },
        { progress: 50, text: 'Generating content...' },
        { progress: 75, text: 'Applying filters...' },
        { progress: 90, text: 'Finalizing...' },
        { progress: 100, text: 'Complete!' }
    ];
    
    let currentStage = 0;
    
    function updateProgress() {
        if (currentStage < stages.length) {
            const stage = stages[currentStage];
            progressBar.style.width = stage.progress + '%';
            progressText.textContent = stage.text;
            currentStage++;
            setTimeout(updateProgress, 2000 + Math.random() * 3000);
        }
    }
    
    updateProgress();
}

// Initialize tooltips
function initializeTooltips() {
    // Add tooltips to form elements
    const tooltipElements = [
        { selector: 'input[name="steps"]', text: 'More steps usually mean better quality but take longer to generate' },
        { selector: 'input[name="guidance"]', text: 'Higher values make the AI follow your prompt more closely' },
        { selector: 'input[name="seed"]', text: 'Use the same seed to get reproducible results' },
        { selector: 'input[name="strength"]', text: 'Controls how much the image should be changed (0.1 = subtle, 1.0 = dramatic)' }
    ];
    
    tooltipElements.forEach(({ selector, text }) => {
        const element = document.querySelector(selector);
        if (element) {
            element.setAttribute('title', text);
            element.setAttribute('data-bs-toggle', 'tooltip');
            element.setAttribute('data-bs-placement', 'top');
        }
    });
    
    // Initialize Bootstrap tooltips
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Particle background effect
function createParticleBackground() {
    const canvas = document.createElement('canvas');
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '-1';
    canvas.style.opacity = '0.1';
    document.body.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    let particles = [];
    
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    function createParticles() {
        particles = [];
        const numberOfParticles = Math.floor((canvas.width * canvas.height) / 10000);
        
        for (let i = 0; i < numberOfParticles; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 2 + 1
            });
        }
    }
    
    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1;
            if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1;
            
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fillStyle = '#667eea';
            ctx.fill();
        });
        
        requestAnimationFrame(animateParticles);
    }
    
    resizeCanvas();
    createParticles();
    animateParticles();
    
    window.addEventListener('resize', () => {
        resizeCanvas();
        createParticles();
    });
}

// Copy to clipboard functionality
function initializeCopyToClipboard() {
    // Add copy buttons to generated file names
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('copy-filename')) {
            const filename = e.target.getAttribute('data-filename');
            navigator.clipboard.writeText(filename).then(() => {
                showToast('Filename copied to clipboard!', 'success');
            });
        }
    });
}

// Keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit forms
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeForm = document.activeElement.closest('form');
            if (activeForm) {
                e.preventDefault();
                activeForm.submit();
            }
        }
        
        // Ctrl/Cmd + D to toggle dark mode
        if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
            e.preventDefault();
            document.querySelector('.theme-toggle').click();
        }
        
        // Escape to close overlays
        if (e.key === 'Escape') {
            hideLoadingOverlay();
        }
    });
}

// Image gallery enhancements
function initializeImageGallery() {
    // Add lightbox functionality to images
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('preview-image') || e.target.tagName === 'IMG') {
            if (e.target.closest('.file-card')) {
                showImageLightbox(e.target.src, e.target.alt);
            }
        }
    });
}

function showImageLightbox(src, alt) {
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    
    const img = document.createElement('img');
    img.src = src;
    img.alt = alt;
    img.style.cssText = `
        max-width: 90%;
        max-height: 90%;
        object-fit: contain;
        border-radius: 12px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    `;
    
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '&times;';
    closeBtn.style.cssText = `
        position: absolute;
        top: 20px;
        right: 20px;
        background: none;
        border: none;
        color: white;
        font-size: 2rem;
        cursor: pointer;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
    `;
    
    lightbox.appendChild(img);
    lightbox.appendChild(closeBtn);
    document.body.appendChild(lightbox);
    
    // Trigger animation
    setTimeout(() => {
        lightbox.style.opacity = '1';
    }, 10);
    
    function closeLightbox() {
        lightbox.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(lightbox);
        }, 300);
    }
    
    closeBtn.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeLightbox();
        }
    });
}

// Toast notification system
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        z-index: 10001;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
        border-left: 4px solid var(--primary-color);
    `;
    
    toast.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="bi bi-check-circle-fill text-success me-2"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
    }, 10);
    
    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Form validation enhancements
function enhanceFormValidation() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Check required fields
            form.querySelectorAll('[required]').forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            // Check prompt length
            const promptField = form.querySelector('textarea[name="prompt"]');
            if (promptField && promptField.value.trim().length < 3) {
                promptField.classList.add('is-invalid');
                showToast('Prompt must be at least 3 characters long', 'error');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
}

// Initialize enhanced form validation
document.addEventListener('DOMContentLoaded', function() {
    enhanceFormValidation();
});