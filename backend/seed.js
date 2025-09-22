require('dotenv').config();
const mongoose = require('mongoose');
const Product = require('./models/Product');
const Cart = require('./models/Cart');
const User = require('./models/User');
const bcrypt = require('bcryptjs');

mongoose.connect(process.env.MONGO_URI);

const seed = async () => {
  try {
    // Ensure all existing users have userIds
    const usersWithoutIds = await User.find({ userId: { $exists: false } });
    for (let user of usersWithoutIds) {
      await user.ensureUserId();
    }
    console.log(`Updated ${usersWithoutIds.length} users with userIds`);

    // Create admin user if doesn't exist
    const existingAdmin = await User.findOne({ email: 'admin@menskart.com' });
    if (!existingAdmin) {
      const hashedPassword = await bcrypt.hash('admin123', 10);
      const admin = await User.create({ name: 'Admin', email: 'admin@menskart.com', password: hashedPassword, role: 'admin' });
      console.log(`Created admin user with ID: ${admin.userId}`);
    }

    // Clear existing products and carts, then add fresh ones
    await Product.deleteMany({});
    await Cart.deleteMany({});
    console.log('Cleared existing products and carts');

    const products = [
      { name: 'Cotton Shirt', description: 'Comfortable cotton shirt', price: 25, category: 'Shirts', stock: 20, image: '/images/products/Formal-shirt.jpg' },
      { name: 'T-Shirt', description: 'Casual t-shirt', price: 15, category: 'Shirts', stock: 30, image: '/images/products/t-shirt.png' },
      { name: 'Denim Jeans', description: 'Classic denim jeans', price: 50, category: 'Pants', stock: 15, image: '/images/products/pant.jpg' },
      { name: 'Leather Jacket', description: 'Stylish leather jacket', price: 100, category: 'Jackets', stock: 10, image: '/images/products/denim-jacket.jpg' },
      { name: 'Sneakers', description: 'Comfortable sneakers', price: 40, category: 'Shoes', stock: 25, image: '/images/products/shoes.jpg' },
      { name: 'Leather Belt', description: 'Elegant leather belt', price: 75, category: 'Accessories', stock: 12, image: '/images/products/belt.jpg' },
      { name: 'Sunglasses', description: 'UV protection sunglasses', price: 30, category: 'Accessories', stock: 18, image: '/images/products/sun-glass.jpg' },
    ];
    await Product.insertMany(products);
    console.log('Fresh sample products added');

    console.log('Database seeding completed successfully');
  } catch (error) {
    console.error('Seeding error:', error);
  } finally {
    process.exit();
  }
};

seed();