const express = require('express');
const Order = require('../models/Order');
const Cart = require('../models/Cart');
const auth = require('../middleware/auth');
const admin = require('../middleware/admin');

const router = express.Router();

// Create order
router.post('/', async (req, res) => {
  try {
    // For testing, use a fixed user ID or get from token if available
    const token = req.header('Authorization')?.replace('Bearer ', '');
    let userId = null;

    if (token) {
      try {
        const jwt = require('jsonwebtoken');
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        userId = decoded.id;
      } catch (err) {
        // Token invalid, use demo user
        userId = '507f1f77bcf86cd799439011'; // Demo user ID
      }
    } else {
      // No token, use demo user for testing
      userId = '507f1f77bcf86cd799439011'; // Demo user ID
    }

    const cart = await Cart.findOne({ userId }).populate('items.productId');
    if (!cart || cart.items.length === 0) return res.status(400).json({ message: 'Cart is empty' });

    // Filter out items with invalid product references
    const validItems = cart.items.filter(item => item.productId && item.productId._id);

    if (validItems.length === 0) return res.status(400).json({ message: 'No valid items in cart' });

    const items = validItems.map(item => ({
      productId: item.productId._id,
      quantity: item.quantity,
      price: item.productId.price,
    }));

    const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

    const order = new Order({
      userId,
      items,
      total,
      address: req.body.address,
      paymentMethod: req.body.paymentMethod || 'cod'
    });

    await order.save();

    // Clear cart
    cart.items = [];
    await cart.save();

    res.status(201).json(order);
  } catch (err) {
    console.error('Order creation error:', err);
    res.status(500).json({ message: err.message });
  }
});

// Get user orders
router.get('/', auth, async (req, res) => {
  try {
    const orders = await Order.find({ userId: req.user.id }).populate('items.productId');
    res.json(orders);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Get single order
router.get('/:id', auth, async (req, res) => {
  try {
    const order = await Order.findById(req.params.id).populate('items.productId');
    if (order.userId.toString() !== req.user.id && req.user.role !== 'admin') {
      return res.status(403).json({ message: 'Not authorized' });
    }
    res.json(order);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Update order (admin)
router.put('/:id', auth, admin, async (req, res) => {
  try {
    const order = await Order.findByIdAndUpdate(req.params.id, req.body, { new: true });
    res.json(order);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

module.exports = router;