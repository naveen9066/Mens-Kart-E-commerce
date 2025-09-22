const API_BASE = 'http://localhost:54112/api';
const token = localStorage.getItem('token');

function apiFetch(url, options = {}) {
  options.headers = { ...options.headers, 'Content-Type': 'application/json' };
  if (token) options.headers.Authorization = `Bearer ${token}`;
  return fetch(`${API_BASE}${url}`, options).then(res => res.json());
}

// Animation and UI enhancements
function initAnimations() {
  // Header scroll effect
  const header = document.querySelector('.main-header');
  let lastScrollY = window.scrollY;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
    lastScrollY = window.scrollY;
  });

  // Reveal animations on scroll
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal');
      }
    });
  }, observerOptions);

  // Observe elements for animation
  document.querySelectorAll('.category-card, .product-card, .footer-section').forEach((el, index) => {
    el.style.setProperty('--i', index);
    observer.observe(el);
  });

  // Loading states
  function showLoading(button) {
    const originalText = button.textContent;
    button.innerHTML = '<div class="loading"></div> Loading...';
    button.disabled = true;

    setTimeout(() => {
      button.innerHTML = originalText;
      button.disabled = false;
    }, 2000);
  }

  // Enhanced button interactions
  document.querySelectorAll('.btn-primary, .add-to-cart-btn, .cta-button').forEach(btn => {
    btn.addEventListener('click', function() {
      this.style.transform = 'scale(0.95)';
      setTimeout(() => {
        this.style.transform = '';
      }, 150);
    });
  });

  // Smooth page transitions
  document.querySelectorAll('a[href^="#"], a[href*="html"]').forEach(link => {
    link.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href.includes('html') || href.startsWith('#')) {
        e.preventDefault();
        document.body.style.opacity = '0.7';
        setTimeout(() => {
          window.location.href = href;
        }, 300);
      }
    });
  });

  // Enhanced form validation
  function validateForm(form) {
    const inputs = form.querySelectorAll('input[required]');
    let isValid = true;

    inputs.forEach(input => {
      const formGroup = input.closest('.form-group');
      const message = formGroup.querySelector('.form-message') || document.createElement('div');

      if (!message.classList.contains('form-message')) {
        message.className = 'form-message';
        formGroup.appendChild(message);
      }

      if (!input.value.trim()) {
        formGroup.classList.add('error');
        formGroup.classList.remove('success');
        message.textContent = 'This field is required';
        message.className = 'form-message error';
        isValid = false;
      } else {
        formGroup.classList.add('success');
        formGroup.classList.remove('error');
        message.textContent = 'Looks good!';
        message.className = 'form-message success';
      }
    });

    return isValid;
  }

  // Apply form validation
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
      if (!validateForm(this)) {
        e.preventDefault();
      } else {
        const submitBtn = this.querySelector('.btn-primary');
        if (submitBtn) showLoading(submitBtn);
      }
    });
  });

  // Product card hover effects
  document.querySelectorAll('.product-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-10px) rotate(1deg)';
    });

    card.addEventListener('mouseleave', function() {
      this.style.transform = '';
    });
  });

  // Search functionality
  const searchInput = document.querySelector('.search-bar input');
  const searchBtn = document.querySelector('.search-bar button');

  if (searchInput && searchBtn) {
    searchBtn.addEventListener('click', () => {
      const query = searchInput.value.trim();
      if (query) {
        window.location.href = `product-list.html?search=${encodeURIComponent(query)}`;
      }
    });

    searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        searchBtn.click();
      }
    });
  }
}

// PWA Registration
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(registration => {
        console.log('SW registered:', registration);

        // Check for updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              // New content available, show update prompt
              showUpdateNotification();
            }
          });
        });
      })
      .catch(error => console.log('SW registration failed:', error));
  });
}

// PWA Update Notification
function showUpdateNotification() {
  const updateDiv = document.createElement('div');
  updateDiv.className = 'update-notification';
  updateDiv.innerHTML = `
    <div class="update-content">
      <p>New version available! Refresh to update.</p>
      <button onclick="window.location.reload()">Refresh</button>
      <button onclick="this.parentElement.parentElement.remove()">Later</button>
    </div>
  `;
  document.body.appendChild(updateDiv);
}

// Install PWA prompt
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;

  // Show install button
  showInstallPrompt();
});

