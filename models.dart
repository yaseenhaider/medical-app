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
