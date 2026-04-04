import 'dart:io';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:flutter/foundation.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:uuid/uuid.dart';
import '../models/models.dart';

// ─────────────────────────────────────────────────────────────────────────────
// AUTH SERVICE
// ─────────────────────────────────────────────────────────────────────────────
class AuthService {
  static final AuthService _instance = AuthService._();
  factory AuthService() => _instance;
  AuthService._();

  final FirebaseAuth _auth = FirebaseAuth.instance;
  final FirebaseFirestore _db = FirebaseFirestore.instance;

  User? get currentUser => _auth.currentUser;
  Stream<User?> get authStateChanges => _auth.authStateChanges();

  Future<UserModel> signUp({
    required String name,
    required String email,
    required String password,
    required String role,
  }) async {
    final credential = await _auth.createUserWithEmailAndPassword(
      email: email.trim(),
      password: password,
    );
    await credential.user!.updateDisplayName(name);

    final user = UserModel(
      uid: credential.user!.uid,
      name: name.trim(),
      email: email.trim(),
      role: role,
      createdAt: DateTime.now(),
    );

    await _db.collection('users').doc(user.uid).set({
      ...user.toJson(),
      'createdAt': FieldValue.serverTimestamp(),
    });

    // If doctor, also create doctor document
    if (role == 'doctor') {
      final doctor = DoctorModel(
        uid: user.uid,
        name: name.trim(),
        email: email.trim(),
        specialty: 'General Physician',
      );
      await _db.collection('doctors').doc(user.uid).set({
        ...doctor.toJson(),
        'createdAt': FieldValue.serverTimestamp(),
      });
    }

    await _updateFcmToken(user.uid);
    return user;
  }

  Future<UserModel> signIn({
    required String email,
    required String password,
  }) async {
    await _auth.signInWithEmailAndPassword(
      email: email.trim(),
      password: password,
    );
    final user = await getUserById(_auth.currentUser!.uid);
    await _updateFcmToken(user.uid);
    return user;
  }

  Future<UserModel> signInWithGoogle() async {
    final googleUser = await GoogleSignIn().signIn();
    if (googleUser == null) throw Exception('Google sign-in cancelled');

    final googleAuth = await googleUser.authentication;
    final credential = GoogleAuthProvider.credential(
      accessToken: googleAuth.accessToken,
      idToken: googleAuth.idToken,
    );

    final userCred = await _auth.signInWithCredential(credential);
    final uid = userCred.user!.uid;

    // Check if user already exists
    final doc = await _db.collection('users').doc(uid).get();
    if (doc.exists) {
      final user = UserModel.fromJson(doc.data()!);
      await _updateFcmToken(uid);
      return user;
    }

    // New Google user — default role is patient
    final user = UserModel(
      uid: uid,
      name: googleUser.displayName ?? 'User',
      email: googleUser.email,
      role: 'patient',
      photoUrl: googleUser.photoUrl ?? '',
      createdAt: DateTime.now(),
    );
    await _db.collection('users').doc(uid).set({
      ...user.toJson(),
      'createdAt': FieldValue.serverTimestamp(),
    });
    await _updateFcmToken(uid);
    return user;
  }

  Future<void> signOut() async {
    await GoogleSignIn().signOut();
    await _auth.signOut();
  }

  Future<void> sendPasswordResetEmail(String email) =>
      _auth.sendPasswordResetEmail(email: email.trim());

  Future<UserModel> getUserById(String uid) async {
    final doc = await _db.collection('users').doc(uid).get();
    if (!doc.exists) throw Exception('User not found');
    return UserModel.fromJson(doc.data()!);
  }

  Future<void> updateUser(UserModel user) async {
    await _db.collection('users').doc(user.uid).update({
      'name': user.name,
      'phone': user.phone,
      'photoUrl': user.photoUrl,
    });
  }

