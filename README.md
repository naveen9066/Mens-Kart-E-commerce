# 🛍️ **Mens Kart** - Men's Fashion E-commerce Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-7+-blue.svg)](https://www.mongodb.com/)
[![PWA](https://img.shields.io/badge/PWA-Ready-orange.svg)](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)

A modern, responsive e-commerce platform built for men's fashion with PWA capabilities and APK conversion support.

![Mens Kart Preview](./frontend/images/preview.png)

## ✨ **Features**

### 🛒 **Core E-commerce Features**
- **Product Catalog** - Browse men's fashion items with categories
- **Shopping Cart** - Add, update, remove items with persistence
- **User Authentication** - Secure login/registration system
- **Order Management** - Complete order placement and tracking
- **Search & Filters** - Find products by category and search terms
- **Responsive Design** - Optimized for mobile, tablet, and desktop

### 📱 **Progressive Web App (PWA)**
- **Installable** - Add to home screen like native apps
- **Offline Support** - Works without internet connection
- **Push Notifications** - Order updates and promotions
- **Fast Loading** - Cached resources for instant access
- **App-like Experience** - Smooth animations and interactions

### 🔧 **Technical Features**
- **RESTful APIs** - Well-documented backend endpoints
- **JWT Authentication** - Secure token-based auth
- **MongoDB Integration** - NoSQL database for scalability
- **Modern UI/UX** - Inspired by Myntra's design language
- **Cross-platform** - Web + Mobile (APK) support

## 🚀 **Tech Stack**

### **Frontend**
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with animations
- **JavaScript (ES6+)** - Interactive functionality
- **PWA** - Service workers, manifest, offline support

### **Backend**
- **Node.js** - Runtime environment
- **Express.js** - Web framework
- **MongoDB** - NoSQL database
- **Mongoose** - ODM for MongoDB
- **JWT** - Authentication tokens
- **bcrypt** - Password hashing

### **Mobile/App**
- **PWA to APK** - Multiple conversion methods
- **Cordova/PhoneGap** - Hybrid app framework
- **Capacitor** - Modern native runtime

## 📁 **Project Structure**

```
mens-kart/
├── backend/                    # Node.js backend
│   ├── models/                # MongoDB schemas
│   │   ├── User.js
│   │   ├── Product.js
│   │   ├── Cart.js
│   │   └── Order.js
│   ├── routes/                # API endpoints
│   │   ├── userRoutes.js
│   │   ├── productRoutes.js
│   │   ├── cartRoutes.js
│   │   └── orderRoutes.js
│   ├── middleware/            # Auth & admin middleware
│   ├── server.js              # Main server file
│   ├── seed.js                # Database seeding
│   └── package.json
├── frontend/                  # Static web files
│   ├── index.html            # Homepage
│   ├── product-list.html     # Product catalog
│   ├── product-details.html  # Product details
│   ├── cart.html             # Shopping cart
│   ├── checkout.html         # Order checkout
│   ├── login.html            # User login
│   ├── register.html         # User registration
│   ├── profile.html          # User profile
│   ├── orders.html           # Order history
│   ├── style.css             # Global styles
│   ├── script.js             # Frontend logic
│   ├── manifest.json         # PWA manifest
│   └── sw.js                 # Service worker
├── config.xml                # Cordova configuration
├── APK_BUILD_GUIDE.md        # APK conversion guide
└── README.md                 # This file
```



### **Quick Start**

1. **Clone the repository**
   ```bash
   git clone https://github.com/naveen9066/MensKart.git
   cd MensKart
   ```

2. **Setup Backend**
   ```bash
   cd backend
   npm install
   npm run seed  # Seed database with sample data
   ```

3. **Configure Environment**
   ```bash
   # Edit backend/.env
   MONGO_URI=mongodb://localhost:27017/mens-kart
   JWT_SECRET=your_super_secret_jwt_key_here
   PORT=5000
   ```

4. **Start Development Server**
   ```bash
   # Backend (from backend/ directory)
   npm run dev

   # Frontend served automatically at http://localhost:5000
   ```

5. **Access the Application**
   - Open [http://localhost:5000](http://localhost:5000) in your browser
   - Register a new account or login with admin credentials


### **Method 1: PWA Builder (Easiest)**
```bash
# Install PWA Builder
npm install -g pwa-builder

# Build APK
pwa-builder http://localhost:5000

# Download generated APK
```

### **Method 2: Apache Cordova**
```bash
# Install Cordova
npm install -g cordova

# Create Cordova project
cordova create mens-kart-cordova com.menskart.app "Mens Kart"
cd mens-kart-cordova

# Copy web files
cp -r ../frontend/* www/
cp ../config.xml .

# Build APK
cordova platform add android
cordova build android
```

### **Method 3: Online Tools**
- [PWABuilder.com](https://www.pwabuilder.com) - Enter your URL
- [PWA2APK.com](https://www.pwa2apk.com) - Upload PWA
- [Web2Apk.com](https://web2apk.com) - Instant conversion

For detailed instructions, see [APK_BUILD_GUIDE.md](./APK_BUILD_GUIDE.md)

## 📚 **API Documentation**

### **Base URL:** `http://localhost:5000/api`

### **Authentication**
All protected routes require JWT token in header:
```
Authorization: Bearer <your_jwt_token>
```

### **User APIs**
```
POST   /api/users/register     # User registration
POST   /api/users/login        # User login
GET    /api/users/profile      # Get user profile
PUT    /api/users/profile      # Update user profile
```

### **Product APIs**
```
GET    /api/products           # Get all products
GET    /api/products/:id       # Get single product
POST   /api/products           # Create product (admin)
PUT    /api/products/:id       # Update product (admin)
DELETE /api/products/:id       # Delete product (admin)
```

### **Cart APIs**
```
GET    /api/cart                # Get user cart
POST   /api/cart                # Add item to cart
PUT    /api/cart/:productId     # Update cart item
DELETE /api/cart/:productId     # Remove cart item
```

### **Order APIs**
```
POST   /api/orders              # Create order
GET    /api/orders              # Get user orders
GET    /api/orders/:id          # Get single order
PUT    /api/orders/:id          # Update order (admin)
```

### **Sample API Usage**

```javascript
// Login
const response = await fetch('/api/users/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});

const { token } = await response.json();

// Use token for authenticated requests
const products = await fetch('/api/products', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

## 🎨 **Customization**

### **Styling**
- Edit `frontend/style.css` for global styles
- CSS variables defined in `:root` for easy theming
- Responsive breakpoints: 480px, 768px, 1024px, 1400px

### **Branding**
- Update colors in CSS variables
- Replace logo in header
- Modify app name in `manifest.json`
- Update icons in `frontend/images/`

### **Features**
- Add new pages in `frontend/`
- Create new API endpoints in `backend/routes/`
- Extend MongoDB models in `backend/models/`

## 🧪 **Testing**

### **Manual Testing**
1. **User Registration/Login** - Test authentication flow
2. **Product Browsing** - Navigate categories and products
3. **Shopping Cart** - Add/remove items, quantity updates
4. **Checkout Process** - Complete order placement
5. **Order History** - View past orders
6. **Responsive Design** - Test on different screen sizes

### **API Testing**
```bash
# Test user registration
curl -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"password123"}'

# Test product listing
curl http://localhost:5000/api/products
```

### **PWA Testing**
- Use Chrome DevTools → Application → Service Workers
- Test offline functionality
- Check installability with Lighthouse

## 🚀 **Deployment**

### **Web Deployment**
```bash
# Build for production
cd backend
npm run build

# Deploy to platforms like:
# - Heroku
# - DigitalOcean
# - AWS EC2
# - Vercel/Netlify (frontend only)
```

### **Environment Variables**
```env
NODE_ENV=production
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/mens-kart
JWT_SECRET=your_production_jwt_secret
PORT=5000
```

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgements**

- **Myntra** - Inspiration for UI/UX design
- **PWA Builder** - APK conversion tools
- **Font Awesome** - Icons library
- **MongoDB** - Database platform


**Made with ❤️ for men's fashion enthusiasts**

**⭐ Star this repo if you find it helpful!**
