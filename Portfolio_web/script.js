// Interactive Tech Background Canvas Animation
;(function() {
  const canvas = document.getElementById('techCanvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let particles = [];
  let animationId = null;
  let mouse = { x: null, y: null };
  let isMouseMoving = false;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  class Particle {
    constructor() {
      this.reset();
    }

    reset() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.vx = (Math.random() - 0.5) * 0.5;
      this.vy = (Math.random() - 0.5) * 0.5;
      this.radius = Math.random() * 2 + 1;
      this.alpha = Math.random() * 0.5 + 0.2;
      this.codeChar = this.getRandomCodeChar();
      this.speed = Math.random() * 0.5 + 0.2;
      this.originalX = this.x;
      this.originalY = this.y;
      this.mouseInfluence = Math.random() * 50 + 20;
    }

    getRandomCodeChar() {
      const chars = '01';
      return chars[Math.floor(Math.random() * chars.length)];
    }

    update() {
      // Mouse interaction
      if (mouse.x !== null && mouse.y !== null) {
        const dx = this.x - mouse.x;
        const dy = this.y - mouse.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < this.mouseInfluence) {
          const force = (this.mouseInfluence - distance) / this.mouseInfluence;
          this.vx += (dx / distance) * force * 0.5;
          this.vy += (dy / distance) * force * 0.5;
          this.alpha = Math.min(0.8, this.alpha + force * 0.3);
        }
      }

      // Apply velocity
      this.x += this.vx;
      this.y += this.vy;

      // Damping
      this.vx *= 0.98;
      this.vy *= 0.98;

      // Boundary check
      if (this.y > canvas.height) {
        this.y = 0;
        this.x = Math.random() * canvas.width;
        this.originalX = this.x;
        this.originalY = this.y;
      }

      // Return to original position gradually
      this.x += (this.originalX - this.x) * 0.002;
      this.y += (this.originalY - this.y) * 0.002;

      // Reset alpha
      this.alpha = Math.max(0.2, this.alpha - 0.005);
    }

    draw() {
      ctx.font = Math.max(12, this.radius * 4) + 'px "JetBrains Mono", monospace';
      const textColor = `rgba(0, 255, 65, ${this.alpha})`; // Dark theme colors
      ctx.fillStyle = textColor;
      ctx.fillText(this.codeChar, this.x, this.y);
    }
  }

  function initParticles() {
    const count = Math.min(50, Math.floor((canvas.width * canvas.height) / 20000)); // Reduced particle count for better performance
    particles = [];
    for (let i = 0; i < count; i++) {
      particles.push(new Particle());
    }
  }

  function drawConnections() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 80) { // Reduced connection distance for better performance
          ctx.beginPath();
          const lineColor = `rgba(0, 212, 255, ${0.15 * (1 - dist / 80)})`; // Dark theme colors
          ctx.strokeStyle = lineColor;
          ctx.lineWidth = 0.5;
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawConnections();

    particles.forEach(p => {
      p.update();
      p.draw();
    });

    animationId = requestAnimationFrame(animate);
  }

  // Mouse interaction
  canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
    isMouseMoving = true;
  });

  canvas.addEventListener('mouseleave', () => {
    mouse.x = null;
    mouse.y = null;
    isMouseMoving = false;
  });

  // Click effect
  canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    // Create ripple effect
    for (let i = 0; i < 5; i++) {
      const particle = new Particle();
      particle.x = clickX;
      particle.y = clickY;
      particle.vx = (Math.random() - 0.5) * 10;
      particle.vy = (Math.random() - 0.5) * 10;
      particle.alpha = 0.8;
      particles.push(particle);
    }
  });

  resize();
  initParticles();
  animate();

  window.addEventListener('resize', () => {
    resize();
    initParticles();
  });
})();

// Interactive Live Counters
;(function() {
  function animateCounter(element, target, duration = 2000) {
    if (!element) return;

    const start = parseInt(element.textContent.replace(/[^\d]/g, '')) || 0;
    const increment = (target - start) / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
      current += increment;
      if ((increment > 0 && current >= target) || (increment < 0 && current <= target)) {
        element.textContent = target.toLocaleString();
        clearInterval(timer);
      } else {
        element.textContent = Math.floor(current).toLocaleString();
      }
    }, 16);
  }

  function initCounters() {
    const observerOptions = {
      threshold: 0.5,
      rootMargin: '0px 0px -50px 0px'
    };

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

    // Observe stat items
    document.querySelectorAll('.stat-item').forEach(item => {
      observer.observe(item);
    });
  }

  // Initialize counters when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCounters);
  } else {
    initCounters();
  }
})();

