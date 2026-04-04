// ─────────────────────────────────────────────────────────────────────────────
// USER MODEL
// ─────────────────────────────────────────────────────────────────────────────
class UserModel {
  final String uid;
  final String name;
  final String email;
  final String role; // 'patient' | 'doctor' | 'admin'
  final String photoUrl;
  final String phone;
  final String fcmToken;
  final DateTime createdAt;

  const UserModel({
    required this.uid,
    required this.name,
    required this.email,
    required this.role,
    this.photoUrl = '',
    this.phone = '',
    this.fcmToken = '',
    required this.createdAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) => UserModel(
    uid: json['uid'] ?? '',
    name: json['name'] ?? '',
    email: json['email'] ?? '',
    role: json['role'] ?? 'patient',
    photoUrl: json['photoUrl'] ?? '',
    phone: json['phone'] ?? '',
    fcmToken: json['fcmToken'] ?? '',
    createdAt: json['createdAt'] != null
        ? (json['createdAt'] as dynamic).toDate()
        : DateTime.now(),
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

  UserModel copyWith({
    String? name,
    String? photoUrl,
    String? phone,
    String? fcmToken,
  }) => UserModel(
    uid: uid,
    name: name ?? this.name,
    email: email,
    role: role,
    photoUrl: photoUrl ?? this.photoUrl,
    phone: phone ?? this.phone,
    fcmToken: fcmToken ?? this.fcmToken,
    createdAt: createdAt,
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// DOCTOR MODEL
// ─────────────────────────────────────────────────────────────────────────────
class DoctorModel {
  final String uid;
  final String name;
  final String email;
  final String photoUrl;
  final String specialty;
  final String about;
  final String clinicAddress;
  final int experience;
  final double fee;
  final double rating;
  final int totalReviews;
  final bool isVerified;
  final bool isAvailable;
  final List<String> availableDays;
  final String startTime;
  final String endTime;

  const DoctorModel({
    required this.uid,
    required this.name,
    required this.email,
    this.photoUrl = '',
    required this.specialty,
    this.about = '',
    this.clinicAddress = '',
    this.experience = 0,
    this.fee = 0,
    this.rating = 0,
    this.totalReviews = 0,
    this.isVerified = false,
    this.isAvailable = true,
    this.availableDays = const ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    this.startTime = '09:00',
    this.endTime = '17:00',
  });

  factory DoctorModel.fromJson(Map<String, dynamic> json) => DoctorModel(
    uid: json['uid'] ?? '',
    name: json['name'] ?? '',
    email: json['email'] ?? '',
    photoUrl: json['photoUrl'] ?? '',
    specialty: json['specialty'] ?? '',
    about: json['about'] ?? '',
    clinicAddress: json['clinicAddress'] ?? '',
    experience: (json['experience'] ?? 0).toInt(),
    fee: (json['fee'] ?? 0).toDouble(),
    rating: (json['rating'] ?? 0).toDouble(),
    totalReviews: (json['totalReviews'] ?? 0).toInt(),
    isVerified: json['isVerified'] ?? false,
    isAvailable: json['isAvailable'] ?? true,
    availableDays: List<String>.from(json['availableDays'] ?? ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']),
    startTime: json['startTime'] ?? '09:00',
    endTime: json['endTime'] ?? '17:00',
  );

  Map<String, dynamic> toJson() => {
    'uid': uid,
    'name': name,
    'email': email,
    'photoUrl': photoUrl,
    'specialty': specialty,
    'about': about,
    'clinicAddress': clinicAddress,
    'experience': experience,
    'fee': fee,
    'rating': rating,
    'totalReviews': totalReviews,
    'isVerified': isVerified,
    'isAvailable': isAvailable,
    'availableDays': availableDays,
    'startTime': startTime,
    'endTime': endTime,
  };

  DoctorModel copyWith({
    String? photoUrl,
    String? about,
    String? clinicAddress,
    bool? isVerified,
    bool? isAvailable,
    double? rating,
    int? totalReviews,
  }) => DoctorModel(
    uid: uid, name: name, email: email,
    photoUrl: photoUrl ?? this.photoUrl,
    specialty: specialty,
    about: about ?? this.about,
    clinicAddress: clinicAddress ?? this.clinicAddress,
    experience: experience, fee: fee,
    rating: rating ?? this.rating,
    totalReviews: totalReviews ?? this.totalReviews,
    isVerified: isVerified ?? this.isVerified,
    isAvailable: isAvailable ?? this.isAvailable,
    availableDays: availableDays,
    startTime: startTime, endTime: endTime,
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// APPOINTMENT MODEL
// ─────────────────────────────────────────────────────────────────────────────
enum AppointmentStatus { pending, confirmed, completed, cancelled }

class AppointmentModel {
  final String id;
  final String patientId;
  final String patientName;
  final String patientPhoto;
  final String doctorId;
  final String doctorName;
  final String doctorSpecialty;
  final String doctorPhoto;
  final String date;       // 'YYYY-MM-DD'
  final String time;       // 'HH:mm'
  final AppointmentStatus status;
  final String notes;
  final double fee;
  final DateTime createdAt;

  const AppointmentModel({
    required this.id,
    required this.patientId,
    required this.patientName,
    this.patientPhoto = '',
    required this.doctorId,
    required this.doctorName,
    this.doctorSpecialty = '',
    this.doctorPhoto = '',
    required this.date,
    required this.time,
    this.status = AppointmentStatus.pending,
    this.notes = '',
    this.fee = 0,
    required this.createdAt,
  });

  factory AppointmentModel.fromJson(Map<String, dynamic> json) => AppointmentModel(
    id: json['id'] ?? '',
    patientId: json['patientId'] ?? '',
    patientName: json['patientName'] ?? '',
    patientPhoto: json['patientPhoto'] ?? '',
    doctorId: json['doctorId'] ?? '',
    doctorName: json['doctorName'] ?? '',
    doctorSpecialty: json['doctorSpecialty'] ?? '',
    doctorPhoto: json['doctorPhoto'] ?? '',
    date: json['date'] ?? '',
    time: json['time'] ?? '',
    status: _statusFromString(json['status'] ?? 'pending'),
    notes: json['notes'] ?? '',
    fee: (json['fee'] ?? 0).toDouble(),
    createdAt: json['createdAt'] != null
        ? (json['createdAt'] as dynamic).toDate()
        : DateTime.now(),
  );

  static AppointmentStatus _statusFromString(String s) {
    switch (s) {
      case 'confirmed': return AppointmentStatus.confirmed;
      case 'completed': return AppointmentStatus.completed;
      case 'cancelled': return AppointmentStatus.cancelled;
      default: return AppointmentStatus.pending;
    }
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'patientId': patientId,
    'patientName': patientName,
    'patientPhoto': patientPhoto,
    'doctorId': doctorId,
    'doctorName': doctorName,
    'doctorSpecialty': doctorSpecialty,
    'doctorPhoto': doctorPhoto,
    'date': date,
    'time': time,
    'status': status.name,
    'notes': notes,
    'fee': fee,
  };

  AppointmentModel copyWith({AppointmentStatus? status, String? notes}) =>
      AppointmentModel(
        id: id, patientId: patientId, patientName: patientName,
        patientPhoto: patientPhoto, doctorId: doctorId, doctorName: doctorName,
        doctorSpecialty: doctorSpecialty, doctorPhoto: doctorPhoto,
        date: date, time: time,
        status: status ?? this.status,
        notes: notes ?? this.notes,
        fee: fee, createdAt: createdAt,
      );
}

// ─────────────────────────────────────────────────────────────────────────────
// MESSAGE MODEL
// ─────────────────────────────────────────────────────────────────────────────
class MessageModel {
  final String id;
  final String senderId;
  final String senderName;
  final String text;
  final String imageUrl;
  final DateTime timestamp;
  final bool isRead;

  const MessageModel({
    required this.id,
    required this.senderId,
    this.senderName = '',
    required this.text,
    this.imageUrl = '',
    required this.timestamp,
    this.isRead = false,
  });

  factory MessageModel.fromJson(Map<String, dynamic> json, String id) => MessageModel(
    id: id,
    senderId: json['senderId'] ?? '',
    senderName: json['senderName'] ?? '',
    text: json['text'] ?? '',
    imageUrl: json['imageUrl'] ?? '',
    timestamp: json['timestamp'] != null
        ? (json['timestamp'] as dynamic).toDate()
        : DateTime.now(),
    isRead: json['isRead'] ?? false,
  );

  Map<String, dynamic> toJson() => {
    'senderId': senderId,
    'senderName': senderName,
    'text': text,
    'imageUrl': imageUrl,
    'isRead': isRead,
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// CHAT ROOM MODEL
// ─────────────────────────────────────────────────────────────────────────────
class ChatRoomModel {
  final String chatId;
  final List<String> participants;
  final String lastMessage;
  final DateTime? lastMessageTime;
  final Map<String, int> unreadCount;
  final String otherUserName;
  final String otherUserPhoto;

  const ChatRoomModel({
    required this.chatId,
    required this.participants,
    this.lastMessage = '',
    this.lastMessageTime,
    this.unreadCount = const {},
    this.otherUserName = '',
    this.otherUserPhoto = '',
  });

  factory ChatRoomModel.fromJson(Map<String, dynamic> json, String chatId) => ChatRoomModel(
    chatId: chatId,
    participants: List<String>.from(json['participants'] ?? []),
    lastMessage: json['lastMessage'] ?? '',
    lastMessageTime: json['lastMessageTime'] != null
        ? (json['lastMessageTime'] as dynamic).toDate()
        : null,
    unreadCount: Map<String, int>.from(json['unreadCount'] ?? {}),
    otherUserName: json['otherUserName'] ?? '',
    otherUserPhoto: json['otherUserPhoto'] ?? '',
  );

  Map<String, dynamic> toJson() => {
    'participants': participants,
    'lastMessage': lastMessage,
    'unreadCount': unreadCount,
    'otherUserName': otherUserName,
    'otherUserPhoto': otherUserPhoto,
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// DOCTOR REVIEW MODEL
// ─────────────────────────────────────────────────────────────────────────────
class DoctorReviewModel {
  final String id;
  final String doctorId;
  final String patientId;
  final String patientName;
  final String patientPhoto;
  final double rating;
  final String comment;
  final DateTime createdAt;

  const DoctorReviewModel({
    required this.id,
    required this.doctorId,
    required this.patientId,
    required this.patientName,
    this.patientPhoto = '',
    required this.rating,
    this.comment = '',
    required this.createdAt,
  });

  factory DoctorReviewModel.fromJson(Map<String, dynamic> json, String id) =>
      DoctorReviewModel(
        id: id,
        doctorId: json['doctorId'] ?? '',
        patientId: json['patientId'] ?? '',
        patientName: json['patientName'] ?? '',
        patientPhoto: json['patientPhoto'] ?? '',
        rating: (json['rating'] ?? 0).toDouble(),
        comment: json['comment'] ?? '',
        createdAt: json['createdAt'] != null
            ? (json['createdAt'] as dynamic).toDate()
            : DateTime.now(),
      );

  Map<String, dynamic> toJson() => {
        'doctorId': doctorId,
        'patientId': patientId,
        'patientName': patientName,
        'patientPhoto': patientPhoto,
        'rating': rating,
        'comment': comment,
      };
}

// ─────────────────────────────────────────────────────────────────────────────
// PRESCRIPTION MODEL
// ─────────────────────────────────────────────────────────────────────────────
class PrescriptionModel {
  final String id;
  final String appointmentId;
  final String doctorId;
  final String doctorName;
  final String patientId;
  final String patientName;
  final List<PrescriptionItem> medicines;
  final String diagnosis;
  final String notes;
  final DateTime issuedAt;

  const PrescriptionModel({
    required this.id,
    required this.appointmentId,
    required this.doctorId,
    required this.doctorName,
    required this.patientId,
    required this.patientName,
    this.medicines = const [],
    this.diagnosis = '',
    this.notes = '',
    required this.issuedAt,
  });

  factory PrescriptionModel.fromJson(Map<String, dynamic> json, String id) =>
      PrescriptionModel(
        id: id,
        appointmentId: json['appointmentId'] ?? '',
        doctorId: json['doctorId'] ?? '',
        doctorName: json['doctorName'] ?? '',
        patientId: json['patientId'] ?? '',
        patientName: json['patientName'] ?? '',
        medicines: (json['medicines'] as List<dynamic>? ?? [])
            .map((m) => PrescriptionItem.fromJson(m as Map<String, dynamic>))
            .toList(),
        diagnosis: json['diagnosis'] ?? '',
        notes: json['notes'] ?? '',
        issuedAt: json['issuedAt'] != null
            ? (json['issuedAt'] as dynamic).toDate()
            : DateTime.now(),
      );

  Map<String, dynamic> toJson() => {
        'appointmentId': appointmentId,
        'doctorId': doctorId,
        'doctorName': doctorName,
        'patientId': patientId,
        'patientName': patientName,
        'medicines': medicines.map((m) => m.toJson()).toList(),
        'diagnosis': diagnosis,
        'notes': notes,
      };
}

class PrescriptionItem {
  final String name;
  final String dosage;
  final String frequency;
  final String duration;

  const PrescriptionItem({
    required this.name,
    this.dosage = '',
    this.frequency = '',
    this.duration = '',
  });

  factory PrescriptionItem.fromJson(Map<String, dynamic> json) =>
      PrescriptionItem(
        name: json['name'] ?? '',
        dosage: json['dosage'] ?? '',
        frequency: json['frequency'] ?? '',
        duration: json['duration'] ?? '',
      );

  Map<String, dynamic> toJson() => {
        'name': name,
        'dosage': dosage,
        'frequency': frequency,
        'duration': duration,
      };
}

// ─────────────────────────────────────────────────────────────────────────────
// NOTIFICATION MODEL
// ─────────────────────────────────────────────────────────────────────────────
enum NotificationType { appointmentBooked, appointmentConfirmed, appointmentCancelled, appointmentReminder, newMessage, newPrescription }

class NotificationModel {
  final String id;
  final String userId;
  final String title;
  final String body;
  final NotificationType type;
  final String? relatedId;
  final bool isRead;
  final DateTime createdAt;

  const NotificationModel({
    required this.id,
    required this.userId,
    required this.title,
    required this.body,
    required this.type,
    this.relatedId,
    this.isRead = false,
    required this.createdAt,
  });

  factory NotificationModel.fromJson(Map<String, dynamic> json, String id) =>
      NotificationModel(
        id: id,
        userId: json['userId'] ?? '',
        title: json['title'] ?? '',
        body: json['body'] ?? '',
        type: _typeFromString(json['type'] ?? ''),
        relatedId: json['relatedId'] as String?,
        isRead: json['isRead'] ?? false,
        createdAt: json['createdAt'] != null
            ? (json['createdAt'] as dynamic).toDate()
            : DateTime.now(),
      );

  static NotificationType _typeFromString(String s) {
    switch (s) {
      case 'appointmentBooked':    return NotificationType.appointmentBooked;
      case 'appointmentConfirmed': return NotificationType.appointmentConfirmed;
      case 'appointmentCancelled': return NotificationType.appointmentCancelled;
      case 'appointmentReminder':  return NotificationType.appointmentReminder;
      case 'newMessage':           return NotificationType.newMessage;
      case 'newPrescription':      return NotificationType.newPrescription;
      default:                     return NotificationType.appointmentBooked;
    }
  }

  Map<String, dynamic> toJson() => {
        'userId': userId,
        'title': title,
        'body': body,
        'type': type.name,
        'relatedId': relatedId,
        'isRead': isRead,
      };

  NotificationModel copyWith({bool? isRead}) => NotificationModel(
        id: id,
        userId: userId,
        title: title,
        body: body,
        type: type,
        relatedId: relatedId,
        isRead: isRead ?? this.isRead,
        createdAt: createdAt,
      );
}
