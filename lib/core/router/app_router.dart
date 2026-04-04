import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../models/models.dart';
import '../../providers/providers.dart';
import '../../features/auth/splash_screen.dart';
import '../../features/auth/login_screen.dart';
import '../../features/auth/register_screen.dart';
import '../../features/patient/patient_shell.dart';
import '../../features/patient/patient_home.dart';
import '../../features/patient/doctor_list_screen.dart';
import '../../features/patient/doctor_profile_screen.dart';
import '../../features/patient/booking_screen.dart';
import '../../features/patient/patient_appointments_screen.dart';
import '../../features/doctor/doctor_shell.dart';
import '../../features/doctor/doctor_home.dart';
import '../../features/doctor/doctor_appointments_screen.dart';
import '../../features/admin/admin_shell.dart';
import '../../features/admin/admin_home.dart';
import '../../features/admin/admin_users_screen.dart';
import '../../features/admin/admin_appointments_screen.dart';
import '../../features/chat/chat_list_screen.dart';
import '../../features/chat/chat_screen.dart';
import '../../features/video/video_call_screen.dart';
import '../../features/profile/profile_screen.dart';

final appRouterProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authStateProvider);
  final userAsync = ref.watch(currentUserProvider);

  return GoRouter(
    initialLocation: '/splash',
    redirect: (context, state) {
      if (authState.isLoading) return '/splash';
      final user = authState.value;
      final path = state.uri.path;

      if (user == null) {
        const open = ['/login', '/register', '/splash'];
        return open.contains(path) ? null : '/login';
      }

      if (userAsync.isLoading) return '/splash';
      final model = userAsync.value;
      if (model == null) return '/login';

      const authPaths = ['/login', '/register', '/splash'];
      if (authPaths.contains(path)) return _homeFor(model.role);
      return null;
    },
    routes: [
      GoRoute(path: '/splash',   builder: (_, __) => const SplashScreen()),
      GoRoute(path: '/login',    builder: (_, __) => const LoginScreen()),
      GoRoute(path: '/register', builder: (_, __) => const RegisterScreen()),

      StatefulShellRoute.indexedStack(
        builder: (_, __, shell) => PatientShell(shell: shell),
        branches: [
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/patient/home',
              builder: (_, __) => const PatientHome(),
              routes: [
                GoRoute(
                  path: 'doctors',
                  builder: (_, __) => const DoctorListScreen(),
                  routes: [
                    GoRoute(
                      path: ':doctorId',
                      builder: (_, s) => DoctorProfileScreen(doctorId: s.pathParameters['doctorId']!),
                      routes: [
                        GoRoute(
                          path: 'book',
                          builder: (_, s) => BookingScreen(doctor: s.extra as DoctorModel),
                        ),
                      ],
                    ),
                  ],
                ),
              ],
            ),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(path: '/patient/appointments', builder: (_, __) => const PatientAppointmentsScreen()),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/patient/chats',
              builder: (_, __) => const ChatListScreen(role: 'patient'),
              routes: [_chatRoute()],
            ),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(path: '/patient/profile', builder: (_, __) => const ProfileScreen()),
          ]),
        ],
      ),

      StatefulShellRoute.indexedStack(
        builder: (_, __, shell) => DoctorShell(shell: shell),
        branches: [
          StatefulShellBranch(routes: [
            GoRoute(path: '/doctor/home', builder: (_, __) => const DoctorHome()),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(path: '/doctor/appointments', builder: (_, __) => const DoctorAppointmentsScreen()),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/doctor/chats',
              builder: (_, __) => const ChatListScreen(role: 'doctor'),
              routes: [_chatRoute()],
            ),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(path: '/doctor/profile', builder: (_, __) => const ProfileScreen()),
          ]),
        ],
      ),

      StatefulShellRoute.indexedStack(
        builder: (_, __, shell) => AdminShell(shell: shell),
        branches: [
          StatefulShellBranch(routes: [
            GoRoute(path: '/admin/home', builder: (_, __) => const AdminHome()),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(path: '/admin/users', builder: (_, __) => const AdminUsersScreen()),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(path: '/admin/appointments', builder: (_, __) => const AdminAppointmentsScreen()),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(path: '/admin/profile', builder: (_, __) => const ProfileScreen()),
          ]),
        ],
      ),

      GoRoute(
        path: '/video/:appointmentId',
        builder: (_, s) => VideoCallScreen(
          appointmentId: s.pathParameters['appointmentId']!,
          channelName:   s.pathParameters['appointmentId']!,
        ),
      ),
    ],
    errorBuilder: (_, s) => Scaffold(body: Center(child: Text('404: ${s.uri}'))),
  );
});

GoRoute _chatRoute() => GoRoute(
  path: ':chatId',
  builder: (_, s) {
    final extra = s.extra as Map<String, dynamic>? ?? {};
    return ChatScreen(
      chatId:         s.pathParameters['chatId']!,
      otherUserId:    extra['otherUserId']   ?? '',
      otherUserName:  extra['otherUserName']  ?? '',
      otherUserPhoto: extra['otherUserPhoto'] ?? '',
    );
  },
);

String _homeFor(String role) {
  switch (role) {
    case 'doctor': return '/doctor/home';
    case 'admin':  return '/admin/home';
    default:       return '/patient/home';
  }
}
