import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/constants/app_colors.dart';
import '../../core/models/models.dart';
import '../../core/services/services.dart';
import '../../core/widgets/widgets.dart';
import '../../providers/providers.dart';

// ─── Admin Shell ──────────────────────────────────────────────────────────────
class AdminShell extends StatelessWidget {
  final StatefulNavigationShell shell;
  const AdminShell({super.key, required this.shell});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: shell,
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: shell.currentIndex,
        onTap: (i) => shell.goBranch(i, initialLocation: i == shell.currentIndex),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.dashboard_outlined), activeIcon: Icon(Icons.dashboard), label: 'Dashboard'),
          BottomNavigationBarItem(icon: Icon(Icons.people_outline), activeIcon: Icon(Icons.people), label: 'Users'),
          BottomNavigationBarItem(icon: Icon(Icons.calendar_today_outlined), activeIcon: Icon(Icons.calendar_today), label: 'Appointments'),
          BottomNavigationBarItem(icon: Icon(Icons.person_outline), activeIcon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}

// ─── Admin Home ───────────────────────────────────────────────────────────────
class AdminHome extends ConsumerWidget {
  const AdminHome({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final statsAsync = ref.watch(dashboardStatsProvider);
    final usersAsync = ref.watch(allUsersProvider);
    final apptAsync  = ref.watch(allAppointmentsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Admin Dashboard'),
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await AuthService().signOut();
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Stats
            statsAsync.when(
              loading: () => const ShimmerCard(height: 100),
              error: (_, __) => const SizedBox.shrink(),
              data: (stats) => Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Overview',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                  const SizedBox(height: 12),
                  GridView.count(
                    crossAxisCount: 2,
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    crossAxisSpacing: 12,
                    mainAxisSpacing: 12,
                    childAspectRatio: 1.6,
                    children: [
                      StatCard(
                        label: 'Total',
                        value: '${stats['total'] ?? 0}',
                        icon: Icons.event_note,
                        color: AppColors.primary,
                      ),
                      StatCard(
                        label: 'Pending',
                        value: '${stats['pending'] ?? 0}',
                        icon: Icons.pending_actions,
                        color: AppColors.warning,
                      ),
                      StatCard(
                        label: 'Confirmed',
                        value: '${stats['confirmed'] ?? 0}',
                        icon: Icons.check_circle_outline,
                        color: AppColors.success,
                      ),
                      StatCard(
                        label: 'Completed',
                        value: '${stats['completed'] ?? 0}',
                        icon: Icons.task_alt,
                        color: AppColors.info,
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // User breakdown
            usersAsync.when(
              loading: () => const ShimmerCard(),
              error: (_, __) => const SizedBox.shrink(),
              data: (users) {
                final doctors  = users.where((u) => u.role == 'doctor').length;
                final patients = users.where((u) => u.role == 'patient').length;
                return Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: AppColors.card,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: AppColors.border, width: 0.8),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Users',
                          style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          _userStat(Icons.people, '${users.length}', 'Total', AppColors.primary),
                          _userStat(Icons.medical_services, '$doctors', 'Doctors', AppColors.info),
                          _userStat(Icons.person, '$patients', 'Patients', AppColors.success),
                        ],
                      ),
                    ],
                  ),
                );
              },
            ),
            const SizedBox(height: 24),

            // Recent appointments
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Recent Appointments',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                TextButton(
                  onPressed: () => context.go('/admin/appointments'),
                  child: const Text('See all'),
                ),
              ],
            ),
            const SizedBox(height: 8),
            apptAsync.when(
              loading: () => const ShimmerCard(height: 110),
              error: (_, __) => const SizedBox.shrink(),
              data: (all) => Column(
                children: all.take(5).map((a) => AppointmentCard(
                  appointment: a,
                  isDoctor: false,
                  trailing: _statusActions(context, a),
                )).toList(),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _userStat(IconData icon, String val, String label, Color color) {
    return Expanded(
      child: Column(
        children: [
          Icon(icon, color: color, size: 28),
          const SizedBox(height: 4),
          Text(val, style: TextStyle(fontSize: 22, fontWeight: FontWeight.w700, color: color)),
          Text(label, style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
        ],
      ),
    );
  }

  Widget? _statusActions(BuildContext context, AppointmentModel apt) {
    if (apt.status == AppointmentStatus.pending) {
      return IconButton(
        icon: const Icon(Icons.check_circle_outline, color: AppColors.success),
        tooltip: 'Confirm',
        onPressed: () => FirestoreService()
            .updateAppointmentStatus(apt.id, AppointmentStatus.confirmed),
      );
    }
    return null;
  }
}

// ─── Admin Users Screen ───────────────────────────────────────────────────────
class AdminUsersScreen extends ConsumerWidget {
  const AdminUsersScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(allUsersProvider);

    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Manage Users'),
          bottom: const TabBar(
            tabs: [Tab(text: 'All'), Tab(text: 'Doctors'), Tab(text: 'Patients')],
            indicatorColor: AppColors.primary,
            labelColor: AppColors.primary,
            unselectedLabelColor: AppColors.textSecondary,
          ),
        ),
        body: usersAsync.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (e, __) => AppErrorWidget(message: e.toString()),
          data: (users) {
            Widget tab(List<UserModel> list) {
              if (list.isEmpty) {
                return EmptyState(
                  icon: Icons.people_outline,
                  title: 'No users',
                  subtitle: '',
                );
              }
              return ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: list.length,
                itemBuilder: (ctx, i) => _UserTile(user: list[i]),
              );
            }

            return TabBarView(
              children: [
                tab(users),
                tab(users.where((u) => u.role == 'doctor').toList()),
                tab(users.where((u) => u.role == 'patient').toList()),
              ],
            );
          },
        ),
      ),
    );
  }
}

