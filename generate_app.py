#!/usr/bin/env python3
import os, zipfile

files = {}

# ─────────────────────────────────────────────────────────────
# pubspec.yaml
# ─────────────────────────────────────────────────────────────
files['pubspec.yaml'] = """name: doctor_appointment_app
description: Doctor Appointment & Telemedicine App
publish_to: "none"
version: 1.0.0+1

environment:
  sdk: ">=3.2.0 <4.0.0"

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.6

  # Firebase
  firebase_core: ^2.27.0
  firebase_auth: ^4.17.9
  cloud_firestore: ^4.15.9
  firebase_storage: ^11.6.10
  firebase_messaging: ^14.7.20

  # Auth
  google_sign_in: ^6.2.1

  # State Management
  flutter_riverpod: ^2.5.1

  # Navigation
  go_router: ^13.2.0

  # UI
  cached_network_image: ^3.3.1
  shimmer: ^3.0.0
  table_calendar: ^3.1.1
  flutter_rating_bar: ^4.0.1

  # Utils
  intl: ^0.19.0
  image_picker: ^1.0.7
  uuid: ^4.3.3

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.1

flutter:
  uses-material-design: true
  assets:
    - assets/images/
"""

# ─────────────────────────────────────────────────────────────
# README
# ─────────────────────────────────────────────────────────────
files['README.md'] = """# Doctor Appointment & Telemedicine App

## Setup Instructions

### 1. Install Flutter
- Download from https://flutter.dev
- Run `flutter doctor` — ensure all checks pass

### 2. Firebase Setup (REQUIRED)
```bash
npm install -g firebase-tools
dart pub global activate flutterfire_cli
firebase login
flutterfire configure
```
This auto-generates `lib/firebase_options.dart`. Delete the placeholder file first.

### 3. Enable Firebase Services (Firebase Console)
- Authentication → Enable Email/Password and Google
- Firestore → Create database (start in test mode)
- Storage → Get started
- Cloud Messaging → Already enabled

### 4. Firestore Indexes (Firebase Console → Indexes)
Create these composite indexes:
| Collection       | Fields                            |
|-----------------|-----------------------------------|
| doctors         | specialty ASC + rating DESC       |
| appointments    | patientId ASC + createdAt DESC    |
| appointments    | doctorId ASC + status ASC         |

### 5. Run the App
```bash
flutter pub get
flutter run                    # Android/iOS
flutter run -d chrome          # Web
```

### 6. Add Sample Doctors (Firestore)
The app needs doctor accounts. Register a user, then in Firestore:
- Set /users/{uid}/role to "doctor"
- Create /doctors/{uid} with: name, specialty, fee, rating, experience, about, photoUrl, isVerified:true

### Video Calls
For production video calls, add Agora SDK:
1. Sign up at agora.io
2. Add `agora_rtc_engine: ^6.3.2` to pubspec.yaml
3. Follow integration guide in lib/features/video/video_call_screen.dart
"""

# ─────────────────────────────────────────────────────────────
# firebase_options.dart (placeholder)
# ─────────────────────────────────────────────────────────────
files['lib/firebase_options.dart'] = """// !! REPLACE THIS FILE !!
// Run: flutterfire configure
// This auto-generates the correct firebase_options.dart

import 'package:firebase_core/firebase_core.dart' show FirebaseOptions;
import 'package:flutter/foundation.dart'
    show defaultTargetPlatform, kIsWeb, TargetPlatform;

class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) return web;
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return android;
      case TargetPlatform.iOS:
        return ios;
      default:
        throw UnsupportedError('Unsupported platform');
    }
  }

  // Replace all values below with your Firebase project config
  static const FirebaseOptions web = FirebaseOptions(
    apiKey: 'YOUR_WEB_API_KEY',
    appId: 'YOUR_WEB_APP_ID',
    messagingSenderId: 'YOUR_SENDER_ID',
    projectId: 'YOUR_PROJECT_ID',
    authDomain: 'YOUR_PROJECT_ID.firebaseapp.com',
    storageBucket: 'YOUR_PROJECT_ID.appspot.com',
  );

  static const FirebaseOptions android = FirebaseOptions(
    apiKey: 'YOUR_ANDROID_API_KEY',
    appId: 'YOUR_ANDROID_APP_ID',
    messagingSenderId: 'YOUR_SENDER_ID',
    projectId: 'YOUR_PROJECT_ID',
    storageBucket: 'YOUR_PROJECT_ID.appspot.com',
  );

  static const FirebaseOptions ios = FirebaseOptions(
    apiKey: 'YOUR_IOS_API_KEY',
    appId: 'YOUR_IOS_APP_ID',
    messagingSenderId: 'YOUR_SENDER_ID',
    projectId: 'YOUR_PROJECT_ID',
    storageBucket: 'YOUR_PROJECT_ID.appspot.com',
    iosBundleId: 'com.yourname.doctorAppointmentApp',
  );
}
"""

# ─────────────────────────────────────────────────────────────
# main.dart
# ─────────────────────────────────────────────────────────────
files['lib/main.dart'] = """import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'firebase_options.dart';
import 'router.dart';
import 'core/constants/app_theme.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  runApp(const ProviderScope(child: MedConnectApp()));
}

class MedConnectApp extends ConsumerWidget {
  const MedConnectApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);
    return MaterialApp.router(
      title: 'MedConnect',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light,
      routerConfig: router,
    );
  }
}
"""

# ─────────────────────────────────────────────────────────────
# router.dart
# ─────────────────────────────────────────────────────────────
files['lib/router.dart'] = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'providers/auth_provider.dart';
import 'features/auth/splash_screen.dart';
import 'features/auth/login_screen.dart';
import 'features/auth/register_screen.dart';
import 'features/patient/home/patient_home_screen.dart';
import 'features/patient/doctors/doctor_list_screen.dart';
import 'features/patient/doctors/doctor_profile_screen.dart';
import 'features/patient/appointments/book_appointment_screen.dart';
import 'features/patient/appointments/patient_appointments_screen.dart';
import 'features/patient/profile/patient_profile_screen.dart';
import 'features/doctor/home/doctor_home_screen.dart';
import 'features/doctor/appointments/doctor_appointments_screen.dart';
import 'features/doctor/profile/doctor_profile_screen.dart';
import 'features/doctor/availability/doctor_availability_screen.dart';
import 'features/admin/home/admin_home_screen.dart';
import 'features/chat/chat_list_screen.dart';
import 'features/chat/chat_screen.dart';
import 'features/video/video_call_screen.dart';
import 'models/doctor_model.dart';

final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authStateProvider);

  return GoRouter(
    initialLocation: '/splash',
    redirect: (context, state) {
      final isLoggedIn = authState.value != null;
      final onAuth = state.fullPath == '/login' ||
          state.fullPath == '/register' ||
          state.fullPath == '/splash';

      if (!isLoggedIn && !onAuth) return '/login';
      return null;
    },
    routes: [
      GoRoute(path: '/splash', builder: (_, __) => const SplashScreen()),
      GoRoute(path: '/login', builder: (_, __) => const LoginScreen()),
      GoRoute(path: '/register', builder: (_, __) => const RegisterScreen()),

      // Patient routes
      GoRoute(path: '/patient/home', builder: (_, __) => const PatientHomeScreen()),
      GoRoute(path: '/patient/doctors', builder: (_, __) => const DoctorListScreen()),
      GoRoute(
        path: '/patient/doctor-profile',
        builder: (ctx, state) {
          final doctor = state.extra as DoctorModel;
          return DoctorProfileScreen(doctor: doctor);
        },
      ),
      GoRoute(
        path: '/patient/book',
        builder: (ctx, state) {
          final doctor = state.extra as DoctorModel;
          return BookAppointmentScreen(doctor: doctor);
        },
      ),
      GoRoute(path: '/patient/appointments', builder: (_, __) => const PatientAppointmentsScreen()),
      GoRoute(path: '/patient/profile', builder: (_, __) => const PatientProfileScreen()),

      // Doctor routes
      GoRoute(path: '/doctor/home', builder: (_, __) => const DoctorHomeScreen()),
      GoRoute(path: '/doctor/appointments', builder: (_, __) => const DoctorAppointmentsScreen()),
      GoRoute(path: '/doctor/profile', builder: (_, __) => const DoctorProfileScreen()),
      GoRoute(path: '/doctor/availability', builder: (_, __) => const DoctorAvailabilityScreen()),

      // Admin routes
      GoRoute(path: '/admin/home', builder: (_, __) => const AdminHomeScreen()),

      // Shared routes
      GoRoute(path: '/chats', builder: (_, __) => const ChatListScreen()),
      GoRoute(
        path: '/chat',
        builder: (ctx, state) {
          final extra = state.extra as Map<String, String>;
          return ChatScreen(
            chatId: extra['chatId']!,
            otherUserName: extra['otherUserName']!,
            otherUserId: extra['otherUserId']!,
          );
        },
      ),
      GoRoute(
        path: '/video-call',
        builder: (ctx, state) {
          final extra = state.extra as Map<String, String>;
          return VideoCallScreen(
            appointmentId: extra['appointmentId']!,
            doctorName: extra['doctorName']!,
          );
        },
      ),
    ],
  );
});
"""

# ─────────────────────────────────────────────────────────────
# core/constants/app_colors.dart
# ─────────────────────────────────────────────────────────────
files['lib/core/constants/app_colors.dart'] = """import 'package:flutter/material.dart';

class AppColors {
  // Primary
  static const primary = Color(0xFF1A73E8);
  static const primaryDark = Color(0xFF1557B0);
  static const primaryLight = Color(0xFFE8F0FE);

  // Secondary
  static const secondary = Color(0xFF34A853);
  static const secondaryLight = Color(0xFFE6F4EA);

  // Status
  static const success = Color(0xFF34A853);
  static const warning = Color(0xFFFBBC04);
  static const error = Color(0xFFEA4335);
  static const info = Color(0xFF4285F4);

  // Neutral
  static const white = Color(0xFFFFFFFF);
  static const background = Color(0xFFF8F9FA);
  static const surface = Color(0xFFFFFFFF);
  static const border = Color(0xFFE0E0E0);
  static const divider = Color(0xFFF0F0F0);

  // Text
  static const textPrimary = Color(0xFF1A1A2E);
  static const textSecondary = Color(0xFF6B7280);
  static const textHint = Color(0xFF9CA3AF);

  // Specialty colors
  static const cardiology = Color(0xFFFF6B6B);
  static const neurology = Color(0xFF6C63FF);
  static const pediatrics = Color(0xFFFFB347);
  static const dermatology = Color(0xFF4ECDC4);
  static const orthopedics = Color(0xFF45B7D1);
  static const general = Color(0xFF96CEB4);
}
"""

# ─────────────────────────────────────────────────────────────
# core/constants/app_theme.dart
# ─────────────────────────────────────────────────────────────
files['lib/core/constants/app_theme.dart'] = """import 'package:flutter/material.dart';
import 'app_colors.dart';

class AppTheme {
  static ThemeData get light => ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: AppColors.primary,
          primary: AppColors.primary,
          surface: AppColors.surface,
          background: AppColors.background,
        ),
        scaffoldBackgroundColor: AppColors.background,
        fontFamily: 'Roboto',
        appBarTheme: const AppBarTheme(
          backgroundColor: AppColors.white,
          foregroundColor: AppColors.textPrimary,
          elevation: 0,
          centerTitle: true,
          surfaceTintColor: Colors.transparent,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.primary,
            foregroundColor: AppColors.white,
            elevation: 0,
            minimumSize: const Size(double.infinity, 52),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
            textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
          ),
        ),
        outlinedButtonTheme: OutlinedButtonThemeData(
          style: OutlinedButton.styleFrom(
            foregroundColor: AppColors.primary,
            minimumSize: const Size(double.infinity, 52),
            side: const BorderSide(color: AppColors.primary),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
            textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: AppColors.white,
          contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: AppColors.border),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: AppColors.border),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: AppColors.primary, width: 2),
          ),
          errorBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: AppColors.error),
          ),
          hintStyle: const TextStyle(color: AppColors.textHint),
        ),
        cardTheme: CardTheme(
          color: AppColors.white,
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
            side: const BorderSide(color: AppColors.border, width: 0.5),
          ),
        ),
        chipTheme: ChipThemeData(
          backgroundColor: AppColors.primaryLight,
          labelStyle: const TextStyle(color: AppColors.primary, fontSize: 12),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        ),
      );
}
"""

# ─────────────────────────────────────────────────────────────
# core/utils/helpers.dart
# ─────────────────────────────────────────────────────────────
files['lib/core/utils/helpers.dart'] = """import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class Helpers {
  static String formatDate(DateTime date) =>
      DateFormat('MMM dd, yyyy').format(date);

  static String formatTime(String time) {
    final parts = time.split(':');
    final hour = int.parse(parts[0]);
    final minute = parts[1];
    final suffix = hour >= 12 ? 'PM' : 'AM';
    final displayHour = hour > 12 ? hour - 12 : (hour == 0 ? 12 : hour);
    return '\$displayHour:\$minute \$suffix';
  }

  static Color statusColor(String status) {
    switch (status) {
      case 'confirmed': return const Color(0xFF34A853);
      case 'pending': return const Color(0xFFFBBC04);
      case 'cancelled': return const Color(0xFFEA4335);
      case 'completed': return const Color(0xFF4285F4);
      default: return Colors.grey;
    }
  }

  static String getChatId(String uid1, String uid2) {
    final sorted = [uid1, uid2]..sort();
    return '\${sorted[0]}_\${sorted[1]}';
  }

  static String getInitials(String name) {
    final parts = name.trim().split(' ');
    if (parts.length >= 2) return '\${parts[0][0]}\${parts[1][0]}'.toUpperCase();
    return parts[0].isNotEmpty ? parts[0][0].toUpperCase() : '?';
  }

  static void showSnackBar(BuildContext context, String message, {bool isError = false}) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text(message),
      backgroundColor: isError ? const Color(0xFFEA4335) : const Color(0xFF34A853),
      behavior: SnackBarBehavior.floating,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
    ));
  }

  static List<String> generateTimeSlots() {
    return [
      '08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
      '11:00', '11:30', '12:00', '12:30', '14:00', '14:30',
      '15:00', '15:30', '16:00', '16:30', '17:00', '17:30',
    ];
  }
}
"""

# ─────────────────────────────────────────────────────────────
# core/widgets/custom_button.dart
# ─────────────────────────────────────────────────────────────
files['lib/core/widgets/custom_button.dart'] = """import 'package:flutter/material.dart';
import '../constants/app_colors.dart';

class AppButton extends StatelessWidget {
  final String label;
  final VoidCallback? onTap;
  final bool loading;
  final bool outline;
  final Color? color;
  final double? width;
  final IconData? icon;

  const AppButton({
    super.key,
    required this.label,
    this.onTap,
    this.loading = false,
    this.outline = false,
    this.color,
    this.width,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    final bg = color ?? AppColors.primary;
    return SizedBox(
      width: width ?? double.infinity,
      height: 52,
      child: outline
          ? OutlinedButton.icon(
              onPressed: loading ? null : onTap,
              icon: icon != null ? Icon(icon, size: 20) : const SizedBox.shrink(),
              label: loading
                  ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2))
                  : Text(label),
              style: OutlinedButton.styleFrom(foregroundColor: bg, side: BorderSide(color: bg)),
            )
          : ElevatedButton.icon(
              onPressed: loading ? null : onTap,
              icon: icon != null ? Icon(icon, size: 20, color: Colors.white) : const SizedBox.shrink(),
              label: loading
                  ? const SizedBox(
                      width: 20, height: 20,
                      child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                  : Text(label),
              style: ElevatedButton.styleFrom(backgroundColor: bg),
            ),
    );
  }
}
"""

# ─────────────────────────────────────────────────────────────
# core/widgets/custom_text_field.dart
# ─────────────────────────────────────────────────────────────
files['lib/core/widgets/custom_text_field.dart'] = """import 'package:flutter/material.dart';