// Interactive Page Transitions
;(function() {
  // Add loading states to navigation
  document.querySelectorAll('a[href]').forEach(link => {
    link.addEventListener('click', function(e) {
      if (this.hostname === window.location.hostname) {
        // Add loading class for smooth transition
        document.body.classList.add('page-transitioning');

        // Remove loading class after navigation
        setTimeout(() => {
          document.body.classList.remove('page-transitioning');
        }, 500);
      }
    });
  });
})();



// Interactive Keyboard Shortcuts
;(function() {
  document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K: Focus search (if exists)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
  // Could focus a search input if added later
    console.log('Search shortcut activated');
  }
  });

  // Add keyboard shortcut hints
  document.addEventListener('keydown', function(e) {
    if (e.key === '?') {
      showKeyboardShortcuts();
    }
  });

  function showKeyboardShortcuts() {
    const shortcuts = document.createElement('div');
    shortcuts.className = 'alert alert-info alert-dismissible fade show position-fixed';
    shortcuts.style.cssText = 'bottom: 20px; right: 20px; z-index: 10000; min-width: 250px;';
    shortcuts.innerHTML = `
      <strong>Keyboard Shortcuts:</strong><br>
      <kbd>Ctrl+K</kbd> Search<br>
      <kbd>?</kbd> Show this help<br>
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(shortcuts);
  }
})();

// Interactive Easter Eggs
;(function() {
  let clickCount = 0;
  let clickTimer;

  // Konami Code or click patterns for fun effects
  document.addEventListener('click', function(e) {
    clickCount++;

    clearTimeout(clickTimer);
    clickTimer = setTimeout(() => {
      clickCount = 0;
    }, 1000);

    // Triple click anywhere for party mode
    if (clickCount === 3) {
      triggerPartyMode();
      clickCount = 0;
    }
  });

  function triggerPartyMode() {
    document.body.style.transition = 'all 0.5s ease';
    document.body.style.filter = 'hue-rotate(180deg) saturate(1.5)';

    setTimeout(() => {
      document.body.style.filter = '';
    }, 3000);

    showNotification('🎉 Party Mode Activated!', 'success');
  }

  function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; left: 50%; transform: translateX(-50%); z-index: 10000; min-width: 300px; text-align: center;';
    notification.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
      if (notification.parentNode) {
        notification.remove();
      }
    }, 3000);
  }

  // Add keyboard shortcut hints
  document.addEventListener('keydown', function(e) {
    if (e.key === '?') {
      showKeyboardShortcuts();
    }
  });

  function showKeyboardShortcuts() {
    const shortcuts = document.createElement('div');
    shortcuts.className = 'alert alert-info alert-dismissible fade show position-fixed';
    shortcuts.style.cssText = 'bottom: 20px; right: 20px; z-index: 10000; min-width: 250px;';
    shortcuts.innerHTML = `
      <strong>Keyboard Shortcuts:</strong><br>
      <kbd>Ctrl+L</kbd> Light theme<br>
      <kbd>Ctrl+D</kbd> Dark theme<br>
      <kbd>?</kbd> Show this help<br>
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(shortcuts);
  }
})();

// Performance Monitoring
;(function() {
  // Monitor page load performance
  window.addEventListener('load', function() {
    setTimeout(() => {
      const perfData = performance.getEntriesByType('navigation')[0];
      console.log(`Page loaded in ${Math.round(perfData.loadEventEnd - perfData.fetchStart)}ms`);
    }, 0);
  });

  // Monitor user interactions
  let interactionCount = 0;
  document.addEventListener('click', () => {
    interactionCount++;
  });

  // Log performance metrics every 30 seconds
  setInterval(() => {
    if (interactionCount > 0) {
      console.log(`User interactions in last 30s: ${interactionCount}`);
      interactionCount = 0;
    }
  }, 30000);
})();