function showInstallPrompt() {
  const installDiv = document.createElement('div');
  installDiv.className = 'install-prompt';
  installDiv.innerHTML = `
    <div class="install-content">
      <p>Install Mens Kart for a better experience!</p>
      <button onclick="installPWA()">Install</button>
      <button onclick="this.parentElement.parentElement.remove()">Not now</button>
    </div>
  `;
  document.body.appendChild(installDiv);
}

function installPWA() {
  if (deferredPrompt) {
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('User accepted PWA install');
      }
      deferredPrompt = null;
    });
  }
  document.querySelector('.install-prompt').remove();
}

// Initialize animations when DOM is loaded
document.addEventListener('DOMContentLoaded', initAnimations);

function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

function addToCart(productId) {
  apiFetch('/cart', { method: 'POST', body: JSON.stringify({ productId, quantity: 1 }) }).then(response => {
    alert('Added to cart successfully!');
  }).catch(err => {
    console.error('Add to cart error:', err);
    alert('Failed to add item to cart. Please try again.');
  });
}

function filterProducts() {
  const category = document.getElementById('category-filter').value;
  const url = category ? `/products?category=${category}` : '/products';
  apiFetch(url).then(products => {
    const list = document.getElementById('product-list');
    list.innerHTML = '';
    products.forEach(p => {
      const div = document.createElement('div');
      div.className = 'product-card';
      div.innerHTML = `
        <div class="product-image">
          <img src="${p.image || 'https://via.placeholder.com/280x250/667eea/ffffff?text=' + encodeURIComponent(p.name)}" alt="${p.name}">
        </div>
        <div class="product-info">
          <div class="product-name">${p.name}</div>
          <div class="product-price">$${p.price}</div>
          <div class="product-rating">
            <span class="stars">★★★★☆</span>
            <span class="rating-count">(4.2)</span>
          </div>
          <button class="add-to-cart-btn" onclick="addToCart('${p._id}')">Add to Cart</button>
        </div>
      `;
      list.appendChild(div);
    });
  });
}

// Index page
if (window.location.pathname.includes('index.html') || window.location.pathname === '/') {
  // Load categories
  const categories = [
    { name: 'Shirts', icon: 'fas fa-tshirt', link: 'product-list.html?category=Shirts' },
    { name: 'Pants', icon: 'fas fa-socks', link: 'product-list.html?category=Pants' },
    { name: 'Jackets', icon: 'fas fa-vest', link: 'product-list.html?category=Jackets' },
    { name: 'Shoes', icon: 'fas fa-shoe-prints', link: 'product-list.html?category=Shoes' },
    { name: 'Accessories', icon: 'fas fa-glasses', link: 'product-list.html?category=Accessories' }
  ];

  const categoryList = document.getElementById('category-list');
  categories.forEach(cat => {
    const div = document.createElement('div');
    div.className = 'category-card';
    div.innerHTML = `
      <i class="${cat.icon}"></i>
      <h3>${cat.name}</h3>
      <a href="${cat.link}">Shop Now</a>
    `;
    categoryList.appendChild(div);
  });

  // Load featured products
  apiFetch('/products').then(products => {
    const list = document.getElementById('product-list');
    products.slice(0, 8).forEach(p => {
      const div = document.createElement('div');
      div.className = 'product-card';
      div.innerHTML = `
        <div class="product-image">
          <img src="${p.image || '/images/placeholder.jpg'}" alt="${p.name}" onerror="this.src='/images/placeholder.jpg'">
        </div>
        <div class="product-info">
          <div class="product-name">${p.name}</div>
          <div class="product-price">$${p.price}</div>
          <div class="product-rating">
            <span class="stars">★★★★☆</span>
            <span class="rating-count">(4.2)</span>
          </div>
          <button class="add-to-cart-btn" onclick="addToCart('${p._id}')">Add to Cart</button>
        </div>
      `;
      list.appendChild(div);
    });
  });
}