class AppTextField extends StatelessWidget {
  final String label;
  final String? hint;
  final TextEditingController? controller;
  final bool obscure;
  final TextInputType keyboardType;
  final String? Function(String?)? validator;
  final Widget? prefix;
  final Widget? suffix;
  final int maxLines;
  final bool readOnly;
  final VoidCallback? onTap;
  final void Function(String)? onChanged;

  const AppTextField({
    super.key,
    required this.label,
    this.hint,
    this.controller,
    this.obscure = false,
    this.keyboardType = TextInputType.text,
    this.validator,
    this.prefix,
    this.suffix,
    this.maxLines = 1,
    this.readOnly = false,
    this.onTap,
    this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label,
            style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500, color: Color(0xFF374151))),
        const SizedBox(height: 6),
        TextFormField(
          controller: controller,
          obscureText: obscure,
          keyboardType: keyboardType,
          validator: validator,
          maxLines: maxLines,
          readOnly: readOnly,
          onTap: onTap,
          onChanged: onChanged,
          decoration: InputDecoration(hintText: hint, prefixIcon: prefix, suffixIcon: suffix),
        ),
      ],
    );
  }
}
"""

# ─────────────────────────────────────────────────────────────
# core/widgets/loading_overlay.dart
# ─────────────────────────────────────────────────────────────
files['lib/core/widgets/loading_overlay.dart'] = """import 'package:flutter/material.dart';
import '../constants/app_colors.dart';

class LoadingOverlay extends StatelessWidget {
  final bool loading;
  final Widget child;
  const LoadingOverlay({super.key, required this.loading, required this.child});

  @override
  Widget build(BuildContext context) => Stack(children: [
        child,
        if (loading)
          const ColoredBox(
            color: Color(0x55000000),
            child: Center(child: CircularProgressIndicator(color: AppColors.white)),
          ),
      ]);
}

class ShimmerCard extends StatelessWidget {
  final double height;
  const ShimmerCard({super.key, this.height = 120});

  @override
  Widget build(BuildContext context) => Container(
        height: height,
        margin: const EdgeInsets.only(bottom: 12),
        decoration: BoxDecoration(
          color: Colors.grey[200],
          borderRadius: BorderRadius.circular(16),
        ),
      );
}

class EmptyState extends StatelessWidget {
  final String title;
  final String subtitle;
  final IconData icon;
  final String? buttonLabel;
  final VoidCallback? onButton;

  const EmptyState({
    super.key,
    required this.title,
    required this.subtitle,
    required this.icon,
    this.buttonLabel,
    this.onButton,
  });

  @override
  Widget build(BuildContext context) => Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppColors.primaryLight,
                shape: BoxShape.circle,
              ),
              child: Icon(icon, size: 48, color: AppColors.primary),
            ),
            const SizedBox(height: 20),
            Text(title,
                style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
            const SizedBox(height: 8),
            Text(subtitle,
                textAlign: TextAlign.center,
                style: const TextStyle(color: AppColors.textSecondary, fontSize: 15)),
            if (buttonLabel != null && onButton != null) ...[
              const SizedBox(height: 24),
              ElevatedButton(onPressed: onButton, child: Text(buttonLabel!)),
            ],
          ]),
        ),
      );
}
"""

# ─────────────────────────────────────────────────────────────
# core/widgets/doctor_card.dart
# ─────────────────────────────────────────────────────────────
files['lib/core/widgets/doctor_card.dart'] = """import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import '../../models/doctor_model.dart';
import '../constants/app_colors.dart';

class DoctorCard extends StatelessWidget {
  final DoctorModel doctor;
  final VoidCallback? onTap;
  final VoidCallback? onBook;

  const DoctorCard({super.key, required this.doctor, this.onTap, this.onBook});

  @override
  Widget build(BuildContext context) => GestureDetector(
        onTap: onTap,
        child: Container(
          margin: const EdgeInsets.only(bottom: 12),
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            color: AppColors.white,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: AppColors.border, width: 0.5),
          ),
          child: Row(children: [
            CircleAvatar(
              radius: 32,
              backgroundColor: AppColors.primaryLight,
              backgroundImage: doctor.photoUrl.isNotEmpty
                  ? CachedNetworkImageProvider(doctor.photoUrl)
                  : null,
              child: doctor.photoUrl.isEmpty
                  ? Text(doctor.name.substring(0, 1),
                      style: const TextStyle(fontSize: 22, color: AppColors.primary, fontWeight: FontWeight.bold))
                  : null,
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Row(children: [
                  Expanded(
                    child: Text(doctor.name,
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                  ),
                  if (doctor.isVerified)
                    const Icon(Icons.verified, color: AppColors.primary, size: 16),
                ]),
                const SizedBox(height: 2),
                Text(doctor.specialty,
                    style: const TextStyle(color: AppColors.textSecondary, fontSize: 13)),
                const SizedBox(height: 6),
                Row(children: [
                  RatingBarIndicator(
                    rating: doctor.rating,
                    itemBuilder: (_, __) => const Icon(Icons.star, color: Color(0xFFFBBC04)),
                    itemCount: 5,
                    itemSize: 14,
                  ),
                  const SizedBox(width: 4),
                  Text('(${doctor.totalReviews})',
                      style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
                  const Spacer(),
                  Text('PKR ${doctor.fee}',
                      style: const TextStyle(
                          fontWeight: FontWeight.bold, color: AppColors.primary, fontSize: 14)),
                ]),
                const SizedBox(height: 4),
                Text('\${doctor.experience} yrs experience',
                    style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
              ]),
            ),
          ]),
        ),
      );
}
"""

# ─────────────────────────────────────────────────────────────
# core/widgets/appointment_card.dart
# ─────────────────────────────────────────────────────────────
files['lib/core/widgets/appointment_card.dart'] = """import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import '../../models/appointment_model.dart';
import '../constants/app_colors.dart';
import '../utils/helpers.dart';

class AppointmentCard extends StatelessWidget {
  final AppointmentModel appointment;
  final bool isDoctor;
  final VoidCallback? onTap;
  final void Function(String status)? onStatusChange;

  const AppointmentCard({
    super.key,
    required this.appointment,
    this.isDoctor = false,
    this.onTap,
    this.onStatusChange,
  });

  @override
  Widget build(BuildContext context) {
    final statusColor = Helpers.statusColor(appointment.status);
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: AppColors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: AppColors.border, width: 0.5),
        ),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(children: [
            CircleAvatar(
              radius: 24,
              backgroundColor: AppColors.primaryLight,
              backgroundImage: (isDoctor ? appointment.patientPhotoUrl : appointment.doctorPhotoUrl).isNotEmpty
                  ? CachedNetworkImageProvider(
                      isDoctor ? appointment.patientPhotoUrl : appointment.doctorPhotoUrl)
                  : null,
              child: (isDoctor ? appointment.patientPhotoUrl : appointment.doctorPhotoUrl).isEmpty
                  ? Text(Helpers.getInitials(isDoctor ? appointment.patientName : appointment.doctorName),
                      style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold))
                  : null,
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(isDoctor ? appointment.patientName : 'Dr. \${appointment.doctorName}',
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                Text('\${appointment.date} · \${Helpers.formatTime(appointment.time)}',
                    style: const TextStyle(color: AppColors.textSecondary, fontSize: 13)),
              ]),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                color: statusColor.withOpacity(0.1),
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                appointment.status[0].toUpperCase() + appointment.status.substring(1),
                style: TextStyle(color: statusColor, fontSize: 12, fontWeight: FontWeight.w600),
              ),
            ),
          ]),
          if (isDoctor && appointment.status == 'pending') ...[
            const SizedBox(height: 12),
            const Divider(height: 1),
            const SizedBox(height: 12),
            Row(children: [
              Expanded(
                child: OutlinedButton(
                  onPressed: () => onStatusChange?.call('cancelled'),
                  style: OutlinedButton.styleFrom(
                      foregroundColor: AppColors.error,
                      side: const BorderSide(color: AppColors.error),
                      minimumSize: const Size(0, 40)),
                  child: const Text('Decline'),
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: ElevatedButton(
                  onPressed: () => onStatusChange?.call('confirmed'),
                  style: ElevatedButton.styleFrom(minimumSize: const Size(0, 40)),
                  child: const Text('Confirm'),
                ),
              ),
            ]),
          ],
        ]),
      ),
    );
  }
}
"""

# ─────────────────────────────────────────────────────────────
# models/user_model.dart
# ─────────────────────────────────────────────────────────────
files['lib/models/user_model.dart'] = """class UserModel {
  final String uid;
  final String name;
  final String email;
  final String role; // patient | doctor | admin
  final String photoUrl;
  final String phone;
  final String fcmToken;

  const UserModel({
    required this.uid,
    required this.name,
    required this.email,
    required this.role,
    this.photoUrl = '',
    this.phone = '',
    this.fcmToken = '',
  });

  factory UserModel.fromJson(Map<String, dynamic> j) => UserModel(
        uid: j['uid'] ?? '',
        name: j['name'] ?? '',
        email: j['email'] ?? '',
        role: j['role'] ?? 'patient',
        photoUrl: j['photoUrl'] ?? '',
        phone: j['phone'] ?? '',
        fcmToken: j['fcmToken'] ?? '',
      );

  Map<String, dynamic> toJson() => {
        'uid': uid,
        'name': name,
        'email': email,
        'role': role,
        'photoUrl': photoUrl,
        'phone': phone,
        'fcmToken': fcmToken,
      };

  UserModel copyWith({String? name, String? photoUrl, String? phone, String? fcmToken}) => UserModel(
        uid: uid,
        name: name ?? this.name,
        email: email,
        role: role,
        photoUrl: photoUrl ?? this.photoUrl,
        phone: phone ?? this.phone,
        fcmToken: fcmToken ?? this.fcmToken,
      );
}
"""

# ─────────────────────────────────────────────────────────────
# models/doctor_model.dart
# ─────────────────────────────────────────────────────────────
files['lib/models/doctor_model.dart'] = """class DoctorModel {
  final String uid;
  final String name;
  final String email;
  final String photoUrl;
  final String specialty;
  final String about;
  final String clinicAddress;
  final double fee;
  final double rating;
  final int totalReviews;
  final int experience;
  final bool isVerified;
  final List<String> qualifications;

  const DoctorModel({
    required this.uid,
    required this.name,
    required this.email,
    required this.specialty,
    this.photoUrl = '',
    this.about = '',
    this.clinicAddress = '',
    this.fee = 0,
    this.rating = 0,
    this.totalReviews = 0,
    this.experience = 0,
    this.isVerified = false,
    this.qualifications = const [],
  });

  factory DoctorModel.fromJson(Map<String, dynamic> j) => DoctorModel(
        uid: j['uid'] ?? '',
        name: j['name'] ?? '',
        email: j['email'] ?? '',
        specialty: j['specialty'] ?? '',
        photoUrl: j['photoUrl'] ?? '',
        about: j['about'] ?? '',
        clinicAddress: j['clinicAddress'] ?? '',
        fee: (j['fee'] ?? 0).toDouble(),
        rating: (j['rating'] ?? 0).toDouble(),
        totalReviews: j['totalReviews'] ?? 0,
        experience: j['experience'] ?? 0,
        isVerified: j['isVerified'] ?? false,
        qualifications: List<String>.from(j['qualifications'] ?? []),
      );

  Map<String, dynamic> toJson() => {
        'uid': uid,
        'name': name,
        'email': email,
        'specialty': specialty,
        'photoUrl': photoUrl,
        'about': about,
        'clinicAddress': clinicAddress,
        'fee': fee,
        'rating': rating,
        'totalReviews': totalReviews,
        'experience': experience,
        'isVerified': isVerified,
        'qualifications': qualifications,
      };
}

const List<String> kSpecialties = [
  'All',
  'General Physician',
  'Cardiologist',
  'Dermatologist',
  'Neurologist',
  'Pediatrician',
  'Orthopedic',
  'Gynecologist',
  'Psychiatrist',
  'ENT Specialist',
  'Ophthalmologist',
];
"""

# ─────────────────────────────────────────────────────────────
# models/appointment_model.dart
# ─────────────────────────────────────────────────────────────
files['lib/models/appointment_model.dart'] = """import 'package:cloud_firestore/cloud_firestore.dart';

class AppointmentModel {
  final String id;
  final String patientId;
  final String doctorId;
  final String patientName;
  final String doctorName;
  final String patientPhotoUrl;
  final String doctorPhotoUrl;
  final String date;
  final String time;
  final String status; // pending | confirmed | cancelled | completed
  final String notes;
  final DateTime createdAt;

  const AppointmentModel({
    required this.id,
    required this.patientId,
    required this.doctorId,
    required this.patientName,
    required this.doctorName,
    this.patientPhotoUrl = '',
    this.doctorPhotoUrl = '',
    required this.date,
    required this.time,
    required this.status,
    this.notes = '',
    required this.createdAt,
  });

  factory AppointmentModel.fromJson(Map<String, dynamic> j) => AppointmentModel(
        id: j['id'] ?? '',
        patientId: j['patientId'] ?? '',
        doctorId: j['doctorId'] ?? '',
        patientName: j['patientName'] ?? '',
        doctorName: j['doctorName'] ?? '',
        patientPhotoUrl: j['patientPhotoUrl'] ?? '',
        doctorPhotoUrl: j['doctorPhotoUrl'] ?? '',
        date: j['date'] ?? '',
        time: j['time'] ?? '',
        status: j['status'] ?? 'pending',
        notes: j['notes'] ?? '',
        createdAt: (j['createdAt'] as Timestamp?)?.toDate() ?? DateTime.now(),
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'patientId': patientId,
        'doctorId': doctorId,
        'patientName': patientName,
        'doctorName': doctorName,
        'patientPhotoUrl': patientPhotoUrl,
        'doctorPhotoUrl': doctorPhotoUrl,
        'date': date,
        'time': time,
        'status': status,
        'notes': notes,
        'createdAt': Timestamp.fromDate(createdAt),
      };

  AppointmentModel copyWith({String? status, String? notes}) => AppointmentModel(
        id: id,
        patientId: patientId,
        doctorId: doctorId,
        patientName: patientName,
        doctorName: doctorName,
        patientPhotoUrl: patientPhotoUrl,
        doctorPhotoUrl: doctorPhotoUrl,
        date: date,
        time: time,
        status: status ?? this.status,
        notes: notes ?? this.notes,
        createdAt: createdAt,
      );
}
"""

# ─────────────────────────────────────────────────────────────
# models/message_model.dart
# ─────────────────────────────────────────────────────────────
files['lib/models/message_model.dart'] = """import 'package:cloud_firestore/cloud_firestore.dart';

class MessageModel {
  final String id;
  final String senderId;
  final String text;
  final String imageUrl;
  final DateTime timestamp;
  final bool isRead;

  const MessageModel({
    required this.id,
    required this.senderId,
    required this.text,
    this.imageUrl = '',
    required this.timestamp,
    this.isRead = false,
  });

