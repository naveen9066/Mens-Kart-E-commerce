const mongoose = require('mongoose');

const orderSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  items: [{
    productId: { type: mongoose.Schema.Types.ObjectId, ref: 'Product', required: true },
    quantity: Number,
    price: Number,
  }],
  total: Number,
  status: { type: String, default: 'pending' }, // pending, shipped, delivered
  address: {
    street: String,
    city: String,
    zip: String,
  },
}, { timestamps: true });

module.exports = mongoose.model('Order', orderSchema);