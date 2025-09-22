@echo off
REM Mens Kart APK Build Demo Script for Windows
REM This script demonstrates different methods to build APK from web app

echo 🚀 Mens Kart APK Build Demo
echo =============================

REM Colors for Windows CMD (limited support)
echo [INFO] Checking system requirements...

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm is not installed. Please install npm first.
    pause
    exit /b 1
)

echo [INFO] Node.js version:
node --version
echo [INFO] npm version:
npm --version

echo.
echo [METHOD 1] Progressive Web App (PWA) Method - RECOMMENDED
echo This method converts your existing PWA to APK
echo.

echo [INFO] Installing PWA Builder globally...
npm install -g pwa-builder

if %errorlevel% equ 0 (
    echo [INFO] PWA Builder installed successfully!
    echo.
    echo To build APK with PWA Builder:
    echo 1. Run: pwa-builder https://your-domain.com
    echo 2. Follow the prompts to generate APK
    echo 3. Download the generated APK file
    echo.
) else (
    echo [ERROR] Failed to install PWA Builder
)

echo.
echo [METHOD 2] Apache Cordova Method
echo This method wraps your web app in a native Android container
echo.

echo [INFO] Installing Cordova globally...
npm install -g cordova

if %errorlevel% equ 0 (
    echo [INFO] Cordova installed successfully!
    echo.
    echo To build APK with Cordova:
    echo 1. cordova create mens-kart-cordova com.menskart.app "Mens Kart"
    echo 2. cd mens-kart-cordova
    echo 3. xcopy ..\frontend\* www\ /E /I /H /Y
    echo 4. copy ..\config.xml .
    echo 5. cordova platform add android
    echo 6. cordova plugin add cordova-plugin-whitelist
    echo 7. cordova build android
    echo.
    echo APK will be in: mens-kart-cordova\platforms\android\app\build\outputs\apk\
) else (
    echo [ERROR] Failed to install Cordova
)

echo.
echo [METHOD 3] Capacitor Method (Modern Cordova)
echo This is a modern alternative to Cordova with better performance
echo.

echo [INFO] Installing Capacitor globally...
npm install -g @capacitor/cli

if %errorlevel% equ 0 (
    echo [INFO] Capacitor installed successfully!
    echo.
    echo To build APK with Capacitor:
    echo 1. npx cap init "Mens Kart" com.menskart.app
    echo 2. npx cap add android
    echo 3. npx cap sync android
    echo 4. npx cap open android
    echo 5. Build APK in Android Studio
    echo.
) else (
    echo [ERROR] Failed to install Capacitor
)

echo.
echo [METHOD 4] Bubblewrap Method (Google's Official Tool)
echo This is Google's official tool for PWA to APK conversion
echo.

echo [INFO] Installing Bubblewrap...
npm install -g @bubblewrap/cli

if %errorlevel% equ 0 (
    echo [INFO] Bubblewrap installed successfully!
    echo.
    echo To build APK with Bubblewrap:
    echo 1. bubblewrap init --manifest=https://your-domain.com/manifest.json
    echo 2. bubblewrap build
    echo.
    echo APK will be generated in the current directory
) else (
    echo [ERROR] Failed to install Bubblewrap
)

echo.
echo [METHOD 5] Online Tools (No Installation Required)
echo Use these online services for quick APK generation:
echo.
echo • PWABuilder.com - https://www.pwabuilder.com
echo • PWA2APK.com - https://www.pwa2apk.com
echo • Web2Apk.com - https://web2apk.com
echo.
echo Simply enter your website URL and download the APK!
echo.

echo.
echo [INFO] Creating quick setup batch file...

echo @echo off > quick-apk-setup.bat
echo REM Quick APK Setup Script for Mens Kart (Windows) >> quick-apk-setup.bat
echo echo Setting up Mens Kart for APK build... >> quick-apk-setup.bat
echo. >> quick-apk-setup.bat
echo REM Install dependencies >> quick-apk-setup.bat
echo call npm install >> quick-apk-setup.bat
echo. >> quick-apk-setup.bat
echo REM Start backend server >> quick-apk-setup.bat
echo start cmd /k "npm run dev" >> quick-apk-setup.bat
echo. >> quick-apk-setup.bat
echo REM Wait for backend to start >> quick-apk-setup.bat
echo timeout /t 5 /nobreak ^> nul >> quick-apk-setup.bat
echo. >> quick-apk-setup.bat
echo REM Install PWA Builder and build APK >> quick-apk-setup.bat
echo npm install -g pwa-builder >> quick-apk-setup.bat
echo pwa-builder http://localhost:5000 >> quick-apk-setup.bat
echo. >> quick-apk-setup.bat
echo echo APK build process completed! >> quick-apk-setup.bat
echo echo Check the generated files for your APK. >> quick-apk-setup.bat
echo pause >> quick-apk-setup.bat

echo [INFO] Quick setup batch file created: quick-apk-setup.bat
echo [INFO] Run 'quick-apk-setup.bat' for automated APK building

echo.
echo [✅] Setup Complete!
echo.
echo Your Mens Kart web app is now ready for APK conversion!
echo.
echo 📱 Recommended Next Steps:
echo 1. Deploy your web app to a domain (e.g., Netlify, Vercel)
echo 2. Use PWABuilder.com for instant APK generation
echo 3. Test the APK on Android devices
echo 4. Publish to Google Play Store
echo.
echo 🎯 For production APK:
echo • Use Cordova/PhoneGap for more control
echo • Add proper signing certificates
echo • Configure app icons and splash screens
echo • Test on multiple Android versions
echo.
echo 📞 Need help? Check APK_BUILD_GUIDE.md for detailed instructions!
echo.
echo [INFO] Happy APK building! 🚀📱
pause