  factory MessageModel.fromJson(Map<String, dynamic> j, String id) => MessageModel(
        id: id,
        senderId: j['senderId'] ?? '',
        text: j['text'] ?? '',
        imageUrl: j['imageUrl'] ?? '',
        timestamp: (j['timestamp'] as Timestamp?)?.toDate() ?? DateTime.now(),
        isRead: j['isRead'] ?? false,
      );

  Map<String, dynamic> toJson() => {
        'senderId': senderId,
        'text': text,
        'imageUrl': imageUrl,
        'timestamp': Timestamp.fromDate(timestamp),
        'isRead': isRead,
      };
}

class ChatPreview {
  final String chatId;
  final String otherUserId;
  final String otherUserName;
  final String otherUserPhoto;
  final String lastMessage;
  final DateTime lastMessageTime;
  final int unreadCount;

  const ChatPreview({
    required this.chatId,
    required this.otherUserId,
    required this.otherUserName,
    this.otherUserPhoto = '',
    required this.lastMessage,
    required this.lastMessageTime,
    this.unreadCount = 0,
  });

  factory ChatPreview.fromJson(Map<String, dynamic> j, String chatId, String currentUid) {
    final participants = List<String>.from(j['participants'] ?? []);
    final otherUid = participants.firstWhere((p) => p != currentUid, orElse: () => '');
    final names = Map<String, String>.from(j['names'] ?? {});
    final photos = Map<String, String>.from(j['photos'] ?? {});
    final unread = Map<String, dynamic>.from(j['unreadCount'] ?? {});
    return ChatPreview(
      chatId: chatId,
      otherUserId: otherUid,
      otherUserName: names[otherUid] ?? 'Unknown',
      otherUserPhoto: photos[otherUid] ?? '',
      lastMessage: j['lastMessage'] ?? '',
      lastMessageTime: (j['lastMessageTime'] as dynamic)?.toDate() ?? DateTime.now(),
      unreadCount: (unread[currentUid] ?? 0) as int,
    );
  }
}
"""

# ─────────────────────────────────────────────────────────────
# services/auth_service.dart
# ─────────────────────────────────────────────────────────────
files['lib/services/auth_service.dart'] = """import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:google_sign_in/google_sign_in.dart';
import '../models/user_model.dart';

class AuthService {
  final _auth = FirebaseAuth.instance;
  final _db = FirebaseFirestore.instance;
  final _googleSignIn = GoogleSignIn();

  Future<UserModel> register({
    required String name,
    required String email,
    required String password,
    required String role,
  }) async {
    final cred = await _auth.createUserWithEmailAndPassword(
        email: email, password: password);
    await cred.user!.updateDisplayName(name);
    final user = UserModel(uid: cred.user!.uid, name: name, email: email, role: role);
    await _db.collection('users').doc(user.uid).set(user.toJson());
    return user;
  }

  Future<UserModel> login(String email, String password) async {
    final cred = await _auth.signInWithEmailAndPassword(email: email, password: password);
    final doc = await _db.collection('users').doc(cred.user!.uid).get();
    if (!doc.exists) throw Exception('User data not found');
    return UserModel.fromJson(doc.data()!);
  }

  Future<UserModel> signInWithGoogle({String role = 'patient'}) async {
    final googleUser = await _googleSignIn.signIn();
    if (googleUser == null) throw Exception('Google sign in cancelled');
    final googleAuth = await googleUser.authentication;
    final credential = GoogleAuthProvider.credential(
      accessToken: googleAuth.accessToken,
      idToken: googleAuth.idToken,
    );
    final cred = await _auth.signInWithCredential(credential);
    final uid = cred.user!.uid;
    final doc = await _db.collection('users').doc(uid).get();
    if (doc.exists) return UserModel.fromJson(doc.data()!);
    final user = UserModel(
      uid: uid,
      name: cred.user!.displayName ?? 'User',
      email: cred.user!.email ?? '',
      role: role,
      photoUrl: cred.user!.photoURL ?? '',
    );
    await _db.collection('users').doc(uid).set(user.toJson());
    return user;
  }

  Future<void> logout() async {
    await Future.wait([_auth.signOut(), _googleSignIn.signOut()]);
  }

  Future<UserModel?> getCurrentUser() async {
    final user = _auth.currentUser;
    if (user == null) return null;
    final doc = await _db.collection('users').doc(user.uid).get();
    return doc.exists ? UserModel.fromJson(doc.data()!) : null;
  }

  Stream<User?> get authStateChanges => _auth.authStateChanges();
}
"""

# ─────────────────────────────────────────────────────────────
# services/firestore_service.dart
# ─────────────────────────────────────────────────────────────
files['lib/services/firestore_service.dart'] = """import 'package:cloud_firestore/cloud_firestore.dart';
import '../models/doctor_model.dart';
import '../models/appointment_model.dart';
import '../models/message_model.dart';
import '../models/user_model.dart';

class FirestoreService {
  final _db = FirebaseFirestore.instance;

  // ── Doctors ──────────────────────────────────────────────
  Stream<List<DoctorModel>> getDoctors({String? specialty}) {
    Query<Map<String, dynamic>> q = _db.collection('doctors')
        .where('isVerified', isEqualTo: true)
        .orderBy('rating', descending: true);
    if (specialty != null && specialty != 'All') {
      q = q.where('specialty', isEqualTo: specialty);
    }
    return q.snapshots().map(
        (s) => s.docs.map((d) => DoctorModel.fromJson(d.data())).toList());
  }

  Future<DoctorModel?> getDoctor(String uid) async {
    final doc = await _db.collection('doctors').doc(uid).get();
    return doc.exists ? DoctorModel.fromJson(doc.data()!) : null;
  }

  Future<void> updateDoctorProfile(String uid, Map<String, dynamic> data) =>
      _db.collection('doctors').doc(uid).set(data, SetOptions(merge: true));

  // ── Appointments ─────────────────────────────────────────
  Stream<List<AppointmentModel>> getPatientAppointments(String patientId) =>
      _db
          .collection('appointments')
          .where('patientId', isEqualTo: patientId)
          .orderBy('createdAt', descending: true)
          .snapshots()
          .map((s) => s.docs.map((d) => AppointmentModel.fromJson(d.data())).toList());

  Stream<List<AppointmentModel>> getDoctorAppointments(String doctorId) =>
      _db
          .collection('appointments')
          .where('doctorId', isEqualTo: doctorId)
          .orderBy('createdAt', descending: true)
          .snapshots()
          .map((s) => s.docs.map((d) => AppointmentModel.fromJson(d.data())).toList());

  Future<void> bookAppointment(AppointmentModel appt) async {
    await _db.runTransaction((tx) async {
      final slotRef = _db
          .collection('doctors/\${appt.doctorId}/slots')
          .doc('\${appt.date}_\${appt.time}');
      final slot = await tx.get(slotRef);
      if (slot.exists && (slot.data()!['isBooked'] as bool? ?? false)) {
        throw Exception('Slot already booked');
      }
      tx.set(slotRef, {'isBooked': true, 'patientId': appt.patientId, 'date': appt.date, 'time': appt.time});
      final apptRef = _db.collection('appointments').doc(appt.id);
      tx.set(apptRef, appt.toJson());
    });
  }

  Future<void> updateAppointmentStatus(String id, String status) =>
      _db.collection('appointments').doc(id).update({'status': status});

  // ── Slots ────────────────────────────────────────────────
  Future<List<String>> getAvailableSlots(String doctorId, String date) async {
    final snap = await _db
        .collection('doctors/\$doctorId/slots')
        .where('date', isEqualTo: date)
        .where('isBooked', isEqualTo: false)
        .get();
    final bookedTimes = snap.docs.map((d) => d.data()['time'] as String).toSet();
    final allSlots = [
      '08:00','08:30','09:00','09:30','10:00','10:30',
      '11:00','11:30','12:00','12:30','14:00','14:30',
      '15:00','15:30','16:00','16:30','17:00','17:30',
    ];
    return allSlots.where((t) => !bookedTimes.contains(t)).toList();
  }

  Future<void> addSlot(String doctorId, String date, String time) =>
      _db.collection('doctors/\$doctorId/slots').doc('\${date}_\$time').set(
          {'date': date, 'time': time, 'isBooked': false, 'patientId': null});

  // ── Chat ─────────────────────────────────────────────────
  Stream<List<MessageModel>> getMessages(String chatId) => _db
      .collection('chats/\$chatId/messages')
      .orderBy('timestamp')
      .snapshots()
      .map((s) => s.docs.map((d) => MessageModel.fromJson(d.data(), d.id)).toList());

  Future<void> sendMessage(String chatId, MessageModel msg, {
    required String myUid, required String myName, required String myPhoto,
    required String otherUid, required String otherName, required String otherPhoto,
  }) async {
    final batch = _db.batch();
    final msgRef = _db.collection('chats/\$chatId/messages').doc();
    batch.set(msgRef, msg.toJson());
    final chatRef = _db.collection('chats').doc(chatId);
    batch.set(chatRef, {
      'participants': [myUid, otherUid],
      'names': {myUid: myName, otherUid: otherName},
      'photos': {myUid: myPhoto, otherUid: otherPhoto},
      'lastMessage': msg.text.isNotEmpty ? msg.text : '📷 Image',
      'lastMessageTime': Timestamp.fromDate(msg.timestamp),
      'unreadCount': {otherUid: FieldValue.increment(1)},
    }, SetOptions(merge: true));
    await batch.commit();
  }

  Stream<List<ChatPreview>> getChats(String uid) => _db
      .collection('chats')
      .where('participants', arrayContains: uid)
      .orderBy('lastMessageTime', descending: true)
      .snapshots()
      .map((s) => s.docs.map((d) => ChatPreview.fromJson(d.data(), d.id, uid)).toList());

  Future<void> markMessagesRead(String chatId, String uid) =>
      _db.collection('chats').doc(chatId).update({'unreadCount.\$uid': 0});

  // ── Users ────────────────────────────────────────────────
  Future<void> updateUser(String uid, Map<String, dynamic> data) =>
      _db.collection('users').doc(uid).update(data);

  Future<UserModel?> getUser(String uid) async {
    final doc = await _db.collection('users').doc(uid).get();
    return doc.exists ? UserModel.fromJson(doc.data()!) : null;
  }

  Stream<List<UserModel>> getAllUsers() => _db
      .collection('users')
      .snapshots()
      .map((s) => s.docs.map((d) => UserModel.fromJson(d.data())).toList());

  Stream<List<DoctorModel>> getAllDoctors() => _db
      .collection('doctors')
      .snapshots()
      .map((s) => s.docs.map((d) => DoctorModel.fromJson(d.data())).toList());
}
"""

# ─────────────────────────────────────────────────────────────
# services/storage_service.dart
# ─────────────────────────────────────────────────────────────
files['lib/services/storage_service.dart'] = """import 'dart:io';
import 'dart:typed_data';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:flutter/foundation.dart';
import 'package:image_picker/image_picker.dart';

class StorageService {
  final _storage = FirebaseStorage.instance;
  final _picker = ImagePicker();

  Future<XFile?> pickImage() =>
      _picker.pickImage(source: ImageSource.gallery, imageQuality: 70, maxWidth: 800);

  Future<String> uploadProfilePhoto(String uid, XFile file) async {
    final ref = _storage.ref('profile_photos/\$uid.jpg');
    UploadTask task;
    if (kIsWeb) {
      final bytes = await file.readAsBytes();
      task = ref.putData(bytes, SettableMetadata(contentType: 'image/jpeg'));
    } else {
      task = ref.putFile(File(file.path));
    }
    final snap = await task;
    return await snap.ref.getDownloadURL();
  }

  Future<String> uploadChatImage(String chatId, XFile file) async {
    final ref = _storage.ref('chat_images/\$chatId/\${DateTime.now().millisecondsSinceEpoch}.jpg');
    UploadTask task;
    if (kIsWeb) {
      final bytes = await file.readAsBytes();
      task = ref.putData(bytes, SettableMetadata(contentType: 'image/jpeg'));
    } else {
      task = ref.putFile(File(file.path));
    }
    final snap = await task;
    return await snap.ref.getDownloadURL();
  }
}
"""

# ─────────────────────────────────────────────────────────────
# providers/auth_provider.dart
# ─────────────────────────────────────────────────────────────
files['lib/providers/auth_provider.dart'] = """import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/user_model.dart';
import '../services/auth_service.dart';
import '../services/firestore_service.dart';

final authServiceProvider = Provider((ref) => AuthService());
final firestoreServiceProvider = Provider((ref) => FirestoreService());

final authStateProvider = StreamProvider<User?>((ref) {
  return ref.read(authServiceProvider).authStateChanges;
});

final currentUserProvider = FutureProvider<UserModel?>((ref) async {
  final authState = ref.watch(authStateProvider);
  return authState.when(
    data: (user) async {
      if (user == null) return null;
      return ref.read(firestoreServiceProvider).getUser(user.uid);
    },
    loading: () => null,
    error: (_, __) => null,
  );
});
"""

# ─────────────────────────────────────────────────────────────
# providers/doctor_provider.dart
# ─────────────────────────────────────────────────────────────
files['lib/providers/doctor_provider.dart'] = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/doctor_model.dart';
import 'auth_provider.dart';

final selectedSpecialtyProvider = StateProvider<String>((ref) => 'All');
final doctorSearchProvider = StateProvider<String>((ref) => '');

final doctorsProvider = StreamProvider<List<DoctorModel>>((ref) {
  ref.keepAlive();
  final specialty = ref.watch(selectedSpecialtyProvider);
  final db = ref.read(firestoreServiceProvider);
  return db.getDoctors(specialty: specialty == 'All' ? null : specialty);
});

final filteredDoctorsProvider = Provider<AsyncValue<List<DoctorModel>>>((ref) {
  final doctors = ref.watch(doctorsProvider);
  final query = ref.watch(doctorSearchProvider).toLowerCase();
  return doctors.when(
    data: (list) => AsyncData(
      query.isEmpty
          ? list
          : list.where((d) =>
              d.name.toLowerCase().contains(query) ||
              d.specialty.toLowerCase().contains(query)).toList(),
    ),
    loading: () => const AsyncLoading(),
    error: (e, s) => AsyncError(e, s),
  );
});
"""

# ─────────────────────────────────────────────────────────────
# providers/appointment_provider.dart
# ─────────────────────────────────────────────────────────────
files['lib/providers/appointment_provider.dart'] = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/appointment_model.dart';
import 'auth_provider.dart';

final patientAppointmentsProvider = StreamProvider<List<AppointmentModel>>((ref) {
  final user = ref.watch(authStateProvider).value;
  if (user == null) return const Stream.empty();
  return ref.read(firestoreServiceProvider).getPatientAppointments(user.uid);
});

final doctorAppointmentsProvider = StreamProvider<List<AppointmentModel>>((ref) {
  final user = ref.watch(authStateProvider).value;
  if (user == null) return const Stream.empty();
  return ref.read(firestoreServiceProvider).getDoctorAppointments(user.uid);
});

final selectedDateProvider = StateProvider<DateTime>((ref) => DateTime.now());
final selectedTimeProvider = StateProvider<String?>((ref) => null);
"""

# ─────────────────────────────────────────────────────────────
# providers/chat_provider.dart
# ─────────────────────────────────────────────────────────────
files['lib/providers/chat_provider.dart'] = """import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/message_model.dart';
import 'auth_provider.dart';