// Product list
if (window.location.pathname.includes('product-list.html')) {
  const category = getQueryParam('category');
  let url = '/products';
  if (category) {
    url += `?category=${category}`;
    document.getElementById('page-title').textContent = `${category}`;
    document.getElementById('category-filter').value = category;
  }

  apiFetch(url).then(products => {
    const list = document.getElementById('product-list');
    products.forEach(p => {
      const div = document.createElement('div');
      div.className = 'product-card';
      div.innerHTML = `
        <div class="product-image">
          <img src="${p.image || '/images/placeholder.jpg'}" alt="${p.name}" onerror="this.src='/images/placeholder.jpg'">
        </div>
        <div class="product-info">
          <div class="product-name">${p.name}</div>
          <div class="product-price">$${p.price}</div>
          <div class="product-rating">
            <span class="stars">★★★★☆</span>
            <span class="rating-count">(4.2)</span>
          </div>
          <button class="add-to-cart-btn" onclick="addToCart('${p._id}')">Add to Cart</button>
        </div>
      `;
      list.appendChild(div);
    });
  });
}

// Product details
if (window.location.pathname.includes('product-details.html')) {
  const id = getQueryParam('id');
  apiFetch(`/products/${id}`).then(product => {
    const container = document.querySelector('.product-detail');
    container.innerHTML = `
      <div class="product-images">
        <img src="${product.image || 'https://via.placeholder.com/500x500/667eea/ffffff?text=' + encodeURIComponent(product.name)}" alt="${product.name}" class="main-image" onerror="this.src='https://via.placeholder.com/500x500/667eea/ffffff?text=' + encodeURIComponent('${product.name}')">
        <div class="thumbnail-images">
          <img src="${product.image || 'https://via.placeholder.com/80x80/667eea/ffffff?text=' + encodeURIComponent(product.name)}" class="thumbnail" alt="Thumbnail 1" onerror="this.src='https://via.placeholder.com/80x80/667eea/ffffff?text=' + encodeURIComponent('${product.name}')">
          <img src="${product.image || 'https://via.placeholder.com/80x80/764ba2/ffffff?text=' + encodeURIComponent(product.name)}" class="thumbnail" alt="Thumbnail 2" onerror="this.src='https://via.placeholder.com/80x80/764ba2/ffffff?text=' + encodeURIComponent('${product.name}')">
        </div>
      </div>
      <div class="product-info">
        <h1>${product.name}</h1>
        <div class="product-price">$${product.price}</div>
        <div class="product-rating">
          <span class="stars">★★★★☆</span>
          <span class="rating-count">(4.2) • ${product.stock} left in stock</span>
        </div>
        <p class="product-description">${product.description}</p>
        <div class="size-selector">
          <label>Size:</label>
          <select>
            <option>S</option>
            <option>M</option>
            <option>L</option>
            <option>XL</option>
          </select>
        </div>
        <div class="quantity-selector">
          <label>Quantity:</label>
          <select id="quantity">
            <option>1</option>
            <option>2</option>
            <option>3</option>
            <option>4</option>
            <option>5</option>
          </select>
        </div>
        <button class="add-to-cart-detail" onclick="addToCart('${product._id}')">Add to Cart</button>
      </div>
    `;
  });
}

// Cart
if (window.location.pathname.includes('cart.html')) {
  function loadCart() {
    apiFetch('/cart').then(cart => {
      const items = document.getElementById('cart-items');
      const totalElement = document.getElementById('cart-total');
      items.innerHTML = '';
      let total = 0;

      if (cart && cart.items && cart.items.length > 0) {
        cart.items.forEach(item => {
          const div = document.createElement('div');
          div.className = 'cart-item';
          const itemTotal = item.productId.price * item.quantity;
          total += itemTotal;

          div.innerHTML = `
            <img src="${item.productId.image || '/images/placeholder.jpg'}" alt="${item.productId.name}" class="cart-item-image" onerror="this.src='/images/placeholder.jpg'">
            <div class="cart-item-details">
              <div class="cart-item-name">${item.productId.name}</div>
              <div class="cart-item-price">$${item.productId.price}</div>
              <div class="quantity-controls">
                <button class="quantity-btn" onclick="updateCart('${item.productId._id}', ${item.quantity - 1})">-</button>
                <input type="number" class="quantity-input" value="${item.quantity}" min="1" onchange="updateCart('${item.productId._id}', this.value)">
                <button class="quantity-btn" onclick="updateCart('${item.productId._id}', ${item.quantity + 1})">+</button>
              </div>
            </div>
            <button class="remove-btn" onclick="removeFromCart('${item.productId._id}')">Remove</button>
          `;
          items.appendChild(div);
        });
      } else {
        items.innerHTML = '<p>Your cart is empty</p>';
      }

      totalElement.textContent = total.toFixed(2);
    }).catch(err => {
      console.error('Cart load error:', err);
      document.getElementById('cart-items').innerHTML = '<p>Unable to load cart. Please try again.</p>';
    });
  }

  loadCart();
}

