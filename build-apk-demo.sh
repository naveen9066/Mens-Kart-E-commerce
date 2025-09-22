#!/bin/bash

# Mens Kart APK Build Demo Script
# This script demonstrates different methods to build APK from web app

echo "🚀 Mens Kart APK Build Demo"
echo "============================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[METHOD $1]${NC} $2"
}

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm first."
    exit 1
fi

print_status "Node.js version: $(node --version)"
print_status "npm version: $(npm --version)"

echo ""
print_header "1" "Progressive Web App (PWA) Method - RECOMMENDED"
echo "This method converts your existing PWA to APK"
echo ""

# Method 1: PWA Builder
print_status "Installing PWA Builder globally..."
npm install -g pwa-builder

if [ $? -eq 0 ]; then
    print_status "PWA Builder installed successfully!"
    echo ""
    echo "To build APK with PWA Builder:"
    echo "1. Run: pwa-builder https://your-domain.com"
    echo "2. Follow the prompts to generate APK"
    echo "3. Download the generated APK file"
    echo ""
else
    print_error "Failed to install PWA Builder"
fi

# Method 2: Cordova/PhoneGap
echo ""
print_header "2" "Apache Cordova Method"
echo "This method wraps your web app in a native Android container"
echo ""

print_status "Installing Cordova globally..."
npm install -g cordova

if [ $? -eq 0 ]; then
    print_status "Cordova installed successfully!"
    echo ""
    echo "To build APK with Cordova:"
    echo "1. cordova create mens-kart-cordova com.menskart.app 'Mens Kart'"
    echo "2. cd mens-kart-cordova"
    echo "3. cp -r ../frontend/* www/"
    echo "4. cp ../config.xml ."
    echo "5. cordova platform add android"
    echo "6. cordova plugin add cordova-plugin-whitelist"
    echo "7. cordova build android"
    echo ""
    echo "APK will be in: mens-kart-cordova/platforms/android/app/build/outputs/apk/"
else
    print_error "Failed to install Cordova"
fi

# Method 3: Capacitor
echo ""
print_header "3" "Capacitor Method (Modern Cordova)"
echo "This is a modern alternative to Cordova with better performance"
echo ""

print_status "Installing Capacitor globally..."
npm install -g @capacitor/cli

if [ $? -eq 0 ]; then
    print_status "Capacitor installed successfully!"
    echo ""
    echo "To build APK with Capacitor:"
    echo "1. npx cap init 'Mens Kart' com.menskart.app"
    echo "2. npx cap add android"
    echo "3. npx cap sync android"
    echo "4. npx cap open android"
    echo "5. Build APK in Android Studio"
    echo ""
else
    print_error "Failed to install Capacitor"
fi

# Method 4: Bubblewrap (Google's PWA to APK tool)
echo ""
print_header "4" "Bubblewrap Method (Google's Official Tool)"
echo "This is Google's official tool for PWA to APK conversion"
echo ""

print_status "Installing Bubblewrap..."
npm install -g @bubblewrap/cli

if [ $? -eq 0 ]; then
    print_status "Bubblewrap installed successfully!"
    echo ""
    echo "To build APK with Bubblewrap:"
    echo "1. bubblewrap init --manifest=https://your-domain.com/manifest.json"
    echo "2. bubblewrap build"
    echo ""
    echo "APK will be generated in the current directory"
else
    print_error "Failed to install Bubblewrap"
fi

echo ""
print_header "5" "Online Tools (No Installation Required)"
echo "Use these online services for quick APK generation:"
echo ""
echo "• PWABuilder.com - https://www.pwabuilder.com"
echo "• PWA2APK.com - https://www.pwa2apk.com"
echo "• Web2Apk.com - https://web2apk.com"
echo ""
echo "Simply enter your website URL and download the APK!"
echo ""

# Create a quick setup script
echo ""
print_status "Creating quick setup script..."
cat > quick-apk-setup.sh << 'EOF'
#!/bin/bash
# Quick APK Setup Script for Mens Kart

echo "Setting up Mens Kart for APK build..."

# Install dependencies
npm install

# Start backend server
npm run dev &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Install PWA Builder and build APK
npm install -g pwa-builder
pwa-builder http://localhost:5000

# Kill backend
kill $BACKEND_PID

echo "APK build process completed!"
echo "Check the generated files for your APK."
EOF

chmod +x quick-apk-setup.sh

print_status "Quick setup script created: quick-apk-setup.sh"
print_status "Run './quick-apk-setup.sh' for automated APK building"

echo ""
print_header "✅" "Setup Complete!"
echo ""
echo "Your Mens Kart web app is now ready for APK conversion!"
echo ""
echo "📱 Recommended Next Steps:"
echo "1. Deploy your web app to a domain (e.g., Netlify, Vercel)"
echo "2. Use PWABuilder.com for instant APK generation"
echo "3. Test the APK on Android devices"
echo "4. Publish to Google Play Store"
echo ""
echo "🎯 For production APK:"
echo "• Use Cordova/PhoneGap for more control"
echo "• Add proper signing certificates"
echo "• Configure app icons and splash screens"
echo "• Test on multiple Android versions"
echo ""
echo "📞 Need help? Check APK_BUILD_GUIDE.md for detailed instructions!"
echo ""
print_status "Happy APK building! 🚀📱"