final chatListProvider = StreamProvider<List<ChatPreview>>((ref) {
  final user = ref.watch(authStateProvider).value;
  if (user == null) return const Stream.empty();
  return ref.read(firestoreServiceProvider).getChats(user.uid);
});

final messagesProvider = StreamProvider.family<List<MessageModel>, String>((ref, chatId) {
  return ref.read(firestoreServiceProvider).getMessages(chatId);
});
"""

# ─────────────────────────────────────────────────────────────
# features/auth/splash_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/auth/splash_screen.dart'] = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/constants/app_colors.dart';
import '../../models/user_model.dart';
import '../../providers/auth_provider.dart';

class SplashScreen extends ConsumerStatefulWidget {
  const SplashScreen({super.key});

  @override
  ConsumerState<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends ConsumerState<SplashScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _ctrl;
  late Animation<double> _fadeAnim;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 1200));
    _fadeAnim = CurvedAnimation(parent: _ctrl, curve: Curves.easeIn);
    _ctrl.forward();
    _navigate();
  }

  Future<void> _navigate() async {
    await Future.delayed(const Duration(seconds: 2));
    if (!mounted) return;
    final user = ref.read(authStateProvider).value;
    if (user == null) {
      if (mounted) context.go('/login');
      return;
    }
    final userModel = await ref.read(firestoreServiceProvider).getUser(user.uid);
    if (!mounted) return;
    _goToHome(userModel);
  }

  void _goToHome(UserModel? user) {
    if (user == null) { context.go('/login'); return; }
    switch (user.role) {
      case 'doctor': context.go('/doctor/home'); break;
      case 'admin': context.go('/admin/home'); break;
      default: context.go('/patient/home');
    }
  }

  @override
  void dispose() { _ctrl.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) => Scaffold(
        backgroundColor: AppColors.primary,
        body: FadeTransition(
          opacity: _fadeAnim,
          child: Center(
            child: Column(mainAxisSize: MainAxisSize.min, children: [
              Container(
                width: 100, height: 100,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(28),
                ),
                child: const Icon(Icons.medical_services_rounded, size: 56, color: AppColors.primary),
              ),
              const SizedBox(height: 24),
              const Text('MedConnect',
                  style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.white)),
              const SizedBox(height: 8),
              const Text('Your health, our priority',
                  style: TextStyle(color: Colors.white70, fontSize: 16)),
              const SizedBox(height: 60),
              const CircularProgressIndicator(color: Colors.white70, strokeWidth: 2),
            ]),
          ),
        ),
      );
}
"""

# ─────────────────────────────────────────────────────────────
# features/auth/login_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/auth/login_screen.dart'] = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/constants/app_colors.dart';
import '../../core/utils/helpers.dart';
import '../../core/widgets/custom_button.dart';
import '../../core/widgets/custom_text_field.dart';
import '../../models/user_model.dart';
import '../../providers/auth_provider.dart';
import '../../services/auth_service.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailCtrl = TextEditingController();
  final _passCtrl = TextEditingController();
  bool _loading = false;
  bool _obscure = true;

  @override
  void dispose() {
    _emailCtrl.dispose();
    _passCtrl.dispose();
    super.dispose();
  }

  Future<void> _login() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    try {
      final service = ref.read(authServiceProvider);
      final user = await service.login(_emailCtrl.text.trim(), _passCtrl.text);
      if (!mounted) return;
      _navigate(user);
    } catch (e) {
      if (mounted) Helpers.showSnackBar(context, 'Login failed: \${e.toString().replaceAll('Exception: ', '')}', isError: true);
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _googleLogin() async {
    setState(() => _loading = true);
    try {
      final service = ref.read(authServiceProvider);
      final user = await service.signInWithGoogle();
      if (!mounted) return;
      _navigate(user);
    } catch (e) {
      if (mounted) Helpers.showSnackBar(context, 'Google sign in failed', isError: true);
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  void _navigate(UserModel user) {
    switch (user.role) {
      case 'doctor': context.go('/doctor/home'); break;
      case 'admin': context.go('/admin/home'); break;
      default: context.go('/patient/home');
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        body: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Form(
              key: _formKey,
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                const SizedBox(height: 40),
                Container(
                  width: 64, height: 64,
                  decoration: BoxDecoration(
                    color: AppColors.primaryLight,
                    borderRadius: BorderRadius.circular(18),
                  ),
                  child: const Icon(Icons.medical_services_rounded, color: AppColors.primary, size: 36),
                ),
                const SizedBox(height: 24),
                const Text('Welcome Back!',
                    style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
                const SizedBox(height: 6),
                const Text('Sign in to continue',
                    style: TextStyle(color: AppColors.textSecondary, fontSize: 16)),
                const SizedBox(height: 40),
                AppTextField(
                  label: 'Email',
                  hint: 'Enter your email',
                  controller: _emailCtrl,
                  keyboardType: TextInputType.emailAddress,
                  prefix: const Icon(Icons.email_outlined, color: AppColors.textHint),
                  validator: (v) => (v == null || !v.contains('@')) ? 'Enter valid email' : null,
                ),
                const SizedBox(height: 16),
                AppTextField(
                  label: 'Password',
                  hint: 'Enter password',
                  controller: _passCtrl,
                  obscure: _obscure,
                  prefix: const Icon(Icons.lock_outline, color: AppColors.textHint),
                  suffix: IconButton(
                    icon: Icon(_obscure ? Icons.visibility_off : Icons.visibility, color: AppColors.textHint),
                    onPressed: () => setState(() => _obscure = !_obscure),
                  ),
                  validator: (v) => (v == null || v.length < 6) ? 'Min 6 characters' : null,
                ),
                const SizedBox(height: 8),
                Align(
                  alignment: Alignment.centerRight,
                  child: TextButton(
                    onPressed: () {},
                    child: const Text('Forgot Password?', style: TextStyle(color: AppColors.primary)),
                  ),
                ),
                const SizedBox(height: 16),
                AppButton(label: 'Sign In', loading: _loading, onTap: _login),
                const SizedBox(height: 16),
                Row(children: [
                  const Expanded(child: Divider()),
                  const Padding(padding: EdgeInsets.symmetric(horizontal: 12),
                      child: Text('OR', style: TextStyle(color: AppColors.textSecondary))),
                  const Expanded(child: Divider()),
                ]),
                const SizedBox(height: 16),
                OutlinedButton.icon(
                  onPressed: _loading ? null : _googleLogin,
                  icon: const Icon(Icons.g_mobiledata, size: 26),
                  label: const Text('Continue with Google'),
                  style: OutlinedButton.styleFrom(minimumSize: const Size(double.infinity, 52)),
                ),
                const SizedBox(height: 32),
                Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                  const Text("Don't have an account?", style: TextStyle(color: AppColors.textSecondary)),
                  TextButton(
                    onPressed: () => context.go('/register'),
                    child: const Text('Sign Up', style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold)),
                  ),
                ]),
              ]),
            ),
          ),
        ),
      );
}
"""

# ─────────────────────────────────────────────────────────────
# features/auth/register_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/auth/register_screen.dart'] = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/constants/app_colors.dart';
import '../../core/utils/helpers.dart';
import '../../core/widgets/custom_button.dart';
import '../../core/widgets/custom_text_field.dart';
import '../../providers/auth_provider.dart';

class RegisterScreen extends ConsumerStatefulWidget {
  const RegisterScreen({super.key});

  @override
  ConsumerState<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends ConsumerState<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameCtrl = TextEditingController();
  final _emailCtrl = TextEditingController();
  final _passCtrl = TextEditingController();
  final _confirmCtrl = TextEditingController();
  String _role = 'patient';
  bool _loading = false;
  bool _obscure = true;

  @override
  void dispose() {
    _nameCtrl.dispose();
    _emailCtrl.dispose();
    _passCtrl.dispose();
    _confirmCtrl.dispose();
    super.dispose();
  }

  Future<void> _register() async {
    if (!_formKey.currentState!.validate()) return;
    if (_passCtrl.text != _confirmCtrl.text) {
      Helpers.showSnackBar(context, 'Passwords do not match', isError: true);
      return;
    }
    setState(() => _loading = true);
    try {
      final service = ref.read(authServiceProvider);
      final user = await service.register(
        name: _nameCtrl.text.trim(),
        email: _emailCtrl.text.trim(),
        password: _passCtrl.text,
        role: _role,
      );
      if (!mounted) return;
      switch (user.role) {
        case 'doctor': context.go('/doctor/home'); break;
        default: context.go('/patient/home');
      }
    } catch (e) {
      if (mounted) Helpers.showSnackBar(context, 'Registration failed: \${e.toString().replaceAll('Exception: ', '')}', isError: true);
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('Create Account')),
        body: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Form(
              key: _formKey,
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                const Text('Join MedConnect',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                const SizedBox(height: 6),
                const Text('Create your account to get started',
                    style: TextStyle(color: AppColors.textSecondary)),
                const SizedBox(height: 32),
                // Role selector
                const Text('I am a', style: TextStyle(fontWeight: FontWeight.w500, fontSize: 14)),
                const SizedBox(height: 10),
                Row(children: [
                  _RoleChip(label: 'Patient', icon: Icons.person, selected: _role == 'patient',
                      onTap: () => setState(() => _role = 'patient')),
                  const SizedBox(width: 12),
                  _RoleChip(label: 'Doctor', icon: Icons.medical_services, selected: _role == 'doctor',
                      onTap: () => setState(() => _role = 'doctor')),
                ]),
                const SizedBox(height: 24),
                AppTextField(
                  label: 'Full Name',
                  hint: 'Dr. Ahmed Ali / Sarah Khan',
                  controller: _nameCtrl,
                  prefix: const Icon(Icons.person_outline, color: AppColors.textHint),
                  validator: (v) => (v == null || v.length < 2) ? 'Enter your name' : null,
                ),
                const SizedBox(height: 16),
                AppTextField(
                  label: 'Email Address',
                  hint: 'your@email.com',
                  controller: _emailCtrl,
                  keyboardType: TextInputType.emailAddress,
                  prefix: const Icon(Icons.email_outlined, color: AppColors.textHint),
                  validator: (v) => (v == null || !v.contains('@')) ? 'Enter valid email' : null,
                ),
                const SizedBox(height: 16),
                AppTextField(
                  label: 'Password',
                  hint: 'Min 6 characters',
                  controller: _passCtrl,
                  obscure: _obscure,
                  prefix: const Icon(Icons.lock_outline, color: AppColors.textHint),
                  suffix: IconButton(
                    icon: Icon(_obscure ? Icons.visibility_off : Icons.visibility, color: AppColors.textHint),
                    onPressed: () => setState(() => _obscure = !_obscure),
                  ),
                  validator: (v) => (v == null || v.length < 6) ? 'Min 6 characters' : null,
                ),
                const SizedBox(height: 16),
                AppTextField(
                  label: 'Confirm Password',
                  hint: 'Re-enter password',
                  controller: _confirmCtrl,
                  obscure: true,
                  prefix: const Icon(Icons.lock_outline, color: AppColors.textHint),
                  validator: (v) => v != _passCtrl.text ? 'Passwords do not match' : null,
                ),
                const SizedBox(height: 32),
                AppButton(label: 'Create Account', loading: _loading, onTap: _register),
                const SizedBox(height: 20),
                Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                  const Text('Already have an account?', style: TextStyle(color: AppColors.textSecondary)),
                  TextButton(
                    onPressed: () => context.go('/login'),
                    child: const Text('Sign In', style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold)),
                  ),
                ]),
              ]),
            ),
          ),
        ),
      );
}

class _RoleChip extends StatelessWidget {
  final String label;
  final IconData icon;
  final bool selected;
  final VoidCallback onTap;

  const _RoleChip({required this.label, required this.icon, required this.selected, required this.onTap});

  @override
  Widget build(BuildContext context) => GestureDetector(
        onTap: onTap,
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
          decoration: BoxDecoration(
            color: selected ? AppColors.primary : AppColors.white,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: selected ? AppColors.primary : AppColors.border),
          ),
          child: Row(mainAxisSize: MainAxisSize.min, children: [
            Icon(icon, color: selected ? Colors.white : AppColors.textSecondary, size: 20),
            const SizedBox(width: 8),
            Text(label, style: TextStyle(color: selected ? Colors.white : AppColors.textPrimary, fontWeight: FontWeight.w600)),
          ]),
        ),
      );
}
"""

# ─────────────────────────────────────────────────────────────
# features/patient/home/patient_home_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/patient/home/patient_home_screen.dart'] = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/widgets/appointment_card.dart';
import '../../../core/widgets/loading_overlay.dart';
import '../../../models/doctor_model.dart';
import '../../../providers/appointment_provider.dart';
import '../../../providers/auth_provider.dart';
import '../../../services/firestore_service.dart';

class PatientHomeScreen extends ConsumerWidget {
  const PatientHomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(currentUserProvider);
    final appointments = ref.watch(patientAppointmentsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 180,
            pinned: true,
            backgroundColor: AppColors.primary,
            flexibleSpace: FlexibleSpaceBar(
              background: Container(
                color: AppColors.primary,
                padding: const EdgeInsets.fromLTRB(24, 60, 24, 20),
                child: user.when(
                  data: (u) => Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('Good Morning,', style: TextStyle(color: Colors.white.withOpacity(0.8), fontSize: 14)),
                    const SizedBox(height: 4),
                    Text(u?.name ?? 'User', style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 4),
                    const Text('How are you feeling today?', style: TextStyle(color: Colors.white70, fontSize: 14)),
                  ]),
                  loading: () => const SizedBox.shrink(),
                  error: (_, __) => const SizedBox.shrink(),
                ),
              ),
            ),
            actions: [
              IconButton(icon: const Icon(Icons.chat_bubble_outline, color: Colors.white), onPressed: () => context.push('/chats')),
              IconButton(icon: const Icon(Icons.person_outline, color: Colors.white), onPressed: () => context.push('/patient/profile')),
            ],
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                // Specialties
                const Text('Find by Specialty', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 14),
                SizedBox(
                  height: 100,
                  child: ListView(
                    scrollDirection: Axis.horizontal,
                    children: kSpecialties.skip(1).map((s) => _SpecialtyItem(specialty: s)).toList(),
                  ),
                ),
                const SizedBox(height: 24),

                // Quick actions
                Row(children: [
                  Expanded(child: _ActionCard(icon: Icons.search, label: 'Find Doctors', color: AppColors.primary,
                      onTap: () => context.push('/patient/doctors'))),
                  const SizedBox(width: 12),
                  Expanded(child: _ActionCard(icon: Icons.calendar_today, label: 'My Appointments', color: AppColors.secondary,
                      onTap: () => context.push('/patient/appointments'))),
                ]),
                const SizedBox(height: 24),

                // Upcoming
                const Text('Upcoming Appointments', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                appointments.when(
                  data: (list) {
                    final upcoming = list.where((a) => a.status == 'confirmed' || a.status == 'pending').take(3).toList();
                    if (upcoming.isEmpty) return const EmptyState(
                      title: 'No Upcoming Appointments',
                      subtitle: 'Book your first appointment with a doctor',
                      icon: Icons.calendar_month,
                      buttonLabel: 'Find Doctors',
                    );
                    return Column(children: upcoming.map((a) => AppointmentCard(appointment: a,
                        onTap: () => context.push('/patient/appointments'))).toList());
                  },
                  loading: () => Column(children: List.generate(2, (_) => const ShimmerCard())),
                  error: (_, __) => const Center(child: Text('Error loading appointments')),
                ),
              ]),
            ),
          ),
        ],
      ),
    );
  }
}

