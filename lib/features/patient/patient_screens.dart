import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';
import 'package:table_calendar/table_calendar.dart';
import '../../core/constants/app_colors.dart';
import '../../core/models/models.dart';
import '../../core/services/services.dart';
import '../../core/widgets/widgets.dart';
import '../../providers/providers.dart';

// ─────────────────────────────────────────────────────────────────────────────
// PATIENT HOME
// ─────────────────────────────────────────────────────────────────────────────
class PatientHome extends ConsumerWidget {
  const PatientHome({super.key});

  static const _specialties = [
    'All', 'General Physician', 'Cardiologist', 'Dermatologist',
    'Neurologist', 'Orthopedic', 'Pediatrician', 'Psychiatrist',
    'Gynecologist', 'ENT',
  ];

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(currentUserProvider);
    final doctorsAsync = ref.watch(doctorsProvider);
    final selectedSpecialty = ref.watch(specialtyFilterProvider);
    final searchQ = ref.watch(searchQueryProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 160,
            floating: false,
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
                    padding: const EdgeInsets.fromLTRB(20, 16, 20, 8),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        userAsync.when(
                          data: (u) => Text(
                            'Hello, ${u?.name.split(' ').first ?? 'Patient'}!',
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 22,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                          loading: () => const SizedBox.shrink(),
                          error: (_, __) => const SizedBox.shrink(),
                        ),
                        const Text(
                          'Find and book your doctor',
                          style: TextStyle(color: Colors.white70, fontSize: 14),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
            bottom: PreferredSize(
              preferredSize: const Size.fromHeight(56),
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 0, 16, 8),
                child: TextField(
                  onChanged: (v) => ref.read(searchQueryProvider.notifier).state = v,
                  decoration: InputDecoration(
                    hintText: 'Search doctors, specialties...',
                    fillColor: Colors.white,
                    filled: true,
                    prefixIcon: const Icon(Icons.search, color: AppColors.textSecondary),
                    contentPadding: const EdgeInsets.symmetric(vertical: 0, horizontal: 16),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(30),
                      borderSide: BorderSide.none,
                    ),
                  ),
                ),
              ),
            ),
          ),

          // Specialty filter chips
          SliverToBoxAdapter(
            child: SizedBox(
              height: 50,
              child: ListView.separated(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                itemCount: _specialties.length,
                separatorBuilder: (_, __) => const SizedBox(width: 8),
                itemBuilder: (ctx, i) {
                  final s = _specialties[i];
                  final active = (s == 'All' && selectedSpecialty == null) ||
                      s == selectedSpecialty;
                  return GestureDetector(
                    onTap: () => ref.read(specialtyFilterProvider.notifier).state =
                        s == 'All' ? null : s,
                    child: AnimatedContainer(
                      duration: const Duration(milliseconds: 200),
                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                      decoration: BoxDecoration(
                        color: active ? AppColors.primary : AppColors.surface,
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(
                          color: active ? AppColors.primary : AppColors.border,
                          width: 0.8,
                        ),
                      ),
                      child: Text(
                        s,
                        style: TextStyle(
                          color: active ? Colors.white : AppColors.textSecondary,
                          fontSize: 13,
                          fontWeight: active ? FontWeight.w600 : FontWeight.w400,
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),
          ),

          // Doctor list
          doctorsAsync.when(
            loading: () => SliverPadding(
              padding: const EdgeInsets.all(16),
              sliver: SliverList(
                delegate: SliverChildBuilderDelegate(
                  (_, __) => const ShimmerCard(height: 110),
                  childCount: 5,
                ),
              ),
            ),
            error: (e, __) => SliverFillRemaining(
              child: AppErrorWidget(message: e.toString()),
            ),
            data: (doctors) {
              final filtered = searchQ.isEmpty
                  ? doctors
                  : doctors.where((d) =>
                      d.name.toLowerCase().contains(searchQ.toLowerCase()) ||
                      d.specialty.toLowerCase().contains(searchQ.toLowerCase())).toList();

              if (filtered.isEmpty) {
                return SliverFillRemaining(
                  child: EmptyState(
                    icon: Icons.person_search,
                    title: 'No doctors found',
                    subtitle: 'Try a different search or specialty filter',
                  ),
                );
              }

              return SliverPadding(
                padding: const EdgeInsets.all(16),
                sliver: SliverList(
                  delegate: SliverChildBuilderDelegate(
                    (ctx, i) => DoctorCard(
                      doctor: filtered[i],
                      onTap: () => ctx.go(
                        '/patient/home/doctors/${filtered[i].uid}',
                        extra: filtered[i],
                      ),
                    ),
                    childCount: filtered.length,
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// DOCTOR LIST SCREEN
// ─────────────────────────────────────────────────────────────────────────────
class DoctorListScreen extends ConsumerWidget {
  const DoctorListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final doctorsAsync = ref.watch(doctorsProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('All Doctors')),
      body: doctorsAsync.when(
        loading: () => ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: 6,
          itemBuilder: (_, __) => const ShimmerCard(height: 110),
        ),
        error: (e, __) => AppErrorWidget(message: e.toString()),
        data: (doctors) => ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: doctors.length,
          itemBuilder: (ctx, i) => DoctorCard(
            doctor: doctors[i],
            onTap: () => ctx.go(
              '/patient/home/doctors/${doctors[i].uid}',
              extra: doctors[i],
            ),
          ),
        ),
      ),
    );
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// DOCTOR PROFILE SCREEN
// ─────────────────────────────────────────────────────────────────────────────
class DoctorProfileScreen extends ConsumerWidget {
  final String doctorId;
  const DoctorProfileScreen({super.key, required this.doctorId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final doctorAsync = ref.watch(doctorByIdProvider(doctorId));

    return doctorAsync.when(
      loading: () => const Scaffold(body: Center(child: CircularProgressIndicator())),
      error: (e, __) => Scaffold(body: AppErrorWidget(message: e.toString())),
      data: (doctor) {
        if (doctor == null) {
          return const Scaffold(body: Center(child: Text('Doctor not found')));
        }
        return _DoctorProfileView(doctor: doctor);
      },
    );
  }
}

class _DoctorProfileView extends ConsumerWidget {
  final DoctorModel doctor;
  const _DoctorProfileView({required this.doctor});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 240,
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
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const SizedBox(height: 60),
                    AppAvatar(imageUrl: doctor.photoUrl, name: doctor.name, radius: 48),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(
                          'Dr. ${doctor.name}',
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 22,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                        if (doctor.isVerified) ...[
                          const SizedBox(width: 6),
                          const Icon(Icons.verified, color: Colors.white, size: 20),
                        ],
                      ],
                    ),
                    const SizedBox(height: 4),
                    Text(doctor.specialty,
                        style: const TextStyle(color: Colors.white70, fontSize: 14)),
                  ],
                ),
              ),
            ),
          ),

          SliverPadding(
            padding: const EdgeInsets.all(16),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                // Stats row
                Row(
                  children: [
                    _statBox('${doctor.experience}+', 'Years Exp'),
                    const SizedBox(width: 12),
                    _statBox('${doctor.rating}', 'Rating'),
                    const SizedBox(width: 12),
                    _statBox('${doctor.totalReviews}', 'Reviews'),
                  ],
                ),
                const SizedBox(height: 20),

                // Fee
                _sectionCard(
                  'Consultation Fee',
                  Row(
                    children: [
                      const Icon(Icons.payments_outlined, color: AppColors.success),
                      const SizedBox(width: 8),
                      Text(
                        'Rs. ${doctor.fee.toInt()} per session',
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          color: AppColors.success,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 12),

                // About
                if (doctor.about.isNotEmpty)
                  _sectionCard(
                    'About',
                    Text(
                      doctor.about,
                      style: const TextStyle(
                        color: AppColors.textSecondary,
                        height: 1.6,
                        fontSize: 14,
                      ),
                    ),
                  ),
                if (doctor.about.isNotEmpty) const SizedBox(height: 12),

                // Clinic
                if (doctor.clinicAddress.isNotEmpty)
                  _sectionCard(
                    'Clinic',
                    Row(
                      children: [
                        const Icon(Icons.location_on_outlined,
                            color: AppColors.primary, size: 18),
                        const SizedBox(width: 6),
                        Expanded(
                          child: Text(
                            doctor.clinicAddress,
                            style: const TextStyle(color: AppColors.textSecondary, fontSize: 14),
                          ),
                        ),
                      ],
                    ),
                  ),
                if (doctor.clinicAddress.isNotEmpty) const SizedBox(height: 12),

                // Available days
                _sectionCard(
                  'Working Days',
                  Wrap(
                    spacing: 8,
                    children: doctor.availableDays
                        .map((d) => Chip(label: Text(d)))
                        .toList(),
                  ),
                ),
                const SizedBox(height: 24),

                AppButton(
                  label: 'Book Appointment',
                  onPressed: () => context.go(
                    '/patient/home/doctors/${doctor.uid}/book',
                    extra: doctor,
                  ),
                  icon: Icons.calendar_today,
                ),
                const SizedBox(height: 16),
              ]),
            ),
          ),
        ],
      ),
    );
  }

  Widget _statBox(String value, String label) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: AppColors.card,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: AppColors.border, width: 0.8),
        ),
        child: Column(
          children: [
            Text(value,
                style: const TextStyle(
                    fontSize: 22, fontWeight: FontWeight.w700, color: AppColors.primary)),
            const SizedBox(height: 2),
            Text(label, style: const TextStyle(color: AppColors.textSecondary, fontSize: 12)),
          ],
        ),
      ),
    );
  }

  Widget _sectionCard(String title, Widget child) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.card,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppColors.border, width: 0.8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title,
              style: const TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: AppColors.textSecondary,
                  letterSpacing: 0.5)),
          const SizedBox(height: 10),
          child,
        ],
      ),
    );
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// BOOKING SCREEN
// ─────────────────────────────────────────────────────────────────────────────
class BookingScreen extends ConsumerStatefulWidget {
  final DoctorModel doctor;
  const BookingScreen({super.key, required this.doctor});
  @override
  ConsumerState<BookingScreen> createState() => _BookingScreenState();
}

