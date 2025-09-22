require('dotenv').config();
const mongoose = require('mongoose');

// Connect to MongoDB
async function connectAndView() {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    console.log('Connected to MongoDB');

    console.log('\n=== MENS KART DATABASE CONTENTS ===\n');

    // View Users
    console.log('👥 USERS:');
    const users = await mongoose.connection.db.collection('users').find({}).toArray();
    if (users.length === 0) {
      console.log('   No users found');
    } else {
      users.forEach((user, index) => {
        console.log(`${index + 1}. ${user.name} (${user.email}) - Role: ${user.role}`);
        console.log(`   ID: ${user._id}, Created: ${user.createdAt}`);
      });
    }

    // View Products
    console.log('\n🛍️  PRODUCTS:');
    const products = await mongoose.connection.db.collection('products').find({}).toArray();
    if (products.length === 0) {
      console.log('   No products found');
    } else {
      products.forEach((product, index) => {
        console.log(`${index + 1}. ${product.name} - $${product.price}`);
        console.log(`   Category: ${product.category}, Stock: ${product.stock}`);
        console.log(`   ID: ${product._id}`);
      });
    }

    // View Carts
    console.log('\n🛒 CARTS:');
    const carts = await mongoose.connection.db.collection('carts').find({}).toArray();
    if (carts.length === 0) {
      console.log('   No carts found');
    } else {
      carts.forEach((cart, index) => {
        console.log(`${index + 1}. User ID: ${cart.userId}`);
        console.log(`   Items: ${cart.items.length}`);
        cart.items.forEach((item, itemIndex) => {
          console.log(`     ${itemIndex + 1}. Product ID: ${item.productId}, Quantity: ${item.quantity}`);
        });
        console.log(`   Created: ${cart.createdAt}`);
      });
    }

    // View Orders
    console.log('\n📦 ORDERS:');
    const orders = await mongoose.connection.db.collection('orders').find({}).toArray();
    if (orders.length === 0) {
      console.log('   No orders found');
    } else {
      orders.forEach((order, index) => {
        console.log(`${index + 1}. Order ID: ${order._id}`);
        console.log(`   User ID: ${order.userId}, Status: ${order.status}`);
        console.log(`   Total: $${order.total}, Items: ${order.items.length}`);
        console.log(`   Created: ${order.createdAt}`);
      });
    }

    console.log('\n=== END OF DATABASE VIEW ===\n');

  } catch (error) {
    console.error('Error viewing database:', error);
  } finally {
    await mongoose.connection.close();
    console.log('Database connection closed');
  }
}

// Run the view function
connectAndView();