function updateCart(productId, quantity) {
  if (quantity <= 0) return removeFromCart(productId);
  apiFetch(`/cart/${productId}`, { method: 'PUT', body: JSON.stringify({ quantity: parseInt(quantity) }) }).then(() => {
    if (window.location.pathname.includes('cart.html')) loadCart();
  });
}

function removeFromCart(productId) {
  apiFetch(`/cart/${productId}`, { method: 'DELETE' }).then(() => {
    if (window.location.pathname.includes('cart.html')) loadCart();
  });
}

// Checkout Multi-Step Process
if (window.location.pathname.includes('checkout.html')) {
  let currentStep = 1;
  let checkoutData = {};

  // Check if user is logged in (optional - allow guest checkout for now)
  // Comment out strict login requirement for testing
  /*
  if (!token) {
    alert('Please login to proceed with checkout');
    window.location.href = 'login.html';
    return;
  }
  */

  function showStep(step) {
    // Hide all steps
    document.querySelectorAll('.checkout-step').forEach(stepEl => {
      stepEl.classList.remove('active');
    });

    // Show current step
    document.getElementById(`step-${step}`).classList.add('active');

    // Update progress
    document.querySelectorAll('.progress-step').forEach((progressEl, index) => {
      if (index + 1 <= step) {
        progressEl.classList.add('active');
      } else {
        progressEl.classList.remove('active');
      }
    });

    currentStep = step;
  }

  window.nextStep = function(fromStep) {
    if (fromStep === 1) {
      // Validate shipping form
      const fullName = document.getElementById('full-name').value.trim();
      const phone = document.getElementById('phone').value.trim();
      const street = document.getElementById('street').value.trim();
      const city = document.getElementById('city').value.trim();
      const state = document.getElementById('state').value.trim();
      const zip = document.getElementById('zip').value.trim();

      if (!fullName || !phone || !street || !city || !state || !zip) {
        alert('Please fill in all shipping details');
        return;
      }

      checkoutData.shipping = {
        fullName,
        phone,
        street,
        city,
        state,
        zip
      };

      console.log('Shipping data set:', checkoutData.shipping);
      showStep(2);
    } else if (fromStep === 2) {
      checkoutData.payment = 'cod';
      console.log('Payment method set:', checkoutData.payment);
      loadOrderReview();
      showStep(3);
    }
  };

  window.prevStep = function(fromStep) {
    showStep(fromStep - 1);
  };

  function loadOrderReview() {
    // Load cart items for review
    apiFetch('/cart').then(cart => {
      console.log('Cart data for review:', cart);

      const orderItems = document.getElementById('order-items');
      const shippingDisplay = document.getElementById('shipping-address-display');
      let total = 0;

      // Handle empty cart gracefully
      if (!cart || !cart.items || cart.items.length === 0) {
        orderItems.innerHTML = '<p style="text-align: center; padding: 20px;">Your cart is empty. Please add items before checkout.</p>';
        document.getElementById('subtotal').textContent = '$0.00';
        document.getElementById('final-total').textContent = '$0.00';
        return;
      }

      orderItems.innerHTML = '';
      cart.items.forEach(item => {
        const itemTotal = item.productId.price * item.quantity;
        total += itemTotal;

        const itemDiv = document.createElement('div');
        itemDiv.className = 'order-item';
        itemDiv.innerHTML = `
          <img src="${item.productId.image || 'https://via.placeholder.com/80x80/667eea/ffffff?text=' + encodeURIComponent(item.productId.name)}" alt="${item.productId.name}" onerror="this.src='https://via.placeholder.com/80x80/667eea/ffffff?text=' + encodeURIComponent('${item.productId.name}')">
          <div class="order-item-details">
            <h4>${item.productId.name}</h4>
            <p>Quantity: ${item.quantity} × $${item.productId.price}</p>
          </div>
          <div class="order-item-total">$${itemTotal.toFixed(2)}</div>
        `;
        orderItems.appendChild(itemDiv);
      });

      // Update totals
      document.getElementById('subtotal').textContent = `$${total.toFixed(2)}`;
      document.getElementById('final-total').textContent = `$${total.toFixed(2)}`;

      // Display shipping address
      if (checkoutData.shipping) {
        shippingDisplay.innerHTML = `
          <p><strong>${checkoutData.shipping.fullName}</strong></p>
          <p>${checkoutData.shipping.street}</p>
          <p>${checkoutData.shipping.city}, ${checkoutData.shipping.state} ${checkoutData.shipping.zip}</p>
          <p>Phone: ${checkoutData.shipping.phone}</p>
        `;
      }
    }).catch(err => {
      console.error('Error loading cart for review:', err);
      // Don't redirect on error, just show empty state
      const orderItems = document.getElementById('order-items');
      orderItems.innerHTML = '<p style="text-align: center; padding: 20px; color: red;">Error loading cart. Please refresh the page.</p>';
    });
  }

  // Place order
  document.getElementById('place-order-btn').addEventListener('click', async () => {
    const placeOrderBtn = document.getElementById('place-order-btn');
    const originalText = placeOrderBtn.innerHTML;
    placeOrderBtn.innerHTML = '<div class="loading"></div> Placing Order...';
    placeOrderBtn.disabled = true;

    try {
      console.log('Placing order with data:', checkoutData);

      // Validate all required data
      if (!checkoutData.shipping) {
        throw new Error('Please complete all shipping information steps');
      }

      if (!checkoutData.payment) {
        throw new Error('Please select a payment method');
      }

      // Check if cart has items
      const cartResponse = await apiFetch('/cart');
      console.log('Cart response:', cartResponse);

      if (!cartResponse || !cartResponse.items || cartResponse.items.length === 0) {
        throw new Error('Your cart is empty. Please add items before checkout.');
      }

      console.log('Cart has items, proceeding with order...');

      const orderData = {
        address: {
          fullName: checkoutData.shipping.fullName,
          phone: checkoutData.shipping.phone,
          street: checkoutData.shipping.street,
          city: checkoutData.shipping.city,
          state: checkoutData.shipping.state,
          zip: checkoutData.shipping.zip
        },
        paymentMethod: checkoutData.payment
      };

      console.log('Sending order data:', orderData);

      const response = await apiFetch('/orders', {
        method: 'POST',
        body: JSON.stringify(orderData)
      });

      console.log('Order response:', response);

      if (response && response._id) {
        // Store order ID for confirmation
        localStorage.setItem('lastOrderId', response._id);

        // Clear cart after successful order (individual items)
        try {
          // Get cart items and remove them one by one
          if (cartResponse.items && cartResponse.items.length > 0) {
            for (const item of cartResponse.items) {
              await apiFetch(`/cart/${item.productId._id}`, { method: 'DELETE' });
            }
          }
        } catch (cartError) {
          console.log('Cart clearing failed, but order was successful');
        }

        // Show success message with order details
        const orderId = response._id.slice(-6).toUpperCase();
        const total = response.total ? `$${response.total.toFixed(2)}` : 'N/A';

        alert(`🎉 Order placed successfully!\n\nOrder ID: #${orderId}\nTotal Amount: ${total}\n\nYou will receive a confirmation email shortly.`);

        // Redirect to orders page
        window.location.href = 'orders.html?confirmation=true';
      } else if (response && response.message) {
        throw new Error(response.message);
      } else if (response && typeof response === 'string') {
        throw new Error(response);
      } else {
        throw new Error('Invalid response from server. Please try again.');
      }
    } catch (error) {
      console.error('Order placement error:', error);

      // Provide user-friendly error messages
      let errorMessage = 'Failed to place order. ';
      if (error.message.includes('cart is empty')) {
        errorMessage += 'Your cart appears to be empty. Please add items and try again.';
      } else if (error.message.includes('login')) {
        errorMessage += 'Please login to place an order.';
      } else if (error.message.includes('shipping')) {
        errorMessage += 'Please complete your shipping information.';
      } else if (error.message.includes('payment')) {
        errorMessage += 'Please select a payment method.';
      } else {
        errorMessage += error.message || 'Please try again or contact support.';
      }

      alert(errorMessage);

      // Reset button
      placeOrderBtn.innerHTML = originalText;
      placeOrderBtn.disabled = false;
    }
  });

  // Initialize first step
  showStep(1);
}

