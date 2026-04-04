import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';
import '../../core/constants/app_colors.dart';
import '../../core/models/models.dart';
import '../../core/services/services.dart';
import '../../core/widgets/widgets.dart';
import '../../providers/providers.dart';

class ProfileScreen extends ConsumerStatefulWidget {
  const ProfileScreen({super.key});

  @override
  ConsumerState<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends ConsumerState<ProfileScreen> {
  final _nameCtrl  = TextEditingController();
  final _phoneCtrl = TextEditingController();
  // Doctor-specific
  final _aboutCtrl    = TextEditingController();
  final _addressCtrl  = TextEditingController();
  final _feeCtrl      = TextEditingController();

  bool _editing  = false;
  bool _saving   = false;
  bool _uploading = false;
  UserModel? _user;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _loadUser());
  }

  @override
  void dispose() {
    _nameCtrl.dispose();
    _phoneCtrl.dispose();
    _aboutCtrl.dispose();
    _addressCtrl.dispose();
    _feeCtrl.dispose();
    super.dispose();
  }

  void _loadUser() {
    final u = ref.read(currentUserProvider).value;
    if (u == null) return;
    setState(() => _user = u);
    _nameCtrl.text  = u.name;
    _phoneCtrl.text = u.phone;
  }

  Future<void> _pickPhoto() async {
    final u = _user;
    if (u == null) return;

    final picker = ImagePicker();
    final picked = await picker.pickImage(
      source: ImageSource.gallery,
      imageQuality: 80,
      maxWidth: 800,
    );
    if (picked == null) return;

    setState(() => _uploading = true);
    try {
      dynamic fileData = kIsWeb
          ? await picked.readAsBytes()
          : File(picked.path);

      final url = await StorageService().uploadProfilePhoto(u.uid, fileData);
      final updated = u.copyWith(photoUrl: url);

      await AuthService().updateUser(updated);
      if (mounted) {
        setState(() => _user = updated);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Photo updated!'),
            backgroundColor: AppColors.success,
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
      ref.invalidate(currentUserProvider);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e'), backgroundColor: AppColors.error),
        );
      }
    } finally {
      if (mounted) setState(() => _uploading = false);
    }
  }

  Future<void> _saveProfile() async {
    final u = _user;
    if (u == null) return;

    setState(() => _saving = true);
    try {
      final updated = u.copyWith(
        name: _nameCtrl.text.trim(),
        phone: _phoneCtrl.text.trim(),
      );
      await AuthService().updateUser(updated);

      // If doctor, update doctor profile too
      if (u.role == 'doctor') {
        await FirestoreService().updateDoctorProfile(u.uid, {
          'name': _nameCtrl.text.trim(),
          'about': _aboutCtrl.text.trim(),
          'clinicAddress': _addressCtrl.text.trim(),
          'fee': double.tryParse(_feeCtrl.text) ?? 0,
        });
      }

      if (mounted) {
        setState(() { _user = updated; _editing = false; });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Profile saved!'),
            backgroundColor: AppColors.success,
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.all(Radius.circular(12))),
          ),
        );
      }
      ref.invalidate(currentUserProvider);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e'), backgroundColor: AppColors.error),
        );
      }
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  Future<void> _signOut() async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Sign Out'),
        content: const Text('Are you sure you want to sign out?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(ctx, true),
            style: ElevatedButton.styleFrom(backgroundColor: AppColors.error),
            child: const Text('Sign Out'),
          ),
        ],
      ),
    );
    if (confirm == true) {
      await AuthService().signOut();
    }
  }

  @override
  Widget build(BuildContext context) {
    final u = _user ?? ref.watch(currentUserProvider).value;
    if (u == null) return const Scaffold(body: Center(child: CircularProgressIndicator()));

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('My Profile'),
        actions: [
          if (!_editing)
            IconButton(
              icon: const Icon(Icons.edit_outlined),
              onPressed: () {
                if (u.role == 'doctor') _loadDoctorProfile(u.uid);
                setState(() => _editing = true);
              },
            )
          else
            TextButton(
              onPressed: () => setState(() => _editing = false),
              child: const Text('Cancel'),
            ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            // Avatar
            Center(
              child: Stack(
                children: [
                  AppAvatar(
                    imageUrl: u.photoUrl,
                    name: u.name,
                    radius: 56,
                  ),
                  Positioned(
                    bottom: 0,
                    right: 0,
                    child: GestureDetector(
                      onTap: _uploading ? null : _pickPhoto,
                      child: Container(
                        width: 34,
                        height: 34,
                        decoration: const BoxDecoration(
                          color: AppColors.primary,
                          shape: BoxShape.circle,
                        ),
                        child: _uploading
                            ? const Padding(
                                padding: EdgeInsets.all(8),
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  valueColor: AlwaysStoppedAnimation(Colors.white),
                                ),
                              )
                            : const Icon(Icons.camera_alt,
                                color: Colors.white, size: 18),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 12),
            if (!_editing) ...[
              Text(u.name,
                  style: const TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.w700,
                      color: AppColors.textPrimary)),
              const SizedBox(height: 4),
              Text(u.email,
                  style: const TextStyle(color: AppColors.textSecondary, fontSize: 14)),
              const SizedBox(height: 4),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
                decoration: BoxDecoration(
                  color: AppColors.primaryLight,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  u.role[0].toUpperCase() + u.role.substring(1),
                  style: const TextStyle(
                      color: AppColors.primary,
                      fontWeight: FontWeight.w600,
                      fontSize: 13),
                ),
              ),
            ],
            const SizedBox(height: 24),

            // Edit form / Info cards
            if (_editing) ...[
              AppTextField(
                label: 'Full Name',
                controller: _nameCtrl,
                prefix: const Icon(Icons.person_outline, color: AppColors.textSecondary),
                validator: (v) => v?.isEmpty == true ? 'Required' : null,
              ),
              const SizedBox(height: 14),
              AppTextField(
                label: 'Phone',
                controller: _phoneCtrl,
                keyboardType: TextInputType.phone,
                prefix: const Icon(Icons.phone_outlined, color: AppColors.textSecondary),
              ),
              if (u.role == 'doctor') ...[
                const SizedBox(height: 14),
                AppTextField(
                  label: 'About',
                  controller: _aboutCtrl,
                  maxLines: 3,
                  hint: 'Brief description about yourself and your practice',
                ),
                const SizedBox(height: 14),
                AppTextField(
                  label: 'Clinic Address',
                  controller: _addressCtrl,
                  prefix:
                      const Icon(Icons.location_on_outlined, color: AppColors.textSecondary),
                ),
                const SizedBox(height: 14),
                AppTextField(
                  label: 'Consultation Fee (Rs.)',
                  controller: _feeCtrl,
                  keyboardType: TextInputType.number,
                  prefix:
                      const Icon(Icons.payments_outlined, color: AppColors.textSecondary),
                ),
              ],
              const SizedBox(height: 24),
              AppButton(
                label: 'Save Changes',
                onPressed: _saveProfile,
                isLoading: _saving,
                icon: Icons.check,
              ),
            ] else ...[
              // Info cards
              _infoCard(Icons.phone_outlined, 'Phone',
                  u.phone.isEmpty ? 'Not set' : u.phone),
              _infoCard(Icons.email_outlined, 'Email', u.email),
              _infoCard(Icons.badge_outlined, 'Role',
                  u.role[0].toUpperCase() + u.role.substring(1)),
            ],

            const SizedBox(height: 24),
            const Divider(),
            const SizedBox(height: 8),

            // Settings
            _settingTile(
              icon: Icons.notifications_outlined,
              label: 'Notifications',
              onTap: () => _showComingSoon('Notification settings'),
            ),
            _settingTile(
              icon: Icons.privacy_tip_outlined,
              label: 'Privacy Policy',
              onTap: () => _showComingSoon('Privacy Policy'),
            ),
            _settingTile(
              icon: Icons.help_outline,
              label: 'Help & Support',
              onTap: () => _showComingSoon('Help & Support'),
            ),
            const SizedBox(height: 12),
            AppButton(
              label: 'Sign Out',
              onPressed: _signOut,
              isOutlined: true,
              icon: Icons.logout,
            ),
            const SizedBox(height: 24),
            const Text('MediConnect v1.0.0',
                style: TextStyle(color: AppColors.textHint, fontSize: 12)),
            const SizedBox(height: 8),
          ],
        ),
      ),
    );
  }

  Widget _infoCard(IconData icon, String label, String value) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      decoration: BoxDecoration(
        color: AppColors.card,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppColors.border, width: 0.8),
      ),
      child: Row(
        children: [
          Icon(icon, color: AppColors.primary, size: 20),
          const SizedBox(width: 12),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(label,
                  style: const TextStyle(
                      color: AppColors.textSecondary, fontSize: 12)),
              const SizedBox(height: 2),
              Text(value,
                  style: const TextStyle(
                      color: AppColors.textPrimary,
                      fontWeight: FontWeight.w500,
                      fontSize: 14)),
            ],
          ),
        ],
      ),
    );
  }

  Widget _settingTile({
    required IconData icon,
    required String label,
    required VoidCallback onTap,
  }) {
    return ListTile(
      contentPadding: EdgeInsets.zero,
      leading: Container(
        width: 40,
        height: 40,
        decoration: BoxDecoration(
          color: AppColors.primaryLight,
          borderRadius: BorderRadius.circular(10),
        ),
        child: Icon(icon, color: AppColors.primary, size: 20),
      ),
      title: Text(label,
          style: const TextStyle(
              fontWeight: FontWeight.w500, fontSize: 14, color: AppColors.textPrimary)),
      trailing: const Icon(Icons.chevron_right, color: AppColors.textHint),
      onTap: onTap,
    );
  }

  Future<void> _loadDoctorProfile(String uid) async {
    try {
      final doc = await FirestoreService().getDoctorById(uid);
      if (doc != null && mounted) {
        _aboutCtrl.text   = doc.about;
        _addressCtrl.text = doc.clinicAddress;
        _feeCtrl.text     = doc.fee.toInt().toString();
      }
    } catch (_) {}
  }

  void _showComingSoon(String feature) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('$feature coming soon!'),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
    );
  }
}
