// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
  initTheme();
  initSmoothScroll();
  initContactForm();
  initActiveNavOnScroll();
  initCounters();
  initNavbarScrollEffect();
  initMagneticButtons();
});

// ========== THEME MANAGEMENT ==========
function initTheme() {
  const setTheme = (theme) => {
    if (theme === 'dark') {
      document.body.classList.add('dark-theme');
      localStorage.setItem('secops_theme', 'dark');
      document.getElementById('darkModeBtn')?.classList.add('active');
      document.getElementById('lightModeBtn')?.classList.remove('active');
    } else {
      document.body.classList.remove('dark-theme');
      localStorage.setItem('secops_theme', 'light');
      document.getElementById('lightModeBtn')?.classList.add('active');
      document.getElementById('darkModeBtn')?.classList.remove('active');
    }
  };

  const savedTheme = localStorage.getItem('secops_theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    setTheme('dark');
  } else {
    setTheme('light');
  }

  const lightBtn = document.getElementById('lightModeBtn');
  const darkBtn = document.getElementById('darkModeBtn');
  if (lightBtn) lightBtn.addEventListener('click', () => setTheme('light'));
  if (darkBtn) darkBtn.addEventListener('click', () => setTheme('dark'));
}

// ========== SMOOTH SCROLL ==========
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId && targetId !== '#') {
        const target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          
          // Update active class on nav links
          document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
          });
          this.classList.add('active');
        }
      }
    });
  });
}

// ========== CONTACT FORM (Simulated) ==========
function initContactForm() {
  const contactForm = document.getElementById('contactForm');
  const feedbackDiv = document.getElementById('formFeedback');
  
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('nameInput')?.value.trim();
      const email = document.getElementById('emailInput')?.value.trim();
      const msg = document.getElementById('msgInput')?.value.trim();
      
      if (!name || !email) {
        feedbackDiv.innerHTML = '<span style="color:#ff6b35;"><i class="fas fa-exclamation-triangle"></i> Please fill name and email.</span>';
        return;
      }
      
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        feedbackDiv.innerHTML = '<span style="color:#ff6b35;"><i class="fas fa-exclamation-triangle"></i> Please enter a valid email.</span>';
        return;
      }
      
      feedbackDiv.innerHTML = '<span style="color:#2e7d64;"><i class="fas fa-check-circle"></i> Thanks! I\'ll get back to you within 24h.</span>';
      contactForm.reset();
      setTimeout(() => { feedbackDiv.innerHTML = ''; }, 4000);
    });
  }
}

// ========== ACTIVE NAV ON SCROLL ==========
function initActiveNavOnScroll() {
  const sections = document.querySelectorAll('section[id]');
  
  window.addEventListener('scroll', () => {
    let current = '';
    const scrollY = window.pageYOffset;
    
    sections.forEach(section => {
      const sectionTop = section.offsetTop - 120;
      const sectionHeight = section.offsetHeight;
      if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
        current = section.getAttribute('id');
      }
    });
    
    document.querySelectorAll('.nav-link').forEach(link => {
      link.classList.remove('active');
      const href = link.getAttribute('href');
      if (href === `#${current}`) {
        link.classList.add('active');
      } else if (current === '' && href === '#home') {
        link.classList.add('active');
      }
    });
  });
}

// ========== COUNTER ANIMATION ==========
function initCounters() {
  function animateCounter(element, target, duration = 2000) {
    if (!element) return;
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        element.textContent = target.toLocaleString();
        clearInterval(timer);
      } else {
        element.textContent = Math.floor(current).toLocaleString();
      }
    }, 16);
  }
  
  const observerOptions = { threshold: 0.5, rootMargin: '0px 0px -50px 0px' };
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const counters = entry.target.querySelectorAll('[data-count]');
        counters.forEach(counter => {
          const target = parseInt(counter.dataset.count);
          animateCounter(counter, target);
        });
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  
  document.querySelectorAll('.stat-card').forEach(item => {
    observer.observe(item);
  });
}

// ========== NAVBAR SCROLL EFFECT ==========
function initNavbarScrollEffect() {
  let lastScrollTop = 0;
  const navbar = document.querySelector('.navbar');
  
  window.addEventListener('scroll', () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (navbar) {
      if (scrollTop > 100) {
        navbar.style.boxShadow = '0 8px 25px rgba(0,0,0,0.1)';
      } else {
        navbar.style.boxShadow = '0 6px 18px rgba(0,0,0,0.03)';
      }
      
      // Hide/show navbar on scroll direction (optional)
      if (scrollTop > lastScrollTop && scrollTop > 200) {
        navbar.style.transform = 'translateY(-100%)';
        navbar.style.transition = 'transform 0.3s ease';
      } else {
        navbar.style.transform = 'translateY(0)';
      }
      lastScrollTop = scrollTop;
    }
  });
}

// ========== MAGNETIC BUTTON EFFECT ==========
function initMagneticButtons() {
  let animationFrame;
  
  function magneticEffect(button, e) {
    if (animationFrame) cancelAnimationFrame(animationFrame);
    animationFrame = requestAnimationFrame(() => {
      const rect = button.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      button.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
    });
  }
  
  function resetMagneticEffect(button) {
    if (animationFrame) cancelAnimationFrame(animationFrame);
    button.style.transform = 'translate(0, 0)';
  }
  
  document.querySelectorAll('.btn-soft-primary, .btn-outline-accent').forEach(button => {
    button.addEventListener('mousemove', (e) => magneticEffect(button, e));
    button.addEventListener('mouseleave', () => resetMagneticEffect(button));
  });
}

// ========== KEYBOARD SHORTCUTS (Bonus) ==========
document.addEventListener('keydown', function(e) {
  if (e.key === '?') {
    showShortcutsHelp();
  }
});

function showShortcutsHelp() {
  const toast = document.createElement('div');
  toast.className = 'alert alert-info fade show position-fixed';
  toast.style.cssText = 'bottom: 20px; right: 20px; z-index: 10000; min-width: 250px; background: #ff6b35; color: white; border: none; border-radius: 16px;';
  toast.innerHTML = `
    <strong>⌨️ Shortcuts</strong><br>
    <kbd style="background:white;color:#333;padding:2px 6px;border-radius:6px;">?</kbd> Show this menu<br>
    <button type="button" class="btn-close btn-close-white" onclick="this.parentElement.remove()" style="float:right;"></button>
  `;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}