class _BookingScreenState extends ConsumerState<BookingScreen> {
  DateTime _selectedDay = DateTime.now().add(const Duration(days: 1));
  String? _selectedTime;
  bool _loading = false;
  final _notesCtrl = TextEditingController();

  @override
  void dispose() {
    _notesCtrl.dispose();
    super.dispose();
  }

  String get _formattedDate => DateFormat('yyyy-MM-dd').format(_selectedDay);
  String get _displayDate => DateFormat('EEEE, MMMM d yyyy').format(_selectedDay);

  Future<void> _book() async {
    if (_selectedTime == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please select a time slot'),
          backgroundColor: AppColors.warning,
        ),
      );
      return;
    }

    final user = ref.read(currentUserProvider).value;
    if (user == null) return;

    setState(() => _loading = true);
    try {
      // Seed slots if none exist
      await FirestoreService().seedDoctorSlots(widget.doctor.uid, _formattedDate);

      final id = await FirestoreService().bookAppointment(
        patientId: user.uid,
        patientName: user.name,
        patientPhoto: user.photoUrl,
        doctor: widget.doctor,
        date: _formattedDate,
        time: _selectedTime!,
        notes: _notesCtrl.text.trim(),
      );

      if (!mounted) return;
      _showSuccess();
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(e.toString()),
          backgroundColor: AppColors.error,
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
      );
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  void _showSuccess() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.all(20),
              decoration: const BoxDecoration(
                color: Color(0xFFE8F8F3),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.check_circle_rounded,
                  color: AppColors.success, size: 56),
            ),
            const SizedBox(height: 16),
            const Text('Appointment Booked!',
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.w700)),
            const SizedBox(height: 8),
            Text(
              'Your appointment with Dr. ${widget.doctor.name} is booked for $_displayDate at $_selectedTime.',
              textAlign: TextAlign.center,
              style: const TextStyle(color: AppColors.textSecondary, fontSize: 14),
            ),
            const SizedBox(height: 20),
            AppButton(
              label: 'View Appointments',
              onPressed: () {
                Navigator.pop(ctx);
                context.go('/patient/appointments');
              },
            ),
            const SizedBox(height: 8),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final dateKey = (doctorId: widget.doctor.uid, date: _formattedDate);
    final slotsAsync = ref.watch(availableSlotsProvider(dateKey));

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(title: const Text('Book Appointment')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Doctor info
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppColors.card,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppColors.border, width: 0.8),
              ),
              child: Row(
                children: [
                  AppAvatar(
                    imageUrl: widget.doctor.photoUrl,
                    name: widget.doctor.name,
                    radius: 28,
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Dr. ${widget.doctor.name}',
                            style: const TextStyle(
                                fontWeight: FontWeight.w600, fontSize: 16)),
                        Text(widget.doctor.specialty,
                            style: const TextStyle(
                                color: AppColors.primary, fontSize: 13)),
                        Text('Rs. ${widget.doctor.fee.toInt()} / session',
                            style: const TextStyle(
                                color: AppColors.success, fontSize: 13)),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Calendar
            const Text('Select Date',
                style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
            const SizedBox(height: 10),
            Container(
              decoration: BoxDecoration(
                color: AppColors.card,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppColors.border, width: 0.8),
              ),
              child: TableCalendar(
                firstDay: DateTime.now().add(const Duration(days: 1)),
                lastDay: DateTime.now().add(const Duration(days: 60)),
                focusedDay: _selectedDay,
                selectedDayPredicate: (d) => isSameDay(d, _selectedDay),
                onDaySelected: (sel, focus) {
                  setState(() {
                    _selectedDay = sel;
                    _selectedTime = null;
                  });
                  // Seed slots for the new date
                  FirestoreService().seedDoctorSlots(widget.doctor.uid, _formattedDate);
                },
                availableGestures: AvailableGestures.all,
                calendarStyle: const CalendarStyle(
                  selectedDecoration: BoxDecoration(
                    color: AppColors.primary,
                    shape: BoxShape.circle,
                  ),
                  todayDecoration: BoxDecoration(
                    color: AppColors.primaryLight,
                    shape: BoxShape.circle,
                  ),
                  todayTextStyle: TextStyle(color: AppColors.primary),
                  weekendTextStyle: TextStyle(color: AppColors.error),
                ),
                headerStyle: const HeaderStyle(
                  formatButtonVisible: false,
                  titleCentered: true,
                  leftChevronIcon: Icon(Icons.chevron_left, color: AppColors.primary),
                  rightChevronIcon: Icon(Icons.chevron_right, color: AppColors.primary),
                ),
              ),
            ),
            const SizedBox(height: 20),

            // Time slots
            Text('Available Slots — $_displayDate',
                style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
            const SizedBox(height: 10),

            slotsAsync.when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (e, __) => Text('Error: $e'),
              data: (slots) {
                if (slots.isEmpty) {
                  return Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: AppColors.card,
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(color: AppColors.border, width: 0.8),
                    ),
                    child: Column(
                      children: [
                        const Icon(Icons.event_busy, color: AppColors.textHint, size: 36),
                        const SizedBox(height: 8),
                        const Text('No slots available for this day',
                            style: TextStyle(color: AppColors.textSecondary)),
                        const SizedBox(height: 8),
                        TextButton(
                          onPressed: () => FirestoreService()
                              .seedDoctorSlots(widget.doctor.uid, _formattedDate),
                          child: const Text('Load Slots'),
                        ),
                      ],
                    ),
                  );
                }

                return Wrap(
                  spacing: 10,
                  runSpacing: 10,
                  children: slots.map((t) {
                    final selected = _selectedTime == t;
                    return GestureDetector(
                      onTap: () => setState(() => _selectedTime = t),
                      child: AnimatedContainer(
                        duration: const Duration(milliseconds: 180),
                        padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 10),
                        decoration: BoxDecoration(
                          color: selected ? AppColors.primary : AppColors.card,
                          borderRadius: BorderRadius.circular(30),
                          border: Border.all(
                            color: selected ? AppColors.primary : AppColors.border,
                            width: selected ? 2 : 0.8,
                          ),
                        ),
                        child: Text(
                          t,
                          style: TextStyle(
                            color: selected ? Colors.white : AppColors.textPrimary,
                            fontWeight: selected ? FontWeight.w600 : FontWeight.w400,
                            fontSize: 14,
                          ),
                        ),
                      ),
                    );
                  }).toList(),
                );
              },
            ),
            const SizedBox(height: 20),

            // Notes
            AppTextField(
              label: 'Notes (optional)',
              hint: 'Describe your concern or symptoms...',
              controller: _notesCtrl,
              maxLines: 3,
            ),
            const SizedBox(height: 24),

            // Summary
            if (_selectedTime != null)
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.primaryLight,
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Column(
                  children: [
                    _summaryRow(Icons.calendar_today, 'Date', _displayDate),
                    const SizedBox(height: 8),
                    _summaryRow(Icons.access_time, 'Time', _selectedTime!),
                    const SizedBox(height: 8),
                    _summaryRow(Icons.payments_outlined, 'Fee',
                        'Rs. ${widget.doctor.fee.toInt()}'),
                  ],
                ),
              ),

            const SizedBox(height: 20),
            AppButton(
              label: 'Confirm Booking',
              onPressed: _book,
              isLoading: _loading,
              icon: Icons.check,
            ),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _summaryRow(IconData icon, String label, String value) {
    return Row(
      children: [
        Icon(icon, size: 16, color: AppColors.primary),
        const SizedBox(width: 8),
        Text('$label: ',
            style: const TextStyle(color: AppColors.textSecondary, fontSize: 13)),
        Text(value,
            style: const TextStyle(
                color: AppColors.textPrimary,
                fontWeight: FontWeight.w600,
                fontSize: 13)),
      ],
    );
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// PATIENT APPOINTMENTS SCREEN
// ─────────────────────────────────────────────────────────────────────────────
class PatientAppointmentsScreen extends ConsumerWidget {
  const PatientAppointmentsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(currentUserProvider).value;
    if (user == null) return const Scaffold(body: Center(child: CircularProgressIndicator()));

    final apptAsync = ref.watch(patientAppointmentsProvider(user.uid));

    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('My Appointments'),
          bottom: const TabBar(
            tabs: [
              Tab(text: 'Upcoming'),
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
            final upcoming = all.where((a) =>
                a.status == AppointmentStatus.pending ||
                a.status == AppointmentStatus.confirmed).toList();
            final completed = all.where((a) => a.status == AppointmentStatus.completed).toList();
            final cancelled = all.where((a) => a.status == AppointmentStatus.cancelled).toList();

            return TabBarView(
              children: [
                _buildList(context, ref, upcoming, false),
                _buildList(context, ref, completed, false),
                _buildList(context, ref, cancelled, false),
              ],
            );
          },
        ),
      ),
    );
  }

  Widget _buildList(BuildContext context, WidgetRef ref,
      List<AppointmentModel> list, bool isDoctor) {
    if (list.isEmpty) {
      return EmptyState(
        icon: Icons.calendar_today_outlined,
        title: 'No appointments',
        subtitle: 'Your appointments will appear here',
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: list.length,
      itemBuilder: (ctx, i) {
        final apt = list[i];
        return AppointmentCard(
          appointment: apt,
          isDoctor: false,
          trailing: apt.status == AppointmentStatus.confirmed
              ? IconButton(
                  icon: const Icon(Icons.video_call, color: AppColors.primary),
                  onPressed: () => ctx.go('/video/${apt.id}'),
                  tooltip: 'Join Video Call',
                )
              : null,
        );
      },
    );
  }
}
