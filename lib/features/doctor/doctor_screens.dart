import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/constants/app_colors.dart';
import '../../core/models/models.dart';
import '../../core/services/services.dart';
import '../../core/widgets/widgets.dart';
import '../../providers/providers.dart';

// ─── Doctor Shell ─────────────────────────────────────────────────────────────
class DoctorShell extends StatelessWidget {
  final StatefulNavigationShell shell;
  const DoctorShell({super.key, required this.shell});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: shell,
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: shell.currentIndex,
        onTap: (i) => shell.goBranch(i, initialLocation: i == shell.currentIndex),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.dashboard_outlined), activeIcon: Icon(Icons.dashboard), label: 'Dashboard'),
          BottomNavigationBarItem(icon: Icon(Icons.calendar_today_outlined), activeIcon: Icon(Icons.calendar_today), label: 'Schedule'),
          BottomNavigationBarItem(icon: Icon(Icons.chat_bubble_outline), activeIcon: Icon(Icons.chat_bubble), label: 'Chats'),
          BottomNavigationBarItem(icon: Icon(Icons.person_outline), activeIcon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}

// ─── Doctor Home ──────────────────────────────────────────────────────────────
class DoctorHome extends ConsumerWidget {
  const DoctorHome({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(currentUserProvider);

    return userAsync.when(
      loading: () => const Scaffold(body: Center(child: CircularProgressIndicator())),
      error: (e, __) => Scaffold(body: AppErrorWidget(message: e.toString())),
      data: (user) {
        if (user == null) return const Scaffold(body: Center(child: Text('Not found')));
        final apptAsync = ref.watch(doctorAppointmentsProvider(user.uid));

        return Scaffold(
          backgroundColor: AppColors.background,
          body: CustomScrollView(
            slivers: [
              SliverAppBar(
                expandedHeight: 140,
                pinned: true,
                backgroundColor: AppColors.primary,
                flexibleSpace: FlexibleSpaceBar(
                  background: Container(
                    decoration: const BoxDecoration(
                      gradient: LinearGradient(
                        colors: AppColors.gradientPrimary,
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                    ),
                    child: SafeArea(
                      child: Padding(
                        padding: const EdgeInsets.fromLTRB(20, 20, 20, 0),
                        child: Row(
                          children: [
                            AppAvatar(
                              imageUrl: user.photoUrl,
                              name: user.name,
                              radius: 30,
                            ),
                            const SizedBox(width: 14),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  const Text('Welcome back,',
                                      style: TextStyle(color: Colors.white70, fontSize: 13)),
                                  Text(
                                    'Dr. ${user.name}',
                                    style: const TextStyle(
                                      color: Colors.white,
                                      fontSize: 20,
                                      fontWeight: FontWeight.w700,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ),
              ),

              SliverPadding(
                padding: const EdgeInsets.all(16),
                sliver: SliverList(
                  delegate: SliverChildListDelegate([
                    // Stats
                    apptAsync.when(
                      loading: () => const ShimmerCard(height: 100),
                      error: (_, __) => const SizedBox.shrink(),
                      data: (appointments) {
                        final pending = appointments
                            .where((a) => a.status == AppointmentStatus.pending)
                            .length;
                        final confirmed = appointments
                            .where((a) => a.status == AppointmentStatus.confirmed)
                            .length;
                        final completed = appointments
                            .where((a) => a.status == AppointmentStatus.completed)
                            .length;

                        return Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text('Overview',
                                style: TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.w600,
                                    color: AppColors.textPrimary)),
                            const SizedBox(height: 12),
                            Row(
                              children: [
                                Expanded(
                                  child: StatCard(
                                    label: 'Pending',
                                    value: '$pending',
                                    icon: Icons.pending_actions,
                                    color: AppColors.warning,
                                  ),
                                ),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: StatCard(
                                    label: 'Confirmed',
                                    value: '$confirmed',
                                    icon: Icons.check_circle_outline,
                                    color: AppColors.success,
                                  ),
                                ),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: StatCard(
                                    label: 'Completed',
                                    value: '$completed',
                                    icon: Icons.task_alt,
                                    color: AppColors.primary,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        );
                      },
                    ),

                    const SizedBox(height: 24),

                    // Today's appointments
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text("Today's Appointments",
                            style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.w600,
                                color: AppColors.textPrimary)),
                        TextButton(
                          onPressed: () => context.go('/doctor/appointments'),
                          child: const Text('See all'),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),

                    apptAsync.when(
                      loading: () => const ShimmerCard(height: 110),
                      error: (_, __) => const SizedBox.shrink(),
                      data: (appointments) {
                        final today = DateTime.now();
                        final todayStr = '${today.year}-${today.month.toString().padLeft(2, '0')}-${today.day.toString().padLeft(2, '0')}';
                        final todayAppts = appointments
                            .where((a) => a.date == todayStr)
                            .take(5)
                            .toList();

                        if (todayAppts.isEmpty) {
                          return EmptyState(
                            icon: Icons.event_available,
                            title: 'No appointments today',
                            subtitle: 'Your schedule is clear for today',
                          );
                        }

                        return Column(
                          children: todayAppts.map((a) => AppointmentCard(
                            appointment: a,
                            isDoctor: true,
                            onTap: () => _showAppointmentActions(context, ref, a),
                            trailing: a.status == AppointmentStatus.confirmed
                                ? IconButton(
                                    icon: const Icon(Icons.video_call,
                                        color: AppColors.primary),
                                    onPressed: () => context.go('/video/${a.id}'),
                                  )
                                : null,
                          )).toList(),
                        );
                      },
                    ),
                  ]),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  void _showAppointmentActions(
    BuildContext context,
    WidgetRef ref,
    AppointmentModel apt,
  ) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 40,
              height: 4,
              decoration: BoxDecoration(
                color: AppColors.border,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            const SizedBox(height: 16),
            Text('Appointment with ${apt.patientName}',
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
            const SizedBox(height: 16),
            if (apt.status == AppointmentStatus.pending) ...[
              AppButton(
                label: 'Confirm Appointment',
                onPressed: () async {
                  await FirestoreService().updateAppointmentStatus(
                    apt.id, AppointmentStatus.confirmed,
                  );
                  if (ctx.mounted) Navigator.pop(ctx);
                },
                icon: Icons.check,
              ),
              const SizedBox(height: 10),
            ],
            if (apt.status == AppointmentStatus.confirmed) ...[
              AppButton(
                label: 'Mark as Completed',
                onPressed: () async {
                  await FirestoreService().updateAppointmentStatus(
                    apt.id, AppointmentStatus.completed,
                  );
                  if (ctx.mounted) Navigator.pop(ctx);
                },
                icon: Icons.task_alt,
              ),
              const SizedBox(height: 10),
            ],
            if (apt.status != AppointmentStatus.cancelled &&
                apt.status != AppointmentStatus.completed)
              AppButton(
                label: 'Cancel Appointment',
                onPressed: () async {
                  await FirestoreService().updateAppointmentStatus(
                    apt.id, AppointmentStatus.cancelled,
                  );
                  if (ctx.mounted) Navigator.pop(ctx);
                },
                isOutlined: true,
                icon: Icons.cancel_outlined,
              ),
          ],
        ),
      ),
    );
  }
}

// ─── Doctor Appointments Screen ───────────────────────────────────────────────
class DoctorAppointmentsScreen extends ConsumerWidget {
  const DoctorAppointmentsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(currentUserProvider).value;
    if (user == null) return const Scaffold(body: Center(child: CircularProgressIndicator()));

    final apptAsync = ref.watch(doctorAppointmentsProvider(user.uid));

    return DefaultTabController(
      length: 4,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('My Schedule'),
          bottom: const TabBar(
            isScrollable: true,
            tabs: [
              Tab(text: 'Pending'),
              Tab(text: 'Confirmed'),
              Tab(text: 'Completed'),
              Tab(text: 'Cancelled'),
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
                itemBuilder: (ctx, i) => AppointmentCard(
                  appointment: list[i],
                  isDoctor: true,
                  onTap: () => _showActions(context, ref, list[i]),
                  trailing: list[i].status == AppointmentStatus.confirmed
                      ? IconButton(
                          icon: const Icon(Icons.video_call, color: AppColors.primary),
                          onPressed: () => ctx.go('/video/${list[i].id}'),
                        )
                      : null,
                ),
              );
            }

            return TabBarView(
              children: [
                tab(all.where((a) => a.status == AppointmentStatus.pending).toList()),
                tab(all.where((a) => a.status == AppointmentStatus.confirmed).toList()),
                tab(all.where((a) => a.status == AppointmentStatus.completed).toList()),
                tab(all.where((a) => a.status == AppointmentStatus.cancelled).toList()),
              ],
            );
          },
        ),
      ),
    );
  }

  void _showActions(BuildContext ctx, WidgetRef ref, AppointmentModel apt) {
    showModalBottomSheet(
      context: ctx,
      shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (sheetCtx) => Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (apt.status == AppointmentStatus.pending)
              AppButton(
                label: 'Confirm',
                icon: Icons.check,
                onPressed: () async {
                  await FirestoreService()
                      .updateAppointmentStatus(apt.id, AppointmentStatus.confirmed);
                  if (sheetCtx.mounted) Navigator.pop(sheetCtx);
                },
              ),
            if (apt.status == AppointmentStatus.confirmed) ...[
              const SizedBox(height: 10),
              AppButton(
                label: 'Mark Completed',
                icon: Icons.task_alt,
                onPressed: () async {
                  await FirestoreService()
                      .updateAppointmentStatus(apt.id, AppointmentStatus.completed);
                  if (sheetCtx.mounted) Navigator.pop(sheetCtx);
                },
              ),
            ],
            if (apt.status != AppointmentStatus.cancelled &&
                apt.status != AppointmentStatus.completed) ...[
              const SizedBox(height: 10),
              AppButton(
                label: 'Cancel',
                isOutlined: true,
                icon: Icons.cancel_outlined,
                onPressed: () async {
                  await FirestoreService()
                      .updateAppointmentStatus(apt.id, AppointmentStatus.cancelled);
                  if (sheetCtx.mounted) Navigator.pop(sheetCtx);
                },
              ),
            ],
            const SizedBox(height: 8),
          ],
        ),
      ),
    );
  }
}