class _SpecialtyItem extends StatelessWidget {
  final String specialty;
  const _SpecialtyItem({required this.specialty});

  @override
  Widget build(BuildContext context) {
    final colors = [AppColors.cardiology, AppColors.neurology, AppColors.pediatrics,
        AppColors.dermatology, AppColors.orthopedics, AppColors.general];
    final color = colors[specialty.hashCode % colors.length];
    return GestureDetector(
      onTap: () => context.push('/patient/doctors', extra: specialty),
      child: Container(
        width: 82,
        margin: const EdgeInsets.only(right: 12),
        decoration: BoxDecoration(
          color: color.withOpacity(0.12),
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
          Icon(Icons.medical_services, color: color, size: 28),
          const SizedBox(height: 8),
          Text(specialty.split(' ').first, textAlign: TextAlign.center,
              style: TextStyle(fontSize: 11, color: color, fontWeight: FontWeight.w600)),
        ]),
      ),
    );
  }
}

class _ActionCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;
  final VoidCallback onTap;

  const _ActionCard({required this.icon, required this.label, required this.color, required this.onTap});

  @override
  Widget build(BuildContext context) => GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: color.withOpacity(0.1),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: color.withOpacity(0.3)),
          ),
          child: Column(children: [
            Icon(icon, color: color, size: 32),
            const SizedBox(height: 8),
            Text(label, textAlign: TextAlign.center,
                style: TextStyle(color: color, fontWeight: FontWeight.w600, fontSize: 13)),
          ]),
        ),
      );
}
"""

# ─────────────────────────────────────────────────────────────
# features/patient/doctors/doctor_list_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/patient/doctors/doctor_list_screen.dart'] = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/widgets/doctor_card.dart';
import '../../../core/widgets/loading_overlay.dart';
import '../../../models/doctor_model.dart';
import '../../../providers/doctor_provider.dart';

class DoctorListScreen extends ConsumerWidget {
  const DoctorListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final specialty = ref.watch(selectedSpecialtyProvider);
    final doctors = ref.watch(filteredDoctorsProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Find Doctors')),
      body: Column(children: [
        // Search
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 8, 16, 0),
          child: TextField(
            onChanged: (v) => ref.read(doctorSearchProvider.notifier).state = v,
            decoration: InputDecoration(
              hintText: 'Search doctors by name or specialty',
              prefixIcon: const Icon(Icons.search, color: AppColors.textHint),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
            ),
          ),
        ),
        // Specialty chips
        SizedBox(
          height: 52,
          child: ListView.separated(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
            scrollDirection: Axis.horizontal,
            itemCount: kSpecialties.length,
            separatorBuilder: (_, __) => const SizedBox(width: 8),
            itemBuilder: (_, i) {
              final s = kSpecialties[i];
              final selected = specialty == s;
              return GestureDetector(
                onTap: () => ref.read(selectedSpecialtyProvider.notifier).state = s,
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 200),
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                  decoration: BoxDecoration(
                    color: selected ? AppColors.primary : AppColors.white,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: selected ? AppColors.primary : AppColors.border),
                  ),
                  child: Text(s,
                      style: TextStyle(
                          color: selected ? Colors.white : AppColors.textSecondary,
                          fontSize: 13, fontWeight: selected ? FontWeight.bold : FontWeight.normal)),
                ),
              );
            },
          ),
        ),
        // Doctor list
        Expanded(
          child: doctors.when(
            data: (list) => list.isEmpty
                ? const EmptyState(title: 'No Doctors Found', subtitle: 'Try a different specialty or search term', icon: Icons.search_off)
                : ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: list.length,
                    itemBuilder: (_, i) => DoctorCard(
                      doctor: list[i],
                      onTap: () => context.push('/patient/doctor-profile', extra: list[i]),
                    ),
                  ),
            loading: () => ListView(padding: const EdgeInsets.all(16),
                children: List.generate(5, (_) => const ShimmerCard())),
            error: (e, _) => Center(child: Text('Error: \$e')),
          ),
        ),
      ]),
    );
  }
}
"""

# ─────────────────────────────────────────────────────────────
# features/patient/doctors/doctor_profile_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/patient/doctors/doctor_profile_screen.dart'] = """import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/utils/helpers.dart';
import '../../../core/widgets/custom_button.dart';
import '../../../models/doctor_model.dart';
import '../../../providers/auth_provider.dart';

class DoctorProfileScreen extends ConsumerWidget {
  final DoctorModel doctor;
  const DoctorProfileScreen({super.key, required this.doctor});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(currentUserProvider).value;
    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 280,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              background: Stack(
                fit: StackFit.expand,
                children: [
                  if (doctor.photoUrl.isNotEmpty)
                    CachedNetworkImage(imageUrl: doctor.photoUrl, fit: BoxFit.cover)
                  else
                    Container(
                      color: AppColors.primaryLight,
                      child: const Icon(Icons.person, size: 100, color: AppColors.primary),
                    ),
                  Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topCenter, end: Alignment.bottomCenter,
                        colors: [Colors.transparent, Colors.black.withOpacity(0.7)],
                      ),
                    ),
                  ),
                  Positioned(bottom: 20, left: 20, right: 20,
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Row(children: [
                        Text('Dr. \${doctor.name}',
                            style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
                        const SizedBox(width: 8),
                        if (doctor.isVerified) const Icon(Icons.verified, color: Colors.white, size: 18),
                      ]),
                      Text(doctor.specialty, style: const TextStyle(color: Colors.white70, fontSize: 15)),
                    ]),
                  ),
                ],
              ),
            ),
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                // Stats row
                Row(children: [
                  _StatBox(icon: Icons.star, value: doctor.rating.toStringAsFixed(1), label: 'Rating', color: const Color(0xFFFBBC04)),
                  const SizedBox(width: 12),
                  _StatBox(icon: Icons.people, value: '\${doctor.totalReviews}', label: 'Reviews', color: AppColors.primary),
                  const SizedBox(width: 12),
                  _StatBox(icon: Icons.work, value: '\${doctor.experience}yr', label: 'Experience', color: AppColors.secondary),
                  const SizedBox(width: 12),
                  _StatBox(icon: Icons.payments, value: 'PKR\${doctor.fee.toInt()}', label: 'Fee', color: const Color(0xFFEA4335)),
                ]),
                const SizedBox(height: 24),
                // About
                if (doctor.about.isNotEmpty) ...[
                  const Text('About', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Text(doctor.about, style: const TextStyle(color: AppColors.textSecondary, height: 1.6)),
                  const SizedBox(height: 20),
                ],
                // Qualifications
                if (doctor.qualifications.isNotEmpty) ...[
                  const Text('Qualifications', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Wrap(spacing: 8, runSpacing: 8, children: doctor.qualifications
                      .map((q) => Chip(label: Text(q))).toList()),
                  const SizedBox(height: 20),
                ],
                // Clinic
                if (doctor.clinicAddress.isNotEmpty) ...[
                  const Text('Clinic Location', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Row(children: [
                    const Icon(Icons.location_on, color: AppColors.primary, size: 18),
                    const SizedBox(width: 6),
                    Expanded(child: Text(doctor.clinicAddress, style: const TextStyle(color: AppColors.textSecondary))),
                  ]),
                  const SizedBox(height: 24),
                ],
                // Chat button
                if (user != null) AppButton(
                  label: 'Message Doctor',
                  outline: true,
                  icon: Icons.chat_bubble_outline,
                  onTap: () {
                    final chatId = Helpers.getChatId(user.uid, doctor.uid);
                    context.push('/chat', extra: {
                      'chatId': chatId,
                      'otherUserName': 'Dr. \${doctor.name}',
                      'otherUserId': doctor.uid,
                    });
                  },
                ),
                const SizedBox(height: 12),
                AppButton(
                  label: 'Book Appointment',
                  icon: Icons.calendar_today,
                  onTap: () => context.push('/patient/book', extra: doctor),
                ),
                const SizedBox(height: 20),
              ]),
            ),
          ),
        ],
      ),
    );
  }
}

class _StatBox extends StatelessWidget {
  final IconData icon;
  final String value;
  final String label;
  final Color color;

  const _StatBox({required this.icon, required this.value, required this.label, required this.color});

  @override
  Widget build(BuildContext context) => Expanded(
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(
            color: color.withOpacity(0.1),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Column(children: [
            Icon(icon, color: color, size: 20),
            const SizedBox(height: 4),
            Text(value, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 14)),
            Text(label, style: const TextStyle(fontSize: 11, color: AppColors.textSecondary)),
          ]),
        ),
      );
}
"""

# ─────────────────────────────────────────────────────────────
# features/patient/appointments/book_appointment_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/patient/appointments/book_appointment_screen.dart'] = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:table_calendar/table_calendar.dart';
import 'package:uuid/uuid.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/utils/helpers.dart';
import '../../../core/widgets/custom_button.dart';
import '../../../models/appointment_model.dart';
import '../../../models/doctor_model.dart';
import '../../../providers/appointment_provider.dart';
import '../../../providers/auth_provider.dart';

class BookAppointmentScreen extends ConsumerStatefulWidget {
  final DoctorModel doctor;
  const BookAppointmentScreen({super.key, required this.doctor});

  @override
  ConsumerState<BookAppointmentScreen> createState() => _BookAppointmentScreenState();
}

class _BookAppointmentScreenState extends ConsumerState<BookAppointmentScreen> {
  DateTime _selectedDay = DateTime.now().add(const Duration(days: 1));
  String? _selectedTime;
  List<String> _availableSlots = [];
  bool _loadingSlots = false;
  bool _booking = false;

  @override
  void initState() {
    super.initState();
    _loadSlots();
  }

  Future<void> _loadSlots() async {
    setState(() { _loadingSlots = true; _selectedTime = null; });
    final dateStr = '\${_selectedDay.year}-\${_selectedDay.month.toString().padLeft(2, '0')}-\${_selectedDay.day.toString().padLeft(2, '0')}';
    final slots = await ref.read(firestoreServiceProvider).getAvailableSlots(widget.doctor.uid, dateStr);
    if (mounted) setState(() { _availableSlots = slots; _loadingSlots = false; });
  }

  Future<void> _book() async {
    if (_selectedTime == null) {
      Helpers.showSnackBar(context, 'Please select a time slot', isError: true);
      return;
    }
    setState(() => _booking = true);
    try {
      final user = ref.read(currentUserProvider).value!;
      final dateStr = '\${_selectedDay.year}-\${_selectedDay.month.toString().padLeft(2, '0')}-\${_selectedDay.day.toString().padLeft(2, '0')}';
      final appt = AppointmentModel(
        id: const Uuid().v4(),
        patientId: user.uid,
        doctorId: widget.doctor.uid,
        patientName: user.name,
        doctorName: widget.doctor.name,
        patientPhotoUrl: user.photoUrl,
        doctorPhotoUrl: widget.doctor.photoUrl,
        date: dateStr,
        time: _selectedTime!,
        status: 'pending',
        createdAt: DateTime.now(),
      );
      await ref.read(firestoreServiceProvider).bookAppointment(appt);
      if (!mounted) return;
      Helpers.showSnackBar(context, 'Appointment booked successfully!');
      context.go('/patient/appointments');
    } catch (e) {
      if (mounted) Helpers.showSnackBar(context, 'Booking failed: \${e.toString()}', isError: true);
    } finally {
      if (mounted) setState(() => _booking = false);
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: Text('Book · Dr. \${widget.doctor.name}')),
        body: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            // Doctor summary
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppColors.primaryLight,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Row(children: [
                CircleAvatar(
                  radius: 26,
                  backgroundColor: AppColors.primary,
                  child: Text(widget.doctor.name[0], style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                ),
                const SizedBox(width: 12),
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text('Dr. \${widget.doctor.name}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                  Text(widget.doctor.specialty, style: const TextStyle(color: AppColors.textSecondary)),
                  Text('PKR \${widget.doctor.fee.toInt()} per visit', style: const TextStyle(color: AppColors.primary, fontSize: 13)),
                ]),
              ]),
            ),
            const SizedBox(height: 24),
            const Text('Select Date', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Container(
              decoration: BoxDecoration(
                color: AppColors.white,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppColors.border, width: 0.5),
              ),
              child: TableCalendar(
                firstDay: DateTime.now(),
                lastDay: DateTime.now().add(const Duration(days: 60)),
                focusedDay: _selectedDay,
                selectedDayPredicate: (d) => isSameDay(d, _selectedDay),
                onDaySelected: (selected, focused) {
                  if (selected.weekday == DateTime.saturday || selected.weekday == DateTime.sunday) return;
                  setState(() => _selectedDay = selected);
                  _loadSlots();
                },
                enabledDayPredicate: (d) => d.weekday != DateTime.saturday && d.weekday != DateTime.sunday,
                calendarStyle: const CalendarStyle(
                  selectedDecoration: BoxDecoration(color: AppColors.primary, shape: BoxShape.circle),
                  todayDecoration: BoxDecoration(color: AppColors.primaryLight, shape: BoxShape.circle),
                  todayTextStyle: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold),
                ),
                headerStyle: const HeaderStyle(formatButtonVisible: false, titleCentered: true),
              ),
            ),
            const SizedBox(height: 24),
            const Text('Select Time', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            if (_loadingSlots)
              const Center(child: CircularProgressIndicator())
            else if (_availableSlots.isEmpty)
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(color: const Color(0xFFFEF3C7), borderRadius: BorderRadius.circular(12)),
                child: const Row(children: [
                  Icon(Icons.info, color: Color(0xFFF59E0B)),
                  SizedBox(width: 8),
                  Text('No slots available for this day. Try another date.'),
                ]),
              )
            else
              Wrap(
                spacing: 10,
                runSpacing: 10,
                children: _availableSlots.map((t) {
                  final selected = t == _selectedTime;
                  return GestureDetector(
                    onTap: () => setState(() => _selectedTime = t),
                    child: AnimatedContainer(
                      duration: const Duration(milliseconds: 200),
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                      decoration: BoxDecoration(
                        color: selected ? AppColors.primary : AppColors.white,
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(color: selected ? AppColors.primary : AppColors.border),
                      ),
                      child: Text(Helpers.formatTime(t),
                          style: TextStyle(color: selected ? Colors.white : AppColors.textPrimary,
                              fontWeight: FontWeight.w500)),
                    ),
                  );
                }).toList(),
              ),
            const SizedBox(height: 32),
            AppButton(
              label: 'Confirm Booking',
              loading: _booking,
              icon: Icons.check_circle_outline,
              onTap: _book,
            ),
            const SizedBox(height: 20),
          ]),
        ),
      );
}
"""

# ─────────────────────────────────────────────────────────────
# features/patient/appointments/patient_appointments_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/patient/appointments/patient_appointments_screen.dart'] = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/utils/helpers.dart';
import '../../../core/widgets/appointment_card.dart';
import '../../../core/widgets/loading_overlay.dart';
import '../../../models/appointment_model.dart';
import '../../../providers/appointment_provider.dart';

