import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/foundation.dart';

// ─────────────────────────────────────────────────────────────────────────────
// FIRESTORE INIT SERVICE
// Seeds the database with required data on first run.
// ─────────────────────────────────────────────────────────────────────────────
class FirestoreInitService {
  static final FirestoreInitService _instance = FirestoreInitService._();
  factory FirestoreInitService() => _instance;
  FirestoreInitService._();

  final FirebaseFirestore _db = FirebaseFirestore.instance;

  /// Call once after Firebase is initialised (e.g. in main.dart or on login).
  /// Safe to call multiple times — skips seed data if it already exists.
  Future<void> init() async {
    try {
      await _seedSpecialties();
      await _seedSampleDoctors();
    } catch (e) {
      // Non-fatal: log and continue so the rest of the app still works.
      debugPrint('[FirestoreInitService] init error: $e');
    }
  }

  // ── Specialties ────────────────────────────────────────────────────────────

  static const List<String> _specialties = [
    'Cardiology',
    'Dermatology',
    'General Physician',
    'Neurology',
    'Ophthalmology',
    'Orthopedics',
    'Pediatrics',
    'Psychiatry',
  ];

  Future<void> _seedSpecialties() async {
    final ref = _db.collection('meta').doc('specialties');
    final snap = await ref.get();
    if (snap.exists) return;
    await ref.set({'list': _specialties, 'updatedAt': FieldValue.serverTimestamp()});
  }

  // ── Sample Doctors ─────────────────────────────────────────────────────────

  static const List<Map<String, dynamic>> _sampleDoctors = [
    {
      'uid': 'seed_doctor_001',
      'name': 'Dr. Sarah Johnson',
      'email': 'sarah.johnson@mediconnect.demo',
      'photoUrl': '',
      'specialty': 'Cardiology',
      'about': 'Board-certified cardiologist with 15 years of experience.',
      'clinicAddress': '123 Heart Ave, New York, NY',
      'experience': 15,
      'fee': 150.0,
      'rating': 4.8,
      'totalReviews': 124,
      'isVerified': true,
      'isAvailable': true,
      'availableDays': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
      'startTime': '09:00',
      'endTime': '17:00',
    },
    {
      'uid': 'seed_doctor_002',
      'name': 'Dr. Michael Chen',
      'email': 'michael.chen@mediconnect.demo',
      'photoUrl': '',
      'specialty': 'General Physician',
      'about': 'Experienced GP focused on preventive care and chronic disease management.',
      'clinicAddress': '456 Wellness Blvd, San Francisco, CA',
      'experience': 10,
      'fee': 100.0,
      'rating': 4.5,
      'totalReviews': 89,
      'isVerified': true,
      'isAvailable': true,
      'availableDays': ['Mon', 'Tue', 'Thu', 'Fri'],
      'startTime': '08:00',
      'endTime': '16:00',
    },
    {
      'uid': 'seed_doctor_003',
      'name': 'Dr. Priya Patel',
      'email': 'priya.patel@mediconnect.demo',
      'photoUrl': '',
      'specialty': 'Pediatrics',
      'about': 'Compassionate pediatrician dedicated to children\'s health and well-being.',
      'clinicAddress': '789 Kids Lane, Chicago, IL',
      'experience': 8,
      'fee': 120.0,
      'rating': 4.9,
      'totalReviews': 201,
      'isVerified': true,
      'isAvailable': true,
      'availableDays': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
      'startTime': '09:00',
      'endTime': '18:00',
    },
  ];

  Future<void> _seedSampleDoctors() async {
    for (final doctor in _sampleDoctors) {
      final ref = _db.collection('doctors').doc(doctor['uid'] as String);
      final snap = await ref.get();
      if (snap.exists) continue;
      await ref.set({
        ...doctor,
        'createdAt': FieldValue.serverTimestamp(),
      });
    }
  }
}
