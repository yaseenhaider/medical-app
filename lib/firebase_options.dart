// IMPORTANT: Run `flutterfire configure` in your project directory
// to auto-generate this file with your Firebase project credentials.
// 
// Steps:
//   1. Install FlutterFire CLI:  dart pub global activate flutterfire_cli
//   2. Run: flutterfire configure
//   3. Select your Firebase project
//   4. This file will be replaced with your real credentials
//
// OR manually fill in the values from your Firebase Console.

import 'package:firebase_core/firebase_core.dart' show FirebaseOptions;
import 'package:flutter/foundation.dart'
    show defaultTargetPlatform, kIsWeb, TargetPlatform;

class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) {
      throw UnsupportedError(
        'DefaultFirebaseOptions have not been configured for web. '
        'Run flutterfire configure.',
      );
    }
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return android;
      case TargetPlatform.iOS:
        throw UnsupportedError(
          'DefaultFirebaseOptions have not been configured for ios. '
          'Run flutterfire configure.',
        );
      default:
        return android;
    }
  }

  static const FirebaseOptions android = FirebaseOptions(
    apiKey: 'AIzaSyAcqz2GHeTmPWdArSDtRYcfvwzOxFbUs6E',
    appId: '1:549861900070:android:2b5fe54ee9c602b0b74be7',
    messagingSenderId: '549861900070',
    projectId: 'medical-app-fdd22',
    databaseURL: 'https://medical-app-fdd22-default-rtdb.asia-southeast1.firebasedatabase.app',
    storageBucket: 'medical-app-fdd22.firebasestorage.app',
  );

}
