const express = require('express');
const mongoose = require('mongoose');
const Cart = require('../models/Cart');
const auth = require('../middleware/auth');

const router = express.Router();

// Get cart
router.get('/', async (req, res) => {
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

    let cart = await Cart.findOne({ userId }).populate('items.productId');
    if (!cart) cart = { items: [] };

    res.json(cart);
  } catch (err) {
    console.error('Cart GET error:', err);
    res.status(500).json({ message: err.message });
  }
});

// Add to cart
router.post('/', async (req, res) => {
  try {
    const { productId, quantity } = req.body;

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

    let cart = await Cart.findOne({ userId });
    if (!cart) {
      cart = new Cart({ userId, items: [] });
    }

    const itemIndex = cart.items.findIndex(item => item.productId.toString() === productId);
    if (itemIndex > -1) {
      cart.items[itemIndex].quantity += quantity;
    } else {
      cart.items.push({ productId: new mongoose.Types.ObjectId(productId), quantity });
    }

    await cart.save();
    res.json(cart);
  } catch (err) {
    console.error('Cart POST error:', err);
    res.status(500).json({ message: err.message });
  }
});

// Update cart item
router.put('/:productId', async (req, res) => {
  try {
    const { quantity } = req.body;

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

    const cart = await Cart.findOne({ userId });
    if (cart) {
      const item = cart.items.find(item => item.productId.toString() === req.params.productId);
      if (item) item.quantity = quantity;
      await cart.save();
    }
    res.json(cart || { items: [] });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Delete cart item
router.delete('/:productId', async (req, res) => {
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

    const cart = await Cart.findOne({ userId });
    if (cart) {
      cart.items = cart.items.filter(item => item.productId.toString() !== req.params.productId);
      await cart.save();
    }
    res.json(cart || { items: [] });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

module.exports = router;