// Login
if (window.location.pathname.includes('login.html')) {
  document.getElementById('login-form').addEventListener('submit', e => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Show loading state
    const submitBtn = document.querySelector('.btn-primary');
    const originalText = submitBtn.textContent;
    submitBtn.innerHTML = '<div class="loading"></div> Signing in...';
    submitBtn.disabled = true;

    apiFetch('/users/login', { method: 'POST', body: JSON.stringify({ email, password }) }).then(data => {
      if (data.token) {
        // Store user data in localStorage
        localStorage.setItem('token', data.token);
        if (data.user) {
          localStorage.setItem('userId', data.user.userId);
          localStorage.setItem('userName', data.user.name);
          localStorage.setItem('userEmail', data.user.email);
        }

        // Simple success message
        alert(`Welcome back! User ID: ${data.user?.userId || 'N/A'}`);
        window.location.href = 'index.html';
      } else {
        throw new Error('Login failed');
      }
    }).catch(err => {
      console.error('Login error:', err);
      alert('Login failed. Please check your credentials and try again.');
      // Reset button
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    });
  });
}

// Register
if (window.location.pathname.includes('register.html')) {
  document.getElementById('register-form').addEventListener('submit', e => {
    e.preventDefault();
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    console.log('Registration attempt:', { name, email, hasPassword: !!password });

    // Basic client-side validation
    if (!name || !email || !password) {
      alert('Please fill in all fields');
      return;
    }

    if (password.length < 6) {
      alert('Password must be at least 6 characters long');
      return;
    }

    // Show loading state
    const submitBtn = document.querySelector('.btn-primary');
    const originalText = submitBtn.textContent;
    submitBtn.innerHTML = '<div class="loading"></div> Creating Account...';
    submitBtn.disabled = true;

    apiFetch('/users/register', {
      method: 'POST',
      body: JSON.stringify({ name, email, password })
    }).then(response => {
      if (response.message && response.message.includes('registered')) {
        // Success - show user ID
        const userId = response.userId || response.user?.userId || 'Will be assigned after login';
        alert(`Account created successfully! User ID: ${userId}`);
        window.location.href = 'login.html';
      } else {
        throw new Error(response.message || 'Registration failed');
      }
    }).catch(err => {
      console.error('Registration error:', err);

      // Provide specific error messages
      let errorMessage = 'Registration failed. Please try again.';
      if (err.message) {
        if (err.message.includes('already exists')) {
          errorMessage = 'An account with this email already exists. Please use a different email or try logging in.';
        } else if (err.message.includes('required')) {
          errorMessage = 'Please fill in all required fields.';
        } else if (err.message.includes('Password')) {
          errorMessage = 'Password must be at least 6 characters long.';
        } else {
          errorMessage = err.message;
        }
      }

      alert(errorMessage);
      // Reset button
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    });
  });
}

