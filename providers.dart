import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/models/models.dart';
import '../core/services/services.dart';

// ─── Auth Providers ───────────────────────────────────────────────────────────

final authServiceProvider = Provider<AuthService>((ref) => AuthService());
final firestoreServiceProvider = Provider<FirestoreService>((ref) => FirestoreService());
final storageServiceProvider = Provider<StorageService>((ref) => StorageService());

final authStateProvider = StreamProvider<User?>((ref) {
  return ref.read(authServiceProvider).authStateChanges;
});

final currentUserProvider = FutureProvider<UserModel?>((ref) async {
  final user = ref.watch(authStateProvider).value;
  if (user == null) return null;
  try {
    return await ref.read(authServiceProvider).getUserById(user.uid);
  } catch (_) {
    return null;
  }
});

// ─── Doctor Providers ─────────────────────────────────────────────────────────

final specialtyFilterProvider = StateProvider<String?>((ref) => null);

final doctorsProvider = StreamProvider<List<DoctorModel>>((ref) {
  ref.keepAlive();
  final specialty = ref.watch(specialtyFilterProvider);
  return ref.read(firestoreServiceProvider).getDoctors(specialty: specialty);
});

final doctorByIdProvider = FutureProvider.family<DoctorModel?, String>((ref, uid) async {
  return ref.read(firestoreServiceProvider).getDoctorById(uid);
});

final availableSlotsProvider = StreamProvider.family<List<String>, ({String doctorId, String date})>(
  (ref, args) {
    return ref.read(firestoreServiceProvider).getAvailableSlots(args.doctorId, args.date);
  },
);

// ─── Appointment Providers ────────────────────────────────────────────────────

final patientAppointmentsProvider = StreamProvider.family<List<AppointmentModel>, String>(
  (ref, patientId) {
    return ref.read(firestoreServiceProvider).getPatientAppointments(patientId);
  },
);

final doctorAppointmentsProvider = StreamProvider.family<List<AppointmentModel>, String>(
  (ref, doctorId) {
    return ref.read(firestoreServiceProvider).getDoctorAppointments(doctorId);
  },
);

final allAppointmentsProvider = StreamProvider<List<AppointmentModel>>((ref) {
  return ref.read(firestoreServiceProvider).getAllAppointments();
});

// ─── Chat Providers ───────────────────────────────────────────────────────────

final userChatsProvider = StreamProvider.family<List<ChatRoomModel>, String>(
  (ref, uid) {
    return ref.read(firestoreServiceProvider).getUserChats(uid);
  },
);

final messagesProvider = StreamProvider.family<List<MessageModel>, String>(
  (ref, chatId) {
    return ref.read(firestoreServiceProvider).getMessages(chatId);
  },
);

// ─── Admin Providers ──────────────────────────────────────────────────────────

final allUsersProvider = StreamProvider<List<UserModel>>((ref) {
  return ref.read(firestoreServiceProvider).getAllUsers();
});

final dashboardStatsProvider = StreamProvider<Map<String, int>>((ref) {
  return ref.read(firestoreServiceProvider).getDashboardStats();
});

// ─── Search Provider ──────────────────────────────────────────────────────────

final searchQueryProvider = StateProvider<String>((ref) => '');