// Interactive Scroll Effects
;(function() {
  let lastScrollTop = 0;
  const navbar = document.querySelector('.navbar');

  function handleScroll() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    // Navbar scroll effects
    if (navbar) {
      if (scrollTop > 100) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }

      // Hide/show navbar on scroll direction
      if (scrollTop > lastScrollTop && scrollTop > 200) {
        navbar.style.transform = 'translateY(-100%)';
      } else {
        navbar.style.transform = 'translateY(0)';
      }
      lastScrollTop = scrollTop;
    }

    // Parallax effect for hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
      const scrolled = scrollTop * 0.5;
      heroSection.style.transform = `translateY(${scrolled}px)`;
    }
  }

  window.addEventListener('scroll', handleScroll, { passive: true });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
})();

// Interactive Hover Effects
;(function() {
  // Add magnetic effect to buttons with throttling
  let animationFrame;
  function magneticEffect(button, e) {
    if (animationFrame) cancelAnimationFrame(animationFrame);
    animationFrame = requestAnimationFrame(() => {
      const rect = button.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      button.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
    });
  }

  function resetMagneticEffect(button) {
    if (animationFrame) cancelAnimationFrame(animationFrame);
    button.style.transform = 'translate(0, 0)';
  }

  document.querySelectorAll('.btn-primary').forEach(button => {
    button.addEventListener('mousemove', (e) => magneticEffect(button, e));
    button.addEventListener('mouseleave', () => resetMagneticEffect(button));
  });

  // Add glow effect to cards on hover
  document.querySelectorAll('.work-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.animation = 'none';
      card.style.transform = 'translateY(-12px) scale(1.02)';
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'translateY(0) scale(1)';
    });
  });
})();



;(function() {
  // Nav toggle functionality for mobile
  const navToggle = document.getElementById('navToggle');
  const mainNav = document.getElementById('mainNav');
  if (navToggle && mainNav) {
    navToggle.addEventListener('click', function() {
      mainNav.classList.toggle('open');
      const isOpen = mainNav.classList.contains('open');
      navToggle.setAttribute('aria-expanded', isOpen);
      navToggle.textContent = isOpen ? '✕' : '☰';
    });
  }
})();

;(function() {
  // Contact form handling with EmailJS
  if (typeof emailjs === 'undefined') return;

  emailjs.init('NN6tpMW5E3TTzVbu5');

  const contactForm = document.getElementById('contactForm');
  const formMessage = document.getElementById('formMessage');

  if (contactForm && formMessage) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();

      const submitBtn = contactForm.querySelector('button[type="submit"]');

      const name = document.getElementById('name').value.trim();
      const email = document.getElementById('email').value.trim();
      const message = document.getElementById('message').value.trim();

      if (!name || !email || !message) {
        formMessage.textContent = 'Please fill in all fields.';
        formMessage.style.color = '#ff6b6b';
        return;
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        formMessage.textContent = 'Please enter a valid email address.';
        formMessage.style.color = '#ff6b6b';
        return;
      }

      // Disable button during send
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending...';

      formMessage.textContent = 'Sending message...';
      formMessage.style.color = '#4ecdc4';

      emailjs.send('service_ocza9rd', 'template_sxam6k9', {
        from_name: name,
        from_email: email,
        message: message,
        to_email: 'olaleyelekanjoseph@gmail.com',
        reply_to: email
      })
      .then(function(response) {
        console.log('SUCCESS!', response.status, response.text);
        formMessage.textContent = 'Thank you! Your message has been sent successfully.';
        formMessage.style.color = '#2aaf7a';
        contactForm.reset();
        setTimeout(function() {
          formMessage.textContent = '';
        }, 5000);
      }, function(error) {
        console.log('FAILED...', error);
        formMessage.textContent = 'Sorry, there was an error sending your message. Please try again or contact me directly.';
        formMessage.style.color = '#ff6b6b';
      })
      .finally(function() {
        // Re-enable button
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send message';
      });
    });
  }
})();

// Scroll reveal animations
;(function() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animated');
      }
    });
  }, observerOptions);

  document.querySelectorAll('.scroll-animate, .stagger-animate').forEach(el => {
    observer.observe(el);
  });
})();