// Profile
if (window.location.pathname.includes('profile.html')) {
  let currentUser = null;

  function loadProfile() {
    apiFetch('/users/profile').then(user => {
      currentUser = user;
      console.log('Loaded user profile:', user); // Debug log
  
      // Update display info
      document.getElementById('display-name').textContent = user.name || 'Not provided';
      document.getElementById('display-email').textContent = user.email;
      document.getElementById('display-phone').textContent = user.phone || 'Not provided';
      document.getElementById('display-userid').textContent = user.userId || 'Not assigned';
  
      // Update form fields
      document.getElementById('name').value = user.name || '';
      document.getElementById('email').value = user.email;
      document.getElementById('phone').value = user.phone || '';
      document.getElementById('userid').value = user.userId || '';
  
      // Update localStorage with latest data
      if (user.userId) localStorage.setItem('userId', user.userId);
      if (user.name) localStorage.setItem('userName', user.name);
      if (user.email) localStorage.setItem('userEmail', user.email);
  
      // Update profile image
      if (user.profileImage) {
        document.getElementById('profile-image').src = user.profileImage;
      } else {
        // Check for locally stored profile image
        const localImage = localStorage.getItem('profileImage');
        if (localImage) {
          document.getElementById('profile-image').src = localImage;
        }
      }
  
      // Load stats
      loadProfileStats(user);
    }).catch(err => {
      console.log('Profile load error:', err);
      // Try to show cached user info if available
      const cachedUserId = localStorage.getItem('userId');
      const cachedName = localStorage.getItem('userName');
      const cachedEmail = localStorage.getItem('userEmail');
  
      if (cachedUserId) {
        document.getElementById('display-name').textContent = cachedName || 'Not provided';
        document.getElementById('display-email').textContent = cachedEmail || 'Not provided';
        document.getElementById('display-phone').textContent = 'Not provided';
        document.getElementById('display-userid').textContent = cachedUserId;
  
        // Show limited profile for offline/cached view
        document.querySelector('.profile-main').innerHTML = `
          <div class="profile-section">
            <div class="section-header">
              <h3>Limited Profile View</h3>
            </div>
            <div class="profile-info">
              <div class="info-group">
                <label>User ID</label>
                <p>${cachedUserId}</p>
              </div>
              <div class="info-group">
                <label>Name</label>
                <p>${cachedName || 'Not available'}</p>
              </div>
              <div class="info-group">
                <label>Email</label>
                <p>${cachedEmail || 'Not available'}</p>
              </div>
            </div>
            <div style="text-align: center; margin-top: 20px;">
              <button class="btn-primary" onclick="window.location.href='login.html'">Login to View Full Profile</button>
            </div>
          </div>
        `;
      } else {
        alert('Please login to view your profile');
        window.location = 'login.html';
      }
    });
  }

  function loadProfileStats(user) {
    // Load orders for stats
    apiFetch('/orders').then(orders => {
      const totalOrders = orders.length;
      const totalSpent = orders.reduce((sum, order) => sum + order.total, 0);
      const memberSince = new Date(user.createdAt).getFullYear();

      document.getElementById('total-orders').textContent = totalOrders;
      document.getElementById('total-spent').textContent = `$${totalSpent.toFixed(2)}`;
      document.getElementById('member-since').textContent = memberSince;

      // Show recent orders
      if (orders.length > 0) {
        const recentOrders = orders.slice(0, 3);
        const recentOrdersDiv = document.getElementById('recent-orders');
        recentOrdersDiv.innerHTML = recentOrders.map(order => `
          <div class="recent-order-item">
            <div class="order-number">#${order._id.slice(-6).toUpperCase()}</div>
            <div class="order-date">${new Date(order.createdAt).toLocaleDateString()}</div>
            <div class="order-amount">$${order.total.toFixed(2)}</div>
            <div class="order-status status-${order.status.toLowerCase()}">${order.status}</div>
          </div>
        `).join('');
      }
    });
  }

  // Edit profile functionality
  document.getElementById('edit-profile-btn').addEventListener('click', () => {
    document.getElementById('profile-info').style.display = 'none';
    document.getElementById('update-profile-form').style.display = 'block';
    document.getElementById('edit-profile-btn').style.display = 'none';
  });

  document.getElementById('cancel-edit-btn').addEventListener('click', () => {
    document.getElementById('profile-info').style.display = 'block';
    document.getElementById('update-profile-form').style.display = 'none';
    document.getElementById('edit-profile-btn').style.display = 'inline-block';
    // Reset form values
    loadProfile();
  });

  document.getElementById('update-profile-form').addEventListener('submit', e => {
    e.preventDefault();
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();

    // Show loading state
    const submitBtn = document.querySelector('#update-profile-form .btn-primary');
    const originalText = submitBtn.textContent;
    submitBtn.innerHTML = '<div class="loading"></div> Updating...';
    submitBtn.disabled = true;

    apiFetch('/users/profile', {
      method: 'PUT',
      body: JSON.stringify({ name, email, phone })
    }).then(response => {
      if (response.user) {
        // Update current user data with response
        currentUser = response.user;

        // Update display info immediately with returned data
        document.getElementById('display-name').textContent = response.user.name || 'Not provided';
        document.getElementById('display-email').textContent = response.user.email;
        document.getElementById('display-phone').textContent = response.user.phone || 'Not provided';
        document.getElementById('display-userid').textContent = response.user.userId || localStorage.getItem('userId') || 'Not assigned';

        // Update localStorage with latest data
        localStorage.setItem('userName', response.user.name);
        localStorage.setItem('userEmail', response.user.email);

        // Simple success alert
        alert('Profile updated successfully!');

        // Switch back to view mode
        document.getElementById('profile-info').style.display = 'block';
        document.getElementById('update-profile-form').style.display = 'none';
        document.getElementById('edit-profile-btn').style.display = 'inline-block';
      } else {
        throw new Error('Invalid response');
      }
    }).catch(err => {
      console.error('Profile update error:', err);
      alert('Failed to update profile. Please try again.');
    }).finally(() => {
      // Reset button state
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    });
  });

  // Profile image upload
  document.getElementById('avatar-input').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function(e) {
        const imageData = e.target.result;
        document.getElementById('profile-image').src = imageData;

        // Here you would typically upload to server
        // For now, we'll just store in localStorage as demo
        localStorage.setItem('profileImage', imageData);
        alert('Profile image updated! (Note: This is stored locally for demo purposes)');
      };
      reader.readAsDataURL(file);
    }
  });

  // Load profile on page load
  loadProfile();
}

