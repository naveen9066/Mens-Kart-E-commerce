const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  userId: { type: String, unique: true }, // Auto-generated unique user ID
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  phone: { type: String },
  profileImage: { type: String, default: '' },
  role: { type: String, default: 'user' }, // user or admin
}, { timestamps: true });

// Auto-generate userId before saving
userSchema.pre('save', async function(next) {
  if (!this.userId) {
    try {
      // Generate unique user ID like MK001, MK002, etc.
      let count = await mongoose.model('User').countDocuments();
      let userId;
      let attempts = 0;
      const maxAttempts = 10;

      do {
        userId = `MK${String(count + 1).padStart(3, '0')}`;
        const existingUser = await mongoose.model('User').findOne({ userId });
        if (!existingUser) {
          break; // userId is unique
        }
        count++;
        attempts++;
      } while (attempts < maxAttempts);

      if (attempts >= maxAttempts) {
        // Fallback to timestamp-based ID if we can't find a unique sequential ID
        userId = `MK${Date.now().toString().slice(-6)}`;
      }

      this.userId = userId;
    } catch (error) {
      console.error('Error generating userId:', error);
      // Fallback to timestamp-based ID
      this.userId = `MK${Date.now().toString().slice(-6)}`;
    }
  }
  next();
});

// Ensure userId is generated for existing users
userSchema.methods.ensureUserId = async function() {
  if (!this.userId) {
    const count = await mongoose.model('User').countDocuments();
    this.userId = `MK${String(count + 1).padStart(3, '0')}`;
    await this.save();
  }
  return this.userId;
};

module.exports = mongoose.model('User', userSchema);