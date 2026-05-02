# MediConnect — Doctor Appointment & Telemedicine App

## Real Backend Upgrade (Django + PostgreSQL)

This repository now includes a production-oriented backend at `/backend` to support real account creation, real authentication, role-based dashboards, and database-backed medical workflows.

### 1) Full medical website feature plan
- Patient onboarding: signup/login, profile, appointment history
- Doctor workspace: role-specific dashboard and patient appointment queue
- Admin operations: user role oversight, appointment volume monitoring, Django admin management
- Core medical data: persistent appointment entities with lifecycle status
- Security baseline: authenticated routes, password validation, CSRF/session handling

### 2) Real app architecture introduced
- **Backend stack:** Django 5 + PostgreSQL driver (`psycopg`)
- **Apps:** `accounts` (auth/roles/dashboards), `clinic` (appointments)
- **Custom user model:** `MedicalUser` with roles (`patient`, `doctor`, `admin`)
- **Database:** PostgreSQL via environment variables (`POSTGRES_*`), SQLite fallback for local quickstart

### 3) Signup/Login + Dashboard + Admin flows
- Real signup creates user records in the database
- Real login/logout using Django auth
- Role-based dashboard routing:
  - `/dashboard/patient/`
  - `/dashboard/doctor/`
  - `/dashboard/admin/`
- Admin flow includes operational summary page + Django admin site (`/admin/`)

### 4) Initial code changes completed
- Added backend project scaffold in `/backend`
- Added real auth models/forms/views/routes/templates
- Added appointment model and appointment list route
- Added backend tests for signup and role-based dashboard redirect

### Run the backend locally
```bash
cd backend
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### PostgreSQL configuration (production-ready path)
Set these environment variables before running migrations/server:
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

## Complete Setup Guide for Android Studio

---

## STEP 1 — Prerequisites

Make sure you have installed:
- Flutter SDK 3.16+ → https://flutter.dev/docs/get-started/install
- Android Studio (with Flutter & Dart plugins)
- Java JDK 17
- Android SDK (API 33 or higher)

Verify your setup:
```bash
flutter doctor
```
All items should show ✓ (green).

---

## STEP 2 — Firebase Project Setup

### 2.1 Create Firebase Project
1. Go to https://console.firebase.google.com
2. Click "Add project" → name it "MediConnect"
3. Enable Google Analytics (optional)

### 2.2 Enable Firebase Services
In Firebase Console sidebar, enable each of these:
- **Authentication** → Sign-in methods → Enable "Email/Password" and "Google"
- **Firestore Database** → Create database → Start in **test mode** (change rules before production)
- **Storage** → Get started → Start in test mode
- **Cloud Messaging** → Already enabled by default

### 2.3 Add Android App
1. In Firebase Console → Project Settings → Add App → Android
2. Android package name: `com.yourname.doctor_app`
   - You can find/change this in `android/app/build.gradle` → `applicationId`
3. Download `google-services.json`
4. Place it in: `android/app/google-services.json`

### 2.4 Add iOS App (optional)
1. Add App → iOS
2. Bundle ID: `com.yourname.doctorApp`
3. Download `GoogleService-Info.plist`
4. Place it in: `ios/Runner/GoogleService-Info.plist`

### 2.5 Connect Flutter to Firebase (EASIEST METHOD)
```bash
# Install FlutterFire CLI
dart pub global activate flutterfire_cli

# In your project directory:
flutterfire configure
```
This auto-generates `lib/firebase_options.dart` with your real credentials.
It REPLACES the placeholder file already in the project.

---

## STEP 3 — Agora Setup (for Video Calls)

1. Go to https://www.agora.io and create a free account
2. Create a new project → select "Testing" mode
3. Copy your **App ID**
4. Open `lib/features/video/video_call_screen.dart`
5. Replace `YOUR_AGORA_APP_ID` with your actual App ID:
   ```dart
   const String _agoraAppId = 'abc123def456...'; // your real ID here
   ```

> **Note:** In "Testing" mode, tokens are not required. For production,
> generate tokens via Firebase Cloud Functions.

---

## STEP 4 — Install Dependencies

```bash
cd doctor_app
flutter pub get
```

---

## STEP 5 — Add Fonts & Assets

The app uses Poppins font. Download from Google Fonts:
https://fonts.google.com/specimen/Poppins

Download these weights and place in `assets/fonts/`:
- `Poppins-Regular.ttf`
- `Poppins-Medium.ttf`
- `Poppins-SemiBold.ttf`
- `Poppins-Bold.ttf`

Also create the assets/images/ directory (even if empty):
```bash
mkdir -p assets/images
mkdir -p assets/fonts
```

**OR** if you want to skip custom fonts temporarily, remove the fonts section
from `pubspec.yaml` and remove `fontFamily: 'Poppins'` from `app_colors.dart`.

---

## STEP 6 — Android Configuration

### 6.1 Update build.gradle (app-level)
In `android/app/build.gradle`:
```groovy
android {
    compileSdkVersion 34

    defaultConfig {
        applicationId "com.yourname.doctor_app"  // match Firebase
        minSdkVersion 23
        targetSdkVersion 34
        versionCode 1
        versionName "1.0.0"
    }
}