function changePassword() {
  alert('Password change feature coming soon!');
}

function logout() {
  // Clear all user-related data
  localStorage.removeItem('token');
  localStorage.removeItem('profileImage');
  localStorage.removeItem('userId');
  localStorage.removeItem('userName');
  localStorage.removeItem('userEmail');
  localStorage.removeItem('lastOrderId');

  // Simple logout message
  alert('You have been logged out successfully.');
  window.location.href = 'index.html';
}

// Orders
if (window.location.pathname.includes('orders.html')) {
  // Check for order confirmation
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('confirmation') === 'true') {
    const orderId = localStorage.getItem('lastOrderId');
    if (orderId) {
      document.getElementById('confirmation-order-id').textContent = `#${orderId.slice(-6).toUpperCase()}`;
      document.getElementById('order-confirmation').style.display = 'flex';

      // Auto redirect after 5 seconds
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 5000);
    }
  }

  // Load user orders
  apiFetch('/orders').then(orders => {
    const ordersList = document.getElementById('orders-list');
    const emptyOrders = document.getElementById('empty-orders');

    if (orders && orders.length > 0) {
      emptyOrders.style.display = 'none';
      ordersList.innerHTML = '';

      orders.forEach(order => {
        const orderDiv = document.createElement('div');
        orderDiv.className = 'order-card';
        const orderDate = new Date(order.createdAt).toLocaleDateString();

        orderDiv.innerHTML = `
          <div class="order-header">
            <div class="order-info">
              <h3>Order #${order._id.slice(-6).toUpperCase()}</h3>
              <p>Placed on ${orderDate}</p>
            </div>
            <div class="order-status status-${order.status.toLowerCase()}">
              ${order.status.charAt(0).toUpperCase() + order.status.slice(1)}
            </div>
          </div>
          <div class="order-items">
            ${order.items.map(item => `
              <div class="order-item-summary">
                <img src="${item.productId?.image || 'https://via.placeholder.com/60x60/667eea/ffffff?text=' + encodeURIComponent(item.productId?.name || 'Product')}" alt="${item.productId?.name || 'Product'}" onerror="this.src='https://via.placeholder.com/60x60/667eea/ffffff?text=' + encodeURIComponent('${item.productId?.name || 'Product'}')">
                <div class="item-details">
                  <h4>${item.productId?.name || 'Product'}</h4>
                  <p>Qty: ${item.quantity} × $${item.price}</p>
                </div>
              </div>
            `).join('')}
          </div>
          <div class="order-footer">
            <div class="order-total">Total: $${order.total.toFixed(2)}</div>
            <div class="order-actions">
              <button class="btn-outline" onclick="viewOrderDetails('${order._id}')">View Details</button>
            </div>
          </div>
        `;
        ordersList.appendChild(orderDiv);
      });
    } else {
      emptyOrders.style.display = 'block';
    }
  }).catch(err => {
    console.log('Orders load error:', err);
    document.getElementById('empty-orders').style.display = 'block';
  });
}

function continueShopping() {
  window.location.href = 'index.html';
}

function viewOrders() {
  document.getElementById('order-confirmation').style.display = 'none';
  // Page will reload and show orders
  window.location.href = 'orders.html';
}

function viewOrderDetails(orderId) {
  // Could implement modal or redirect to detailed view
  alert('Order details feature coming soon!');
}