class PatientAppointmentsScreen extends ConsumerWidget {
  const PatientAppointmentsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final appointments = ref.watch(patientAppointmentsProvider);

    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('My Appointments'),
          bottom: const TabBar(
            labelColor: AppColors.primary,
            unselectedLabelColor: AppColors.textSecondary,
            indicatorColor: AppColors.primary,
            tabs: [Tab(text: 'Upcoming'), Tab(text: 'Completed'), Tab(text: 'Cancelled')],
          ),
        ),
        body: appointments.when(
          data: (list) => TabBarView(children: [
            _AppointmentList(appointments: list.where((a) => a.status == 'pending' || a.status == 'confirmed').toList(), context: context),
            _AppointmentList(appointments: list.where((a) => a.status == 'completed').toList(), context: context),
            _AppointmentList(appointments: list.where((a) => a.status == 'cancelled').toList(), context: context),
          ]),
          loading: () => ListView(padding: const EdgeInsets.all(16), children: List.generate(3, (_) => const ShimmerCard(height: 100))),
          error: (e, _) => Center(child: Text('Error: \$e')),
        ),
      ),
    );
  }
}

class _AppointmentList extends StatelessWidget {
  final List<AppointmentModel> appointments;
  final BuildContext context;

  const _AppointmentList({required this.appointments, required this.context});

  @override
  Widget build(BuildContext _) {
    if (appointments.isEmpty) return const EmptyState(
      title: 'No Appointments',
      subtitle: 'Your appointments will appear here',
      icon: Icons.calendar_today,
    );
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: appointments.length,
      itemBuilder: (_, i) {
        final a = appointments[i];
        return AppointmentCard(
          appointment: a,
          onTap: a.status == 'confirmed' ? () {
            context.push('/video-call', extra: {
              'appointmentId': a.id,
              'doctorName': a.doctorName,
            });
          } : null,
        );
      },
    );
  }
}
"""

# ─────────────────────────────────────────────────────────────
# features/patient/profile/patient_profile_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/patient/profile/patient_profile_screen.dart'] = """import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/utils/helpers.dart';
import '../../../core/widgets/custom_button.dart';
import '../../../core/widgets/custom_text_field.dart';
import '../../../core/widgets/loading_overlay.dart';
import '../../../providers/auth_provider.dart';
import '../../../services/auth_service.dart';
import '../../../services/firestore_service.dart';
import '../../../services/storage_service.dart';

class PatientProfileScreen extends ConsumerStatefulWidget {
  const PatientProfileScreen({super.key});

  @override
  ConsumerState<PatientProfileScreen> createState() => _PatientProfileScreenState();
}

class _PatientProfileScreenState extends ConsumerState<PatientProfileScreen> {
  final _nameCtrl = TextEditingController();
  final _phoneCtrl = TextEditingController();
  bool _editing = false;
  bool _saving = false;

  @override
  void dispose() { _nameCtrl.dispose(); _phoneCtrl.dispose(); super.dispose(); }

  Future<void> _save() async {
    setState(() => _saving = true);
    try {
      final user = ref.read(currentUserProvider).value!;
      await ref.read(firestoreServiceProvider).updateUser(user.uid, {
        'name': _nameCtrl.text.trim(),
        'phone': _phoneCtrl.text.trim(),
      });
      if (mounted) { setState(() => _editing = false); Helpers.showSnackBar(context, 'Profile updated'); }
    } catch (e) {
      if (mounted) Helpers.showSnackBar(context, 'Error: \$e', isError: true);
    } finally { if (mounted) setState(() => _saving = false); }
  }

  @override
  Widget build(BuildContext context) {
    final userAsync = ref.watch(currentUserProvider);
    return userAsync.when(
      data: (user) {
        if (user == null) return const Scaffold(body: Center(child: Text('Not logged in')));
        if (!_editing) { _nameCtrl.text = user.name; _phoneCtrl.text = user.phone; }
        return Scaffold(
          appBar: AppBar(title: const Text('My Profile'), actions: [
            IconButton(
              icon: Icon(_editing ? Icons.close : Icons.edit),
              onPressed: () => setState(() => _editing = !_editing),
            ),
          ]),
          body: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Column(children: [
              CircleAvatar(
                radius: 52,
                backgroundColor: AppColors.primaryLight,
                backgroundImage: user.photoUrl.isNotEmpty ? CachedNetworkImageProvider(user.photoUrl) : null,
                child: user.photoUrl.isEmpty
                    ? Text(Helpers.getInitials(user.name), style: const TextStyle(fontSize: 32, color: AppColors.primary, fontWeight: FontWeight.bold))
                    : null,
              ),
              const SizedBox(height: 16),
              Text(user.name, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
              Text(user.email, style: const TextStyle(color: AppColors.textSecondary)),
              Container(
                margin: const EdgeInsets.symmetric(vertical: 8),
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                decoration: BoxDecoration(color: AppColors.primaryLight, borderRadius: BorderRadius.circular(20)),
                child: Text(user.role.toUpperCase(),
                    style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 12)),
              ),
              const SizedBox(height: 24),
              if (_editing) ...[
                AppTextField(label: 'Full Name', controller: _nameCtrl),
                const SizedBox(height: 16),
                AppTextField(label: 'Phone Number', controller: _phoneCtrl, keyboardType: TextInputType.phone),
                const SizedBox(height: 24),
                AppButton(label: 'Save Changes', loading: _saving, onTap: _save),
                const SizedBox(height: 12),
              ] else ...[
                _InfoRow(icon: Icons.phone, label: 'Phone', value: user.phone.isEmpty ? 'Not set' : user.phone),
                const Divider(),
                _InfoRow(icon: Icons.email, label: 'Email', value: user.email),
                const SizedBox(height: 32),
              ],
              AppButton(
                label: 'Sign Out',
                outline: true,
                color: AppColors.error,
                icon: Icons.logout,
                onTap: () async {
                  await ref.read(authServiceProvider).logout();
                  if (mounted) context.go('/login');
                },
              ),
            ]),
          ),
        );
      },
      loading: () => const Scaffold(body: Center(child: CircularProgressIndicator())),
      error: (e, _) => Scaffold(body: Center(child: Text('Error: \$e'))),
    );
  }
}

class _InfoRow extends StatelessWidget {
  final IconData icon; final String label; final String value;
  const _InfoRow({required this.icon, required this.label, required this.value});

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.symmetric(vertical: 12),
    child: Row(children: [
      Icon(icon, color: AppColors.primary, size: 20),
      const SizedBox(width: 12),
      Text(label, style: const TextStyle(color: AppColors.textSecondary, fontSize: 14)),
      const Spacer(),
      Text(value, style: const TextStyle(fontWeight: FontWeight.w500)),
    ]),
  );
}
"""

# ─────────────────────────────────────────────────────────────
# features/doctor/home/doctor_home_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/doctor/home/doctor_home_screen.dart'] = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/utils/helpers.dart';
import '../../../core/widgets/appointment_card.dart';
import '../../../core/widgets/loading_overlay.dart';
import '../../../providers/appointment_provider.dart';
import '../../../providers/auth_provider.dart';
import '../../../services/firestore_service.dart';

class DoctorHomeScreen extends ConsumerWidget {
  const DoctorHomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(currentUserProvider);
    final appointments = ref.watch(doctorAppointmentsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 160,
            pinned: true,
            backgroundColor: AppColors.primary,
            flexibleSpace: FlexibleSpaceBar(
              background: Container(
                color: AppColors.primary,
                padding: const EdgeInsets.fromLTRB(24, 60, 24, 20),
                child: user.when(
                  data: (u) => Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    const Text('Welcome,', style: TextStyle(color: Colors.white70, fontSize: 14)),
                    Text('Dr. \${u?.name ?? ''}', style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
                    const Text('Manage your appointments', style: TextStyle(color: Colors.white70, fontSize: 13)),
                  ]),
                  loading: () => const SizedBox.shrink(),
                  error: (_, __) => const SizedBox.shrink(),
                ),
              ),
            ),
            actions: [
              IconButton(icon: const Icon(Icons.chat_bubble_outline, color: Colors.white), onPressed: () => context.push('/chats')),
              IconButton(icon: const Icon(Icons.person_outline, color: Colors.white), onPressed: () => context.push('/doctor/profile')),
            ],
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                // Stats
                appointments.when(
                  data: (list) => Row(children: [
                    _StatCard(label: 'Total', value: '\${list.length}', color: AppColors.primary, icon: Icons.calendar_month),
                    const SizedBox(width: 10),
                    _StatCard(label: 'Pending', value: '\${list.where((a) => a.status == 'pending').length}', color: AppColors.warning, icon: Icons.pending),
                    const SizedBox(width: 10),
                    _StatCard(label: 'Confirmed', value: '\${list.where((a) => a.status == 'confirmed').length}', color: AppColors.success, icon: Icons.check_circle),
                  ]),
                  loading: () => const SizedBox.shrink(),
                  error: (_, __) => const SizedBox.shrink(),
                ),
                const SizedBox(height: 20),
                // Quick actions
                Row(children: [
                  Expanded(child: _ActionBtn(icon: Icons.calendar_view_day, label: 'Appointments', onTap: () => context.push('/doctor/appointments'))),
                  const SizedBox(width: 12),
                  Expanded(child: _ActionBtn(icon: Icons.schedule, label: 'Availability', onTap: () => context.push('/doctor/availability'))),
                ]),
                const SizedBox(height: 24),
                const Text('Pending Requests', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                appointments.when(
                  data: (list) {
                    final pending = list.where((a) => a.status == 'pending').toList();
                    if (pending.isEmpty) return const EmptyState(
                      title: 'No Pending Requests',
                      subtitle: 'New appointment requests will appear here',
                      icon: Icons.inbox,
                    );
                    return Column(children: pending.take(5).map((a) => AppointmentCard(
                      appointment: a,
                      isDoctor: true,
                      onStatusChange: (status) async {
                        await ref.read(firestoreServiceProvider).updateAppointmentStatus(a.id, status);
                        if (context.mounted) Helpers.showSnackBar(context, 'Appointment \$status');
                      },
                    )).toList());
                  },
                  loading: () => Column(children: List.generate(2, (_) => const ShimmerCard(height: 100))),
                  error: (e, _) => Center(child: Text('Error: \$e')),
                ),
              ]),
            ),
          ),
        ],
      ),
    );
  }
}

class _StatCard extends StatelessWidget {
  final String label, value;
  final Color color;
  final IconData icon;

  const _StatCard({required this.label, required this.value, required this.color, required this.icon});

  @override
  Widget build(BuildContext context) => Expanded(
        child: Container(
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            color: color.withOpacity(0.1),
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: color.withOpacity(0.3)),
          ),
          child: Column(children: [
            Icon(icon, color: color, size: 22),
            const SizedBox(height: 6),
            Text(value, style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: color)),
            Text(label, style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
          ]),
        ),
      );
}

class _ActionBtn extends StatelessWidget {
  final IconData icon; final String label; final VoidCallback onTap;
  const _ActionBtn({required this.icon, required this.label, required this.onTap});

  @override
  Widget build(BuildContext context) => GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 16),
          decoration: BoxDecoration(
            color: AppColors.white,
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: AppColors.border, width: 0.5),
          ),
          child: Column(children: [
            Icon(icon, color: AppColors.primary, size: 28),
            const SizedBox(height: 8),
            Text(label, style: const TextStyle(color: AppColors.textPrimary, fontWeight: FontWeight.w500, fontSize: 13)),
          ]),
        ),
      );
}
"""

# ─────────────────────────────────────────────────────────────
# features/doctor/appointments/doctor_appointments_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/doctor/appointments/doctor_appointments_screen.dart'] = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/utils/helpers.dart';
import '../../../core/widgets/appointment_card.dart';
import '../../../core/widgets/loading_overlay.dart';
import '../../../providers/appointment_provider.dart';
import '../../../providers/auth_provider.dart';

class DoctorAppointmentsScreen extends ConsumerWidget {
  const DoctorAppointmentsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final appointments = ref.watch(doctorAppointmentsProvider);
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Appointments'),
          bottom: const TabBar(
            labelColor: AppColors.primary,
            unselectedLabelColor: AppColors.textSecondary,
            indicatorColor: AppColors.primary,
            isScrollable: true,
            tabs: [Tab(text: 'All'), Tab(text: 'Pending'), Tab(text: 'Confirmed'), Tab(text: 'Completed')],
          ),
        ),
        body: appointments.when(
          data: (list) => TabBarView(children: [
            _List(appts: list, context: context, ref: ref),
            _List(appts: list.where((a) => a.status == 'pending').toList(), context: context, ref: ref),
            _List(appts: list.where((a) => a.status == 'confirmed').toList(), context: context, ref: ref),
            _List(appts: list.where((a) => a.status == 'completed').toList(), context: context, ref: ref),
          ]),
          loading: () => ListView(padding: const EdgeInsets.all(16), children: List.generate(3, (_) => const ShimmerCard(height: 100))),
          error: (e, _) => Center(child: Text('Error: \$e')),
        ),
      ),
    );
  }
}

class _List extends StatelessWidget {
  final List appts;
  final BuildContext context;
  final WidgetRef ref;

  const _List({required this.appts, required this.context, required this.ref});

  @override
  Widget build(BuildContext context) {
    if (appts.isEmpty) return const EmptyState(title: 'No Appointments', subtitle: '', icon: Icons.calendar_today);
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: appts.length,
      itemBuilder: (_, i) => AppointmentCard(
        appointment: appts[i],
        isDoctor: true,
        onStatusChange: (status) async {
          await ref.read(firestoreServiceProvider).updateAppointmentStatus(appts[i].id, status);
          if (context.mounted) Helpers.showSnackBar(context, 'Status updated to \$status');
        },
      ),
    );
  }
}
"""

# ─────────────────────────────────────────────────────────────
# features/doctor/profile/doctor_profile_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/doctor/profile/doctor_profile_screen.dart'] = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/utils/helpers.dart';
import '../../../core/widgets/custom_button.dart';
import '../../../core/widgets/custom_text_field.dart';
import '../../../models/doctor_model.dart';
import '../../../providers/auth_provider.dart';
import '../../../services/auth_service.dart';
import '../../../services/firestore_service.dart';

class DoctorProfileScreen extends ConsumerStatefulWidget {
  const DoctorProfileScreen({super.key});

  @override
  ConsumerState<DoctorProfileScreen> createState() => _DoctorProfileScreenState();
}

class _DoctorProfileScreenState extends ConsumerState<DoctorProfileScreen> {
  final _nameCtrl = TextEditingController();
  final _aboutCtrl = TextEditingController();
  final _feeCtrl = TextEditingController();
  final _clinicCtrl = TextEditingController();
  final _expCtrl = TextEditingController();
  String _specialty = kSpecialties[1];
  bool _saving = false;

  @override
  void dispose() {
    _nameCtrl.dispose(); _aboutCtrl.dispose();
    _feeCtrl.dispose(); _clinicCtrl.dispose(); _expCtrl.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    setState(() => _saving = true);
    try {
      final user = ref.read(currentUserProvider).value!;
      await ref.read(firestoreServiceProvider).updateDoctorProfile(user.uid, {
        'uid': user.uid,
        'name': _nameCtrl.text.trim(),
        'email': user.email,
        'about': _aboutCtrl.text.trim(),
        'fee': double.tryParse(_feeCtrl.text) ?? 0,
        'clinicAddress': _clinicCtrl.text.trim(),
        'experience': int.tryParse(_expCtrl.text) ?? 0,
        'specialty': _specialty,
        'isVerified': false,
        'rating': 0.0,
        'totalReviews': 0,
        'qualifications': [],
      });
      await ref.read(firestoreServiceProvider).updateUser(user.uid, {'name': _nameCtrl.text.trim()});
      if (mounted) Helpers.showSnackBar(context, 'Profile updated!');
    } catch (e) {
      if (mounted) Helpers.showSnackBar(context, 'Error: \$e', isError: true);
    } finally { if (mounted) setState(() => _saving = false); }
  }

  @override
  Widget build(BuildContext context) {
    final user = ref.watch(currentUserProvider).value;
    if (user != null) {
      _nameCtrl.text = _nameCtrl.text.isEmpty ? user.name : _nameCtrl.text;
    }
    return Scaffold(
      appBar: AppBar(title: const Text('My Profile')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(children: [
          CircleAvatar(
            radius: 48, backgroundColor: AppColors.primaryLight,
            child: Text(Helpers.getInitials(user?.name ?? 'D'),
                style: const TextStyle(fontSize: 28, color: AppColors.primary, fontWeight: FontWeight.bold)),
          ),
          const SizedBox(height: 24),
          AppTextField(label: 'Full Name', controller: _nameCtrl, prefix: const Icon(Icons.person_outline)),
          const SizedBox(height: 16),
          Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Text('Specialty', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w500, color: Color(0xFF374151))),
            const SizedBox(height: 6),
            DropdownButtonFormField<String>(
              value: _specialty,
              items: kSpecialties.skip(1).map((s) => DropdownMenuItem(value: s, child: Text(s))).toList(),
              onChanged: (v) => setState(() => _specialty = v!),
              decoration: const InputDecoration(),
            ),
          ]),
          const SizedBox(height: 16),
          AppTextField(label: 'Years of Experience', controller: _expCtrl, keyboardType: TextInputType.number),
          const SizedBox(height: 16),
          AppTextField(label: 'Consultation Fee (PKR)', controller: _feeCtrl, keyboardType: TextInputType.number),
          const SizedBox(height: 16),
          AppTextField(label: 'Clinic Address', controller: _clinicCtrl),
          const SizedBox(height: 16),
          AppTextField(label: 'About', controller: _aboutCtrl, maxLines: 4, hint: 'Tell patients about your expertise...'),
          const SizedBox(height: 24),
          AppButton(label: 'Save Profile', loading: _saving, onTap: _save),
          const SizedBox(height: 12),
          AppButton(
            label: 'Sign Out', outline: true, color: AppColors.error, icon: Icons.logout,
            onTap: () async {
              await ref.read(authServiceProvider).logout();
              if (mounted) context.go('/login');
            },
          ),
          const SizedBox(height: 20),
        ]),
      ),
    );
  }
}
"""