dependencies {
    implementation platform('com.google.firebase:firebase-bom:32.7.0')
    implementation 'com.google.firebase:firebase-analytics'
}
```

### 6.2 Update build.gradle (project-level)
In `android/build.gradle`:
```groovy
buildscript {
    dependencies {
        classpath 'com.google.gms:google-services:4.4.1'
    }
}
```

### 6.3 Apply Google Services Plugin
At the bottom of `android/app/build.gradle`:
```groovy
apply plugin: 'com.google.gms.google-services'
```

---

## STEP 7 — Firestore Indexes (Required)

Create these indexes in Firebase Console → Firestore → Indexes:

| Collection | Fields | Order |
|---|---|---|
| doctors | specialty ASC, rating DESC | Composite |
| appointments | patientId ASC, createdAt DESC | Composite |
| appointments | doctorId ASC, createdAt DESC | Composite |
| chats/{id}/messages | timestamp ASC | Single field |

> Firebase will prompt you to create indexes automatically when the app
> first runs queries that need them — just click the link in the console error.

---

## STEP 8 — Deploy Firestore Security Rules

In Firebase Console → Firestore → Rules, paste the contents of `firestore.rules`.

---

## STEP 9 — Run the App

```bash
# Run on connected Android device or emulator
flutter run

# Run on specific device
flutter run -d <device-id>

# List available devices
flutter devices

# Run on Chrome (web)
flutter run -d chrome
```

---

## STEP 10 — Create Demo Data

After first run, register 3 accounts:

1. **Admin account**
   - Email: `admin@mediconnect.com`
   - Password: any
   - Role: Patient (then manually change `role` to `admin` in Firestore)

2. **Doctor account**
   - Email: `doctor@mediconnect.com`
   - Role: Doctor
   - After login → Profile → Edit → add specialty, fee, about

3. **Patient account**
   - Email: `patient@mediconnect.com`
   - Role: Patient

**To set admin role manually:**
1. Firebase Console → Firestore → users collection
2. Find the admin user document
3. Change `role` field from `"patient"` to `"admin"`

---

## App Structure

```
lib/
├── main.dart                    ← App entry point
├── firebase_options.dart        ← Auto-generated by flutterfire configure
├── core/
│   ├── constants/
│   │   └── app_colors.dart      ← Colors, theme
│   ├── models/
│   │   └── models.dart          ← UserModel, DoctorModel, AppointmentModel, etc.
│   ├── services/
│   │   └── services.dart        ← AuthService, FirestoreService, StorageService
│   ├── router/
│   │   └── app_router.dart      ← GoRouter with role-based navigation
│   └── widgets/
│       └── widgets.dart         ← Shared UI components
├── providers/
│   └── providers.dart           ← All Riverpod providers
└── features/
    ├── auth/                    ← Splash, Login, Register
    ├── patient/                 ← Home, Doctors, Booking, Appointments
    ├── doctor/                  ← Dashboard, Schedule
    ├── admin/                   ← Dashboard, Users, Appointments
    ├── chat/                    ← Chat list, Chat screen
    ├── video/                   ← Video call screen (Agora)
    └── profile/                 ← Profile editing
```

---

## Common Issues & Fixes

### "google-services.json not found"
→ Make sure the file is in `android/app/` not `android/`

### "Firebase App not initialized"
→ Run `flutterfire configure` again, or check `firebase_options.dart` has real values

### "CLEARTEXT traffic not permitted"
→ Add `android:usesCleartextTraffic="true"` in AndroidManifest.xml temporarily (dev only)

### "Agora Error: invalid App ID"
→ Replace `YOUR_AGORA_APP_ID` in `video_call_screen.dart` with your real ID from agora.io

### "No slots available"
→ Tap "Load Slots" button on the booking screen. Slots are seeded when you select a date.

### Camera / Mic permission denied
→ Go to Android Settings → Apps → MediConnect → Permissions → Enable Camera & Microphone

### "MissingPluginException on web"
→ Some plugins (Agora, image_picker) have limited web support. Video calls are mobile-only.

### Google Sign-In fails
→ Add your debug SHA-1 to Firebase:
```bash
cd android && ./gradlew signingReport
```
Copy the SHA-1 and add it in Firebase Console → Project Settings → Android app.

---

## Building Release APK

```bash
# Generate keystore (do once)
keytool -genkey -v -keystore android/app/release.jks \
  -alias mediconnect -keyalg RSA -keysize 2048 -validity 10000

# Build release APK
flutter build apk --release

# Build App Bundle (for Play Store)
flutter build appbundle --release

# Output location:
# build/app/outputs/flutter-apk/app-release.apk
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Flutter (Dart) |
| State Management | Riverpod 2.x |
| Navigation | GoRouter |
| Auth | Firebase Auth |
| Database | Cloud Firestore |
| Storage | Firebase Storage |
| Notifications | Firebase Cloud Messaging |
| Video Calls | Agora RTC Engine |
| Image Caching | cached_network_image |
| Calendar | table_calendar |

## Author
Yaseen Haider