class _UserTile extends ConsumerWidget {
  final UserModel user;
  const _UserTile({required this.user});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppColors.card,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppColors.border, width: 0.8),
      ),
      child: Row(
        children: [
          AppAvatar(imageUrl: user.photoUrl, name: user.name, radius: 24),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(user.name,
                    style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                Text(user.email,
                    style: const TextStyle(color: AppColors.textSecondary, fontSize: 12)),
              ],
            ),
          ),
          _roleBadge(user.role),
          if (user.role == 'doctor')
            _DoctorVerifyToggle(uid: user.uid),
        ],
      ),
    );
  }

  Widget _roleBadge(String role) {
    Color c = role == 'doctor' ? AppColors.info : AppColors.success;
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: c.withOpacity(0.12),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(role,
          style: TextStyle(color: c, fontSize: 11, fontWeight: FontWeight.w600)),
    );
  }
}

class _DoctorVerifyToggle extends ConsumerWidget {
  final String uid;
  const _DoctorVerifyToggle({required this.uid});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final doctorAsync = ref.watch(doctorByIdProvider(uid));
    return doctorAsync.when(
      data: (doc) {
        if (doc == null) return const SizedBox.shrink();
        return IconButton(
          icon: Icon(
            doc.isVerified ? Icons.verified : Icons.verified_outlined,
            color: doc.isVerified ? AppColors.primary : AppColors.textHint,
          ),
          tooltip: doc.isVerified ? 'Revoke verification' : 'Verify doctor',
          onPressed: () =>
              FirestoreService().verifyDoctor(uid, !doc.isVerified),
        );
      },
      loading: () => const SizedBox.shrink(),
      error: (_, __) => const SizedBox.shrink(),
    );
  }
}

// ─── Admin Appointments Screen ────────────────────────────────────────────────
class AdminAppointmentsScreen extends ConsumerWidget {
  const AdminAppointmentsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final apptAsync = ref.watch(allAppointmentsProvider);

    return DefaultTabController(
      length: 4,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('All Appointments'),
          bottom: const TabBar(
            isScrollable: true,
            tabs: [
              Tab(text: 'All'),
              Tab(text: 'Pending'),
              Tab(text: 'Confirmed'),
              Tab(text: 'Completed'),
            ],
            indicatorColor: AppColors.primary,
            labelColor: AppColors.primary,
            unselectedLabelColor: AppColors.textSecondary,
          ),
        ),
        body: apptAsync.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (e, __) => AppErrorWidget(message: e.toString()),
          data: (all) {
            Widget tab(List<AppointmentModel> list) {
              if (list.isEmpty) {
                return EmptyState(
                  icon: Icons.calendar_today_outlined,
                  title: 'No appointments',
                  subtitle: '',
                );
              }
              return ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: list.length,
                itemBuilder: (_, i) => AppointmentCard(
                  appointment: list[i],
                  isDoctor: false,
                  trailing: list[i].status == AppointmentStatus.pending
                      ? Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            IconButton(
                              icon: const Icon(Icons.check, color: AppColors.success),
                              onPressed: () => FirestoreService()
                                  .updateAppointmentStatus(
                                      list[i].id, AppointmentStatus.confirmed),
                            ),
                            IconButton(
                              icon: const Icon(Icons.close, color: AppColors.error),
                              onPressed: () => FirestoreService()
                                  .updateAppointmentStatus(
                                      list[i].id, AppointmentStatus.cancelled),
                            ),
                          ],
                        )
                      : null,
                ),
              );
            }

            return TabBarView(
              children: [
                tab(all),
                tab(all.where((a) => a.status == AppointmentStatus.pending).toList()),
                tab(all.where((a) => a.status == AppointmentStatus.confirmed).toList()),
                tab(all.where((a) => a.status == AppointmentStatus.completed).toList()),
              ],
            );
          },
        ),
      ),
    );
  }
}