# ─────────────────────────────────────────────────────────────
# features/doctor/availability/doctor_availability_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/doctor/availability/doctor_availability_screen.dart'] = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:table_calendar/table_calendar.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/utils/helpers.dart';
import '../../../core/widgets/custom_button.dart';
import '../../../providers/auth_provider.dart';

class DoctorAvailabilityScreen extends ConsumerStatefulWidget {
  const DoctorAvailabilityScreen({super.key});

  @override
  ConsumerState<DoctorAvailabilityScreen> createState() => _DoctorAvailabilityScreenState();
}

class _DoctorAvailabilityScreenState extends ConsumerState<DoctorAvailabilityScreen> {
  DateTime _focusedDay = DateTime.now();
  DateTime _selectedDay = DateTime.now().add(const Duration(days: 1));
  final Set<String> _selectedTimes = {};
  bool _saving = false;

  final _allSlots = Helpers.generateTimeSlots();

  String get _dateStr {
    final d = _selectedDay;
    return '\${d.year}-\${d.month.toString().padLeft(2, '0')}-\${d.day.toString().padLeft(2, '0')}';
  }

  Future<void> _saveSlots() async {
    if (_selectedTimes.isEmpty) {
      Helpers.showSnackBar(context, 'Select at least one time slot', isError: true);
      return;
    }
    setState(() => _saving = true);
    try {
      final uid = ref.read(authStateProvider).value!.uid;
      final db = ref.read(firestoreServiceProvider);
      for (final time in _selectedTimes) {
        await db.addSlot(uid, _dateStr, time);
      }
      if (mounted) {
        Helpers.showSnackBar(context, '\${_selectedTimes.length} slots saved for \$_dateStr!');
        setState(() => _selectedTimes.clear());
      }
    } catch (e) {
      if (mounted) Helpers.showSnackBar(context, 'Error: \$e', isError: true);
    } finally { if (mounted) setState(() => _saving = false); }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('Manage Availability')),
        body: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Text('Select Date', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            Container(
              decoration: BoxDecoration(color: AppColors.white, borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppColors.border, width: 0.5)),
              child: TableCalendar(
                firstDay: DateTime.now(),
                lastDay: DateTime.now().add(const Duration(days: 60)),
                focusedDay: _focusedDay,
                selectedDayPredicate: (d) => isSameDay(d, _selectedDay),
                onDaySelected: (selected, focused) {
                  if (selected.weekday == DateTime.saturday || selected.weekday == DateTime.sunday) return;
                  setState(() { _selectedDay = selected; _focusedDay = focused; _selectedTimes.clear(); });
                },
                enabledDayPredicate: (d) => d.weekday != DateTime.saturday && d.weekday != DateTime.sunday,
                calendarStyle: const CalendarStyle(
                  selectedDecoration: BoxDecoration(color: AppColors.primary, shape: BoxShape.circle),
                  todayDecoration: BoxDecoration(color: AppColors.primaryLight, shape: BoxShape.circle),
                  todayTextStyle: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold),
                ),
                headerStyle: const HeaderStyle(formatButtonVisible: false, titleCentered: true),
              ),
            ),
            const SizedBox(height: 20),
            Text('Select Time Slots for \$_dateStr', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            Wrap(
              spacing: 10, runSpacing: 10,
              children: _allSlots.map((t) {
                final selected = _selectedTimes.contains(t);
                return GestureDetector(
                  onTap: () => setState(() => selected ? _selectedTimes.remove(t) : _selectedTimes.add(t)),
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 150),
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                    decoration: BoxDecoration(
                      color: selected ? AppColors.primary : AppColors.white,
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: selected ? AppColors.primary : AppColors.border),
                    ),
                    child: Text(Helpers.formatTime(t),
                        style: TextStyle(color: selected ? Colors.white : AppColors.textPrimary, fontWeight: FontWeight.w500)),
                  ),
                );
              }).toList(),
            ),
            const SizedBox(height: 24),
            if (_selectedTimes.isNotEmpty)
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(color: AppColors.primaryLight, borderRadius: BorderRadius.circular(10)),
                child: Text('\${_selectedTimes.length} slots selected', style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.w600)),
              ),
            const SizedBox(height: 16),
            AppButton(label: 'Save Available Slots', loading: _saving, icon: Icons.save, onTap: _saveSlots),
          ]),
        ),
      );
}
"""

# ─────────────────────────────────────────────────────────────
# features/admin/home/admin_home_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/admin/home/admin_home_screen.dart'] = """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/utils/helpers.dart';
import '../../../core/widgets/loading_overlay.dart';
import '../../../providers/auth_provider.dart';
import '../../../services/auth_service.dart';
import '../../../services/firestore_service.dart';

class AdminHomeScreen extends ConsumerWidget {
  const AdminHomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final users = ref.watch(StreamProvider((ref) => ref.read(firestoreServiceProvider).getAllUsers()));
    final doctors = ref.watch(StreamProvider((ref) => ref.read(firestoreServiceProvider).getAllDoctors()));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Admin Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await ref.read(authServiceProvider).logout();
              if (context.mounted) context.go('/login');
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Text('Platform Overview', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          Row(children: [
            users.when(
              data: (u) => Expanded(child: _StatCard(icon: Icons.people, label: 'Total Users', value: '\${u.length}', color: AppColors.primary)),
              loading: () => const Expanded(child: ShimmerCard(height: 80)),
              error: (_, __) => const Expanded(child: SizedBox()),
            ),
            const SizedBox(width: 12),
            doctors.when(
              data: (d) => Expanded(child: _StatCard(icon: Icons.medical_services, label: 'Doctors', value: '\${d.length}', color: AppColors.secondary)),
              loading: () => const Expanded(child: ShimmerCard(height: 80)),
              error: (_, __) => const Expanded(child: SizedBox()),
            ),
          ]),
          const SizedBox(height: 24),
          const Text('Doctors', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          doctors.when(
            data: (list) => Column(children: list.map((d) => Container(
              margin: const EdgeInsets.only(bottom: 10),
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(color: AppColors.white, borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: AppColors.border, width: 0.5)),
              child: Row(children: [
                CircleAvatar(
                  backgroundColor: AppColors.primaryLight,
                  child: Text(Helpers.getInitials(d.name), style: const TextStyle(color: AppColors.primary)),
                ),
                const SizedBox(width: 12),
                Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text('Dr. \${d.name}', style: const TextStyle(fontWeight: FontWeight.bold)),
                  Text(d.specialty, style: const TextStyle(color: AppColors.textSecondary, fontSize: 13)),
                ])),
                Switch(
                  value: d.isVerified,
                  onChanged: (v) async {
                    await ref.read(firestoreServiceProvider).updateDoctorProfile(d.uid, {'isVerified': v});
                    if (context.mounted) Helpers.showSnackBar(context, v ? 'Doctor verified' : 'Verification removed');
                  },
                ),
              ]),
            )).toList()),
            loading: () => Column(children: List.generate(3, (_) => const ShimmerCard(height: 70))),
            error: (e, _) => Text('Error: \$e'),
          ),
          const SizedBox(height: 24),
          const Text('All Users', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          users.when(
            data: (list) => Column(children: list.map((u) => ListTile(
              leading: CircleAvatar(
                backgroundColor: AppColors.primaryLight,
                child: Text(Helpers.getInitials(u.name), style: const TextStyle(color: AppColors.primary)),
              ),
              title: Text(u.name),
              subtitle: Text(u.email),
              trailing: Chip(label: Text(u.role.toUpperCase()),
                  backgroundColor: u.role == 'doctor' ? AppColors.primaryLight : AppColors.secondaryLight),
            )).toList()),
            loading: () => Column(children: List.generate(3, (_) => const ShimmerCard(height: 60))),
            error: (e, _) => Text('Error: \$e'),
          ),
        ]),
      ),
    );
  }
}

class _StatCard extends StatelessWidget {
  final IconData icon; final String label, value; final Color color;
  const _StatCard({required this.icon, required this.label, required this.value, required this.color});

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.all(16),
    decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(14),
        border: Border.all(color: color.withOpacity(0.3))),
    child: Column(children: [
      Icon(icon, color: color, size: 28),
      const SizedBox(height: 8),
      Text(value, style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: color)),
      Text(label, style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
    ]),
  );
}
"""

# ─────────────────────────────────────────────────────────────
# features/chat/chat_list_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/chat/chat_list_screen.dart'] = """import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';
import '../../core/constants/app_colors.dart';
import '../../core/utils/helpers.dart';
import '../../core/widgets/loading_overlay.dart';
import '../../providers/chat_provider.dart';

class ChatListScreen extends ConsumerWidget {
  const ChatListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final chats = ref.watch(chatListProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('Messages')),
      body: chats.when(
        data: (list) => list.isEmpty
            ? const EmptyState(title: 'No Conversations', subtitle: 'Start by messaging a doctor from their profile', icon: Icons.chat_bubble_outline)
            : ListView.separated(
                itemCount: list.length,
                separatorBuilder: (_, __) => const Divider(height: 1, indent: 80),
                itemBuilder: (_, i) {
                  final chat = list[i];
                  return ListTile(
                    leading: CircleAvatar(
                      radius: 26,
                      backgroundColor: AppColors.primaryLight,
                      backgroundImage: chat.otherUserPhoto.isNotEmpty
                          ? CachedNetworkImageProvider(chat.otherUserPhoto) : null,
                      child: chat.otherUserPhoto.isEmpty
                          ? Text(Helpers.getInitials(chat.otherUserName),
                              style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold)) : null,
                    ),
                    title: Text(chat.otherUserName, style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text(chat.lastMessage, maxLines: 1, overflow: TextOverflow.ellipsis,
                        style: const TextStyle(color: AppColors.textSecondary)),
                    trailing: Column(mainAxisAlignment: MainAxisAlignment.center, crossAxisAlignment: CrossAxisAlignment.end, children: [
                      Text(DateFormat('HH:mm').format(chat.lastMessageTime),
                          style: const TextStyle(fontSize: 12, color: AppColors.textHint)),
                      if (chat.unreadCount > 0) ...[
                        const SizedBox(height: 4),
                        Container(
                          width: 20, height: 20,
                          decoration: const BoxDecoration(color: AppColors.primary, shape: BoxShape.circle),
                          child: Center(child: Text('\${chat.unreadCount}',
                              style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold))),
                        ),
                      ],
                    ]),
                    onTap: () => context.push('/chat', extra: {
                      'chatId': chat.chatId,
                      'otherUserName': chat.otherUserName,
                      'otherUserId': chat.otherUserId,
                    }),
                  );
                },
              ),
        loading: () => ListView(children: List.generate(5, (_) => const ShimmerCard(height: 70))),
        error: (e, _) => Center(child: Text('Error: \$e')),
      ),
    );
  }
}
"""

# ─────────────────────────────────────────────────────────────
# features/chat/chat_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/chat/chat_screen.dart'] = """import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../core/constants/app_colors.dart';
import '../../core/utils/helpers.dart';
import '../../models/message_model.dart';
import '../../providers/auth_provider.dart';
import '../../providers/chat_provider.dart';

class ChatScreen extends ConsumerStatefulWidget {
  final String chatId;
  final String otherUserName;
  final String otherUserId;

  const ChatScreen({
    super.key,
    required this.chatId,
    required this.otherUserName,
    required this.otherUserId,
  });