  Future<void> _updateFcmToken(String uid) async {
    try {
      if (kIsWeb) return; // FCM token not needed for web in this demo
      final token = await FirebaseMessaging.instance.getToken();
      if (token != null) {
        await _db.collection('users').doc(uid).update({'fcmToken': token});
      }
    } catch (_) {}
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// FIRESTORE SERVICE
// ─────────────────────────────────────────────────────────────────────────────
class FirestoreService {
  static final FirestoreService _instance = FirestoreService._();
  factory FirestoreService() => _instance;
  FirestoreService._();

  final FirebaseFirestore _db = FirebaseFirestore.instance;
  final _uuid = const Uuid();

  // ─── Doctors ──────────────────────────────────────────────────────────────

  Stream<List<DoctorModel>> getDoctors({String? specialty}) {
    Query<Map<String, dynamic>> q = _db.collection('doctors')
        .where('isAvailable', isEqualTo: true)
        .orderBy('rating', descending: true);
    if (specialty != null && specialty.isNotEmpty) {
      q = q.where('specialty', isEqualTo: specialty);
    }
    return q.snapshots().map(
      (s) => s.docs.map((d) => DoctorModel.fromJson(d.data())).toList(),
    );
  }

  Future<DoctorModel?> getDoctorById(String uid) async {
    final doc = await _db.collection('doctors').doc(uid).get();
    if (!doc.exists) return null;
    return DoctorModel.fromJson(doc.data()!);
  }

  Future<void> updateDoctorProfile(String uid, Map<String, dynamic> data) =>
      _db.collection('doctors').doc(uid).update(data);

  // ─── Available Slots ──────────────────────────────────────────────────────

  Stream<List<String>> getAvailableSlots(String doctorId, String date) {
    return _db
        .collection('doctors')
        .doc(doctorId)
        .collection('slots')
        .where('date', isEqualTo: date)
        .where('isBooked', isEqualTo: false)
        .snapshots()
        .map((s) => s.docs.map((d) => d.data()['time'] as String).toList()
          ..sort());
  }

  Future<void> seedDoctorSlots(String doctorId, String date) async {
    final slots = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
                   '14:00', '14:30', '15:00', '15:30', '16:00', '16:30'];
    final batch = _db.batch();
    for (final time in slots) {
      final ref = _db.collection('doctors').doc(doctorId)
          .collection('slots').doc('${date}_$time');
      batch.set(ref, {
        'date': date,
        'time': time,
        'isBooked': false,
        'patientId': null,
      }, SetOptions(merge: true));
    }
    await batch.commit();
  }

  // ─── Appointments ─────────────────────────────────────────────────────────

  Future<String> bookAppointment({
    required String patientId,
    required String patientName,
    required String patientPhoto,
    required DoctorModel doctor,
    required String date,
    required String time,
  }) async {
    final slotRef = _db
        .collection('doctors').doc(doctor.uid)
        .collection('slots').doc('${date}_$time');

    final apptId = _uuid.v4();

    await _db.runTransaction((tx) async {
      final slot = await tx.get(slotRef);
      if (!slot.exists || (slot.data()?['isBooked'] == true)) {
        throw Exception('This slot is no longer available. Please select another time.');
      }
      // Mark slot booked
      tx.update(slotRef, {'isBooked': true, 'patientId': patientId});

      // Create appointment
      final apptRef = _db.collection('appointments').doc(apptId);
      tx.set(apptRef, {
        'id': apptId,
        'patientId': patientId,
        'patientName': patientName,
        'patientPhoto': patientPhoto,
        'doctorId': doctor.uid,
        'doctorName': doctor.name,
        'doctorSpecialty': doctor.specialty,
        'doctorPhoto': doctor.photoUrl,
        'date': date,
        'time': time,
        'status': 'pending',
        'notes': '',
        'fee': doctor.fee,
        'createdAt': FieldValue.serverTimestamp(),
      });
    });

    return apptId;
  }

  Future<void> updateAppointmentStatus(
    String appointmentId,
    AppointmentStatus status, {
    String notes = '',
  }) async {
    final data = <String, dynamic>{'status': status.name};
    if (notes.isNotEmpty) data['notes'] = notes;
    await _db.collection('appointments').doc(appointmentId).update(data);
  }

  Stream<List<AppointmentModel>> getPatientAppointments(String patientId) {
    return _db
        .collection('appointments')
        .where('patientId', isEqualTo: patientId)
        .orderBy('createdAt', descending: true)
        .snapshots()
        .map((s) => s.docs.map((d) => AppointmentModel.fromJson(d.data())).toList());
  }

  Stream<List<AppointmentModel>> getDoctorAppointments(String doctorId) {
    return _db
        .collection('appointments')
        .where('doctorId', isEqualTo: doctorId)
        .orderBy('createdAt', descending: true)
        .snapshots()
        .map((s) => s.docs.map((d) => AppointmentModel.fromJson(d.data())).toList());
  }

  Stream<List<AppointmentModel>> getAllAppointments() {
    return _db
        .collection('appointments')
        .orderBy('createdAt', descending: true)
        .snapshots()
        .map((s) => s.docs.map((d) => AppointmentModel.fromJson(d.data())).toList());
  }

  // ─── Chat ─────────────────────────────────────────────────────────────────

  String getChatId(String uid1, String uid2) {
    final sorted = [uid1, uid2]..sort();
    return '${sorted[0]}_${sorted[1]}';
  }

  Future<void> sendMessage({
    required String chatId,
    required String senderId,
    required String senderName,
    required String receiverId,
    required String receiverName,
    required String receiverPhoto,
    required String text,
    String imageUrl = '',
  }) async {
    final batch = _db.batch();
    final msgRef = _db.collection('chats').doc(chatId).collection('messages').doc();

    batch.set(msgRef, {
      'senderId': senderId,
      'senderName': senderName,
      'text': text,
      'imageUrl': imageUrl,
      'isRead': false,
      'timestamp': FieldValue.serverTimestamp(),
    });

    batch.set(_db.collection('chats').doc(chatId), {
      'participants': [senderId, receiverId],
      'lastMessage': text.isNotEmpty ? text : '📷 Image',
      'lastMessageTime': FieldValue.serverTimestamp(),
      'unreadCount': {receiverId: FieldValue.increment(1)},
      'otherUserName_$receiverId': senderName,
      'otherUserPhoto_$receiverId': '',
      'otherUserName_$senderId': receiverName,
      'otherUserPhoto_$senderId': receiverPhoto,
    }, SetOptions(merge: true));

    await batch.commit();
  }

  Stream<List<MessageModel>> getMessages(String chatId) {
    return _db
        .collection('chats').doc(chatId).collection('messages')
        .orderBy('timestamp')
        .snapshots()
        .map((s) => s.docs.map((d) => MessageModel.fromJson(d.data(), d.id)).toList());
  }

  Stream<List<ChatRoomModel>> getUserChats(String uid) {
    return _db
        .collection('chats')
        .where('participants', arrayContains: uid)
        .orderBy('lastMessageTime', descending: true)
        .snapshots()
        .map((s) => s.docs.map((d) => ChatRoomModel.fromJson(d.data(), d.id)).toList());
  }

  Future<void> markMessagesRead(String chatId, String uid) async {
    await _db.collection('chats').doc(chatId).update({
      'unreadCount.$uid': 0,
    });
    final msgs = await _db
        .collection('chats').doc(chatId).collection('messages')
        .where('isRead', isEqualTo: false)
        .where('senderId', isNotEqualTo: uid)
        .get();
    final batch = _db.batch();
    for (final doc in msgs.docs) {
      batch.update(doc.reference, {'isRead': true});
    }
    await batch.commit();
  }

  // ─── Admin ────────────────────────────────────────────────────────────────

  Stream<List<UserModel>> getAllUsers() {
    return _db.collection('users').snapshots().map(
      (s) => s.docs.map((d) => UserModel.fromJson(d.data())).toList(),
    );
  }

  Future<void> verifyDoctor(String uid, bool verified) =>
      _db.collection('doctors').doc(uid).update({'isVerified': verified});

  Future<void> toggleDoctorAvailability(String uid, bool available) =>
      _db.collection('doctors').doc(uid).update({'isAvailable': available});

  Stream<Map<String, int>> getDashboardStats() {
    return _db.collection('appointments').snapshots().map((s) {
      final all = s.docs;
      return {
        'total': all.length,
        'pending': all.where((d) => d.data()['status'] == 'pending').length,
        'confirmed': all.where((d) => d.data()['status'] == 'confirmed').length,
        'completed': all.where((d) => d.data()['status'] == 'completed').length,
      };
    });
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// STORAGE SERVICE
// ─────────────────────────────────────────────────────────────────────────────
class StorageService {
  static final StorageService _instance = StorageService._();
  factory StorageService() => _instance;
  StorageService._();

  final FirebaseStorage _storage = FirebaseStorage.instance;

  Future<String> uploadProfilePhoto(String uid, dynamic fileData) async {
    final ref = _storage.ref().child('profiles/$uid/avatar.jpg');
    UploadTask task;
    if (kIsWeb) {
      task = ref.putData(fileData as Uint8List, SettableMetadata(contentType: 'image/jpeg'));
    } else {
      task = ref.putFile(fileData as File);
    }
    final snapshot = await task;
    return snapshot.ref.getDownloadURL();
  }

  Future<String> uploadChatImage(String chatId, dynamic fileData) async {
    final uuid = const Uuid().v4();
    final ref = _storage.ref().child('chats/$chatId/$uuid.jpg');
    UploadTask task;
    if (kIsWeb) {
      task = ref.putData(fileData as Uint8List, SettableMetadata(contentType: 'image/jpeg'));
    } else {
      task = ref.putFile(fileData as File);
    }
    final snapshot = await task;
    return snapshot.ref.getDownloadURL();
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// REVIEW SERVICE
// ─────────────────────────────────────────────────────────────────────────────
class ReviewService {
  static final ReviewService _instance = ReviewService._();
  factory ReviewService() => _instance;
  ReviewService._();

  final FirebaseFirestore _db = FirebaseFirestore.instance;
  final _uuid = const Uuid();

  Future<void> submitReview({
    required String doctorId,
    required String patientId,
    required String patientName,
    required String patientPhoto,
    required double rating,
    required String comment,
  }) async {
    final reviewId = _uuid.v4();
    final batch = _db.batch();

    // Add review document
    batch.set(
      _db.collection('doctors').doc(doctorId).collection('reviews').doc(reviewId),
      {
        'doctorId': doctorId,
        'patientId': patientId,
        'patientName': patientName,
        'patientPhoto': patientPhoto,
        'rating': rating,
        'comment': comment,
        'createdAt': FieldValue.serverTimestamp(),
      },
    );

    // Update doctor's average rating
    final reviewsSnap = await _db
        .collection('doctors')
        .doc(doctorId)
        .collection('reviews')
        .get();

    final existingRatings = reviewsSnap.docs
        .map((d) => (d.data()['rating'] as num).toDouble())
        .toList()
      ..add(rating);

    final avgRating =
        existingRatings.reduce((a, b) => a + b) / existingRatings.length;

    batch.update(_db.collection('doctors').doc(doctorId), {
      'rating': double.parse(avgRating.toStringAsFixed(1)),
      'totalReviews': existingRatings.length,
    });

    await batch.commit();
  }

  Stream<List<DoctorReviewModel>> getDoctorReviews(String doctorId) {
    return _db
        .collection('doctors')
        .doc(doctorId)
        .collection('reviews')
        .orderBy('createdAt', descending: true)
        .snapshots()
        .map((s) => s.docs
            .map((d) => DoctorReviewModel.fromJson(d.data(), d.id))
            .toList());
  }

  Future<bool> hasPatientReviewed(String doctorId, String patientId) async {
    final snap = await _db
        .collection('doctors')
        .doc(doctorId)
        .collection('reviews')
        .where('patientId', isEqualTo: patientId)
        .limit(1)
        .get();
    return snap.docs.isNotEmpty;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// PRESCRIPTION SERVICE
// ─────────────────────────────────────────────────────────────────────────────
class PrescriptionService {
  static final PrescriptionService _instance = PrescriptionService._();
  factory PrescriptionService() => _instance;
  PrescriptionService._();

  final FirebaseFirestore _db = FirebaseFirestore.instance;
  final _uuid = const Uuid();

  Future<String> createPrescription({
    required String appointmentId,
    required String doctorId,
    required String doctorName,
    required String patientId,
    required String patientName,
    required List<PrescriptionItem> medicines,
    required String diagnosis,
    String notes = '',
  }) async {
    final id = _uuid.v4();
    await _db.collection('prescriptions').doc(id).set({
      'id': id,
      'appointmentId': appointmentId,
      'doctorId': doctorId,
      'doctorName': doctorName,
      'patientId': patientId,
      'patientName': patientName,
      'medicines': medicines.map((m) => m.toJson()).toList(),
      'diagnosis': diagnosis,
      'notes': notes,
      'issuedAt': FieldValue.serverTimestamp(),
    });
    return id;
  }

  Stream<List<PrescriptionModel>> getPatientPrescriptions(String patientId) {
    return _db
        .collection('prescriptions')
        .where('patientId', isEqualTo: patientId)
        .orderBy('issuedAt', descending: true)
        .snapshots()
        .map((s) => s.docs
            .map((d) => PrescriptionModel.fromJson(d.data(), d.id))
            .toList());
  }

  Stream<List<PrescriptionModel>> getDoctorPrescriptions(String doctorId) {
    return _db
        .collection('prescriptions')
        .where('doctorId', isEqualTo: doctorId)
        .orderBy('issuedAt', descending: true)
        .snapshots()
        .map((s) => s.docs
            .map((d) => PrescriptionModel.fromJson(d.data(), d.id))
            .toList());
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// NOTIFICATION SERVICE
// ─────────────────────────────────────────────────────────────────────────────
class NotificationService {
  static final NotificationService _instance = NotificationService._();
  factory NotificationService() => _instance;
  NotificationService._();

  final FirebaseFirestore _db = FirebaseFirestore.instance;
  final _uuid = const Uuid();

  Future<void> sendNotification({
    required String userId,
    required String title,
    required String body,
    required NotificationType type,
    String? relatedId,
  }) async {
    final id = _uuid.v4();
    await _db.collection('notifications').doc(id).set({
      'id': id,
      'userId': userId,
      'title': title,
      'body': body,
      'type': type.name,
      'relatedId': relatedId,
      'isRead': false,
      'createdAt': FieldValue.serverTimestamp(),
    });
  }

  Stream<List<NotificationModel>> getUserNotifications(String userId) {
    return _db
        .collection('notifications')
        .where('userId', isEqualTo: userId)
        .orderBy('createdAt', descending: true)
        .snapshots()
        .map((s) => s.docs
            .map((d) => NotificationModel.fromJson(d.data(), d.id))
            .toList());
  }

  Future<void> markAsRead(String notificationId) async {
    await _db
        .collection('notifications')
        .doc(notificationId)
        .update({'isRead': true});
  }

  Future<void> markAllAsRead(String userId) async {
    final snap = await _db
        .collection('notifications')
        .where('userId', isEqualTo: userId)
        .where('isRead', isEqualTo: false)
        .get();
    final batch = _db.batch();
    for (final doc in snap.docs) {
      batch.update(doc.reference, {'isRead': true});
    }
    await batch.commit();
  }

  Stream<int> getUnreadCount(String userId) {
    return _db
        .collection('notifications')
        .where('userId', isEqualTo: userId)
        .where('isRead', isEqualTo: false)
        .snapshots()
        .map((s) => s.docs.length);
  }
}