  @override
  ConsumerState<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends ConsumerState<ChatScreen> {
  final _msgCtrl = TextEditingController();
  final _scrollCtrl = ScrollController();
  bool _sending = false;

  @override
  void initState() {
    super.initState();
    // Mark messages as read
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final uid = ref.read(authStateProvider).value?.uid;
      if (uid != null) {
        ref.read(firestoreServiceProvider).markMessagesRead(widget.chatId, uid);
      }
    });
  }

  @override
  void dispose() { _msgCtrl.dispose(); _scrollCtrl.dispose(); super.dispose(); }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollCtrl.hasClients) {
        _scrollCtrl.animateTo(_scrollCtrl.position.maxScrollExtent,
            duration: const Duration(milliseconds: 300), curve: Curves.easeOut);
      }
    });
  }

  Future<void> _sendMessage() async {
    final text = _msgCtrl.text.trim();
    if (text.isEmpty) return;
    _msgCtrl.clear();
    setState(() => _sending = true);
    try {
      final user = ref.read(currentUserProvider).value!;
      final otherUser = await ref.read(firestoreServiceProvider).getUser(widget.otherUserId);
      final msg = MessageModel(
        id: '', senderId: user.uid, text: text,
        timestamp: DateTime.now(), isRead: false,
      );
      await ref.read(firestoreServiceProvider).sendMessage(
        widget.chatId, msg,
        myUid: user.uid, myName: user.name, myPhoto: user.photoUrl,
        otherUid: widget.otherUserId, otherName: otherUser?.name ?? widget.otherUserName,
        otherPhoto: otherUser?.photoUrl ?? '',
      );
      _scrollToBottom();
    } catch (e) {
      if (mounted) Helpers.showSnackBar(context, 'Failed to send: \$e', isError: true);
    } finally { if (mounted) setState(() => _sending = false); }
  }

  @override
  Widget build(BuildContext context) {
    final currentUid = ref.watch(authStateProvider).value?.uid ?? '';
    final messages = ref.watch(messagesProvider(widget.chatId));

    return Scaffold(
      appBar: AppBar(
        title: Row(children: [
          CircleAvatar(
            radius: 18, backgroundColor: AppColors.primaryLight,
            child: Text(Helpers.getInitials(widget.otherUserName),
                style: const TextStyle(color: AppColors.primary, fontSize: 14, fontWeight: FontWeight.bold)),
          ),
          const SizedBox(width: 10),
          Text(widget.otherUserName, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        ]),
      ),
      body: Column(children: [
        Expanded(
          child: messages.when(
            data: (msgs) {
              _scrollToBottom();
              if (msgs.isEmpty) return const Center(
                child: Column(mainAxisSize: MainAxisSize.min, children: [
                  Icon(Icons.chat_bubble_outline, size: 60, color: AppColors.border),
                  SizedBox(height: 12),
                  Text('No messages yet. Say hello!', style: TextStyle(color: AppColors.textSecondary)),
                ]),
              );
              return ListView.builder(
                controller: _scrollCtrl,
                padding: const EdgeInsets.all(16),
                itemCount: msgs.length,
                itemBuilder: (_, i) => _MessageBubble(msg: msgs[i], isMe: msgs[i].senderId == currentUid),
              );
            },
            loading: () => const Center(child: CircularProgressIndicator()),
            error: (e, _) => Center(child: Text('Error: \$e')),
          ),
        ),
        // Input
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
          decoration: const BoxDecoration(
            color: AppColors.white,
            border: Border(top: BorderSide(color: AppColors.border, width: 0.5)),
          ),
          child: SafeArea(
            child: Row(children: [
              Expanded(
                child: TextField(
                  controller: _msgCtrl,
                  maxLines: 4, minLines: 1,
                  textCapitalization: TextCapitalization.sentences,
                  decoration: InputDecoration(
                    hintText: 'Type a message...',
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(24), borderSide: BorderSide.none),
                    filled: true,
                    fillColor: AppColors.background,
                    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                  ),
                ),
              ),
              const SizedBox(width: 8),
              GestureDetector(
                onTap: _sending ? null : _sendMessage,
                child: Container(
                  width: 48, height: 48,
                  decoration: const BoxDecoration(color: AppColors.primary, shape: BoxShape.circle),
                  child: _sending
                      ? const Padding(padding: EdgeInsets.all(12), child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                      : const Icon(Icons.send_rounded, color: Colors.white, size: 22),
                ),
              ),
            ]),
          ),
        ),
      ]),
    );
  }
}

class _MessageBubble extends StatelessWidget {
  final MessageModel msg;
  final bool isMe;

  const _MessageBubble({required this.msg, required this.isMe});

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(bottom: 8),
        child: Row(
          mainAxisAlignment: isMe ? MainAxisAlignment.end : MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            if (!isMe) ...[
              CircleAvatar(radius: 14, backgroundColor: AppColors.primaryLight,
                  child: const Icon(Icons.person, size: 16, color: AppColors.primary)),
              const SizedBox(width: 6),
            ],
            ConstrainedBox(
              constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.7),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                decoration: BoxDecoration(
                  color: isMe ? AppColors.primary : AppColors.white,
                  borderRadius: BorderRadius.only(
                    topLeft: const Radius.circular(16),
                    topRight: const Radius.circular(16),
                    bottomLeft: Radius.circular(isMe ? 16 : 4),
                    bottomRight: Radius.circular(isMe ? 4 : 16),
                  ),
                  border: isMe ? null : Border.all(color: AppColors.border, width: 0.5),
                ),
                child: Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
                  Text(msg.text, style: TextStyle(color: isMe ? Colors.white : AppColors.textPrimary, fontSize: 15)),
                  const SizedBox(height: 4),
                  Row(mainAxisSize: MainAxisSize.min, children: [
                    Text(DateFormat('HH:mm').format(msg.timestamp),
                        style: TextStyle(fontSize: 11, color: isMe ? Colors.white70 : AppColors.textHint)),
                    if (isMe) ...[
                      const SizedBox(width: 4),
                      Icon(msg.isRead ? Icons.done_all : Icons.done,
                          size: 14, color: msg.isRead ? Colors.lightBlue[200] : Colors.white70),
                    ],
                  ]),
                ]),
              ),
            ),
          ],
        ),
      );
}
"""

# ─────────────────────────────────────────────────────────────
# features/video/video_call_screen.dart
# ─────────────────────────────────────────────────────────────
files['lib/features/video/video_call_screen.dart'] = """import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/constants/app_colors.dart';

// ----------------------------------------------------------------
// VIDEO CALL SCREEN
// Currently shows a functional UI mockup.
// To add real video: integrate agora_rtc_engine (mobile only).
// See README.md for instructions.
// ----------------------------------------------------------------

class VideoCallScreen extends ConsumerStatefulWidget {
  final String appointmentId;
  final String doctorName;

  const VideoCallScreen({super.key, required this.appointmentId, required this.doctorName});

  @override
  ConsumerState<VideoCallScreen> createState() => _VideoCallScreenState();
}

class _VideoCallScreenState extends ConsumerState<VideoCallScreen> {
  bool _muted = false;
  bool _cameraOff = false;
  bool _speakerOn = true;
  bool _connecting = true;
  Duration _elapsed = Duration.zero;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    // Simulate connection
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) setState(() => _connecting = false);
      _timer = Timer.periodic(const Duration(seconds: 1), (_) {
        if (mounted) setState(() => _elapsed += const Duration(seconds: 1));
      });
    });
  }

  @override
  void dispose() { _timer?.cancel(); super.dispose(); }

  String get _timeStr {
    final m = _elapsed.inMinutes.remainder(60).toString().padLeft(2, '0');
    final s = _elapsed.inSeconds.remainder(60).toString().padLeft(2, '0');
    return '\$m:\$s';
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        backgroundColor: const Color(0xFF1A1A2E),
        body: SafeArea(
          child: Stack(children: [
            // Remote video area (simulated)
            if (!_connecting)
              Positioned.fill(
                child: Container(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topCenter, end: Alignment.bottomCenter,
                      colors: [const Color(0xFF16213E), const Color(0xFF0F3460)],
                    ),
                  ),
                  child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                    CircleAvatar(
                      radius: 60, backgroundColor: AppColors.primaryLight,
                      child: Text(widget.doctorName[0].toUpperCase(),
                          style: const TextStyle(fontSize: 48, color: AppColors.primary, fontWeight: FontWeight.bold)),
                    ),
                    const SizedBox(height: 20),
                    Text('Dr. \${widget.doctorName}',
                        style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    Text(_timeStr, style: const TextStyle(color: Colors.white70, fontSize: 16)),
                  ]),
                ),
              )
            else
              Center(child: Column(mainAxisSize: MainAxisSize.min, children: [
                const CircularProgressIndicator(color: AppColors.primary),
                const SizedBox(height: 20),
                Text('Connecting to Dr. \${widget.doctorName}...',
                    style: const TextStyle(color: Colors.white70, fontSize: 16)),
              ])),

            // Local camera preview (top right)
            if (!_connecting && !_cameraOff)
              Positioned(
                top: 20, right: 20,
                child: Container(
                  width: 90, height: 130,
                  decoration: BoxDecoration(
                    color: AppColors.primaryDark,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: Colors.white24),
                  ),
                  child: const Center(child: Icon(Icons.person, color: Colors.white54, size: 40)),
                ),
              ),

            // Top bar
            Positioned(
              top: 0, left: 0, right: 0,
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topCenter, end: Alignment.bottomCenter,
                    colors: [Colors.black45, Colors.transparent],
                  ),
                ),
                child: Row(children: [
                  IconButton(
                    icon: const Icon(Icons.arrow_back, color: Colors.white),
                    onPressed: () => context.pop(),
                  ),
                  const Spacer(),
                  const Icon(Icons.fiber_manual_record, color: Colors.red, size: 12),
                  const SizedBox(width: 6),
                  const Text('LIVE', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                ]),
              ),
            ),

            // Bottom controls
            Positioned(
              bottom: 0, left: 0, right: 0,
              child: Container(
                padding: const EdgeInsets.fromLTRB(24, 20, 24, 32),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.bottomCenter, end: Alignment.topCenter,
                    colors: [Colors.black87, Colors.transparent],
                  ),
                ),
                child: Row(mainAxisAlignment: MainAxisAlignment.spaceEvenly, children: [
                  _CallBtn(icon: _muted ? Icons.mic_off : Icons.mic,
                      label: _muted ? 'Unmute' : 'Mute', color: _muted ? Colors.red : Colors.white54,
                      onTap: () => setState(() => _muted = !_muted)),
                  _CallBtn(icon: _cameraOff ? Icons.videocam_off : Icons.videocam,
                      label: _cameraOff ? 'Cam On' : 'Cam Off', color: _cameraOff ? Colors.red : Colors.white54,
                      onTap: () => setState(() => _cameraOff = !_cameraOff)),
                  _CallBtn(icon: Icons.call_end, label: 'End Call', color: Colors.red, size: 64,
                      onTap: () => context.pop()),
                  _CallBtn(icon: _speakerOn ? Icons.volume_up : Icons.volume_off,
                      label: 'Speaker', color: Colors.white54,
                      onTap: () => setState(() => _speakerOn = !_speakerOn)),
                  _CallBtn(icon: Icons.flip_camera_ios, label: 'Flip', color: Colors.white54,
                      onTap: () {}),
                ]),
              ),
            ),
          ]),
        ),
      );
}

class _CallBtn extends StatelessWidget {
  final IconData icon; final String label; final Color color;
  final VoidCallback onTap; final double size;

  const _CallBtn({required this.icon, required this.label, required this.color,
      required this.onTap, this.size = 52});

  @override
  Widget build(BuildContext context) => GestureDetector(
        onTap: onTap,
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Container(
            width: size, height: size,
            decoration: BoxDecoration(
              color: color == Colors.red ? Colors.red : Colors.white.withOpacity(0.15),
              shape: BoxShape.circle,
            ),
            child: Icon(icon, color: Colors.white, size: size * 0.45),
          ),
          const SizedBox(height: 6),
          Text(label, style: const TextStyle(color: Colors.white70, fontSize: 11)),
        ]),
      );
}
"""

# ─────────────────────────────────────────────────────────────
# web/index.html
# ─────────────────────────────────────────────────────────────
files['web/index.html'] = """<!DOCTYPE html>
<html>
<head>
  <base href="$FLUTTER_BASE_HREF">
  <meta charset="UTF-8">
  <meta content="IE=Edge" http-equiv="X-UA-Compatible">
  <meta name="description" content="MedConnect - Doctor Appointment App">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black">
  <meta name="apple-mobile-web-app-title" content="MedConnect">
  <link rel="apple-touch-icon" href="icons/Icon-192.png">
  <link rel="icon" type="image/png" href="favicon.png"/>
  <title>MedConnect</title>
  <link rel="manifest" href="manifest.json">
  <script>
    // Firebase config is handled by flutter/firebase_options.dart
    // This file is the standard Flutter web entry point
  </script>
</head>
<body>
  <script src="flutter_bootstrap.js" async=""></script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────
# android/app/src/main/AndroidManifest.xml additions note
# ─────────────────────────────────────────────────────────────
files['ANDROID_SETUP.md'] = """# Android Setup Notes

Add these permissions to android/app/src/main/AndroidManifest.xml
inside the <manifest> tag:

```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.RECORD_AUDIO"/>
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
```

Also ensure minSdkVersion = 21 in android/app/build.gradle:
```
defaultConfig {
    minSdkVersion 21
    targetSdkVersion 34
}
```

For Google Sign-In, add your SHA-1 fingerprint in Firebase Console:
Project Settings > Your Apps > Android app > Add fingerprint

Get SHA-1:
```
cd android && ./gradlew signingReport
```
"""

# ─────────────────────────────────────────────────────────────
# FIRESTORE_RULES.md
# ─────────────────────────────────────────────────────────────
files['FIRESTORE_RULES.md'] = """# Firestore Security Rules

Copy these rules to Firebase Console > Firestore > Rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    function isAuth() {
      return request.auth != null;
    }

    function isOwner(uid) {
      return isAuth() && request.auth.uid == uid;
    }

    function getUserRole() {
      return get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role;
    }

    function isAdmin() {
      return isAuth() && getUserRole() == 'admin';
    }

    function isDoctor() {
      return isAuth() && getUserRole() == 'doctor';
    }

    // Users collection
    match /users/{uid} {
      allow read: if isAuth();
      allow create: if isOwner(uid);
      allow update: if isOwner(uid) || isAdmin();
    }

    // Doctors collection
    match /doctors/{uid} {
      allow read: if true;
      allow create, update: if isOwner(uid) || isAdmin();
    }

    // Doctor slots subcollection
    match /doctors/{uid}/slots/{slotId} {
      allow read: if isAuth();
      allow write: if isOwner(uid) || isAdmin();
      allow update: if isAuth(); // patients need to mark as booked
    }

    // Appointments
    match /appointments/{apptId} {
      allow read: if isAuth() && (
        resource.data.patientId == request.auth.uid ||
        resource.data.doctorId == request.auth.uid ||
        isAdmin()
      );
      allow create: if isAuth();
      allow update: if isAuth() && (
        resource.data.patientId == request.auth.uid ||
        resource.data.doctorId == request.auth.uid ||
        isAdmin()
      );
    }

    // Chats
    match /chats/{chatId} {
      allow read, write: if isAuth() && request.auth.uid in resource.data.participants;
      allow create: if isAuth();

      match /messages/{msgId} {
        allow read, write: if isAuth();
      }
    }
  }
}
```
"""

# ─────────────────────────────────────────────────────────────
# Sample data seed script
# ─────────────────────────────────────────────────────────────
files['SAMPLE_DATA.md'] = """# Adding Sample Doctor Data

After setting up Firebase, add sample doctors via Firestore Console.

## Step 1: Register a Doctor Account
1. Open the app, tap Sign Up
2. Select "Doctor" role
3. Register with email (e.g. doctor@test.com)
4. Note the UID from Firebase Auth console

## Step 2: Add to doctors collection
In Firestore Console > doctors > Add document (use UID as doc ID):

```json
{
  "uid": "<doctor_uid>",
  "name": "Dr. Ahmed Khan",
  "email": "doctor@test.com",
  "specialty": "Cardiologist",
  "experience": 8,
  "fee": 1500,
  "rating": 4.7,
  "totalReviews": 124,
  "photoUrl": "",
  "about": "Expert cardiologist with 8 years experience in cardiac care.",
  "clinicAddress": "Al-Shifa Hospital, F-8/4, Islamabad",
  "isVerified": true,
  "qualifications": ["MBBS", "FCPS (Cardiology)", "MRCP"]
}
```

## Step 3: Add more sample doctors
Repeat for different specialties:
- General Physician
- Dermatologist
- Neurologist
- Pediatrician

## Step 4: Verify in Admin Panel
Login with admin role (set role: 'admin' in Firestore for your account)
and verify doctors from the Admin Dashboard.
"""

# ─────────────────────────────────────────────────────────────
# assets placeholder
# ─────────────────────────────────────────────────────────────
files['assets/images/.gitkeep'] = ""

# ─────────────────────────────────────────────────────────────
# Create zip
# ─────────────────────────────────────────────────────────────
output_path = '/home/claude/doctor_appointment_app.zip'
with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for path, content in files.items():
        zf.writestr(f'doctor_appointment_app/{path}', content)

print(f"Created {len(files)} files in {output_path}")
for p in sorted(files.keys()):
    print(f"  {p}")
