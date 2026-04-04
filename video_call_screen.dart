import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:agora_rtc_engine/agora_rtc_engine.dart';
import '../../core/constants/app_colors.dart';
import '../../providers/providers.dart';

// ─── IMPORTANT: Replace with your Agora App ID ───────────────────────────────
const String _agoraAppId = 'YOUR_AGORA_APP_ID';
// For production: generate tokens via Firebase Cloud Functions
// For testing/demo: use empty string with no token (disable token in Agora console)

class VideoCallScreen extends ConsumerStatefulWidget {
  final String appointmentId;
  final String channelName;

  const VideoCallScreen({
    super.key,
    required this.appointmentId,
    required this.channelName,
  });

  @override
  ConsumerState<VideoCallScreen> createState() => _VideoCallScreenState();
}

class _VideoCallScreenState extends ConsumerState<VideoCallScreen> {
  RtcEngine? _engine;
  int? _remoteUid;
  bool _localUserJoined = false;
  bool _muted           = false;
  bool _cameraOff       = false;
  bool _speakerOn       = true;
  bool _initialized     = false;
  String? _error;
  int _callDuration     = 0;
  late final _timer = Stream.periodic(const Duration(seconds: 1), (i) => i + 1)
      .listen((sec) { if (mounted) setState(() => _callDuration = sec); });

  @override
  void initState() {
    super.initState();
    SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
    _initAgora();
  }

  @override
  void dispose() {
    _timer.cancel();
    _engine?.leaveChannel();
    _engine?.release();
    SystemChrome.setPreferredOrientations(DeviceOrientation.values);
    super.dispose();
  }

  Future<void> _initAgora() async {
    // Check App ID is set
    if (_agoraAppId == 'YOUR_AGORA_APP_ID' || _agoraAppId.isEmpty) {
      setState(() => _error =
          'Agora App ID not configured.\n\nReplace YOUR_AGORA_APP_ID in video_call_screen.dart with your real App ID from agora.io');
      return;
    }

    // Request permissions
    final statuses = await [Permission.camera, Permission.microphone].request();
    final camOk = statuses[Permission.camera]?.isGranted ?? false;
    final micOk = statuses[Permission.microphone]?.isGranted ?? false;
    if (!camOk || !micOk) {
      setState(() => _error = 'Camera and microphone permissions are required for video calls.');
      return;
    }

    try {
      _engine = createAgoraRtcEngine();
      await _engine!.initialize(RtcEngineContext(appId: _agoraAppId));

      _engine!.registerEventHandler(RtcEngineEventHandler(
        onJoinChannelSuccess: (connection, elapsed) {
          if (mounted) setState(() => _localUserJoined = true);
        },
        onUserJoined: (connection, remoteUid, elapsed) {
          if (mounted) setState(() => _remoteUid = remoteUid);
        },
        onUserOffline: (connection, remoteUid, reason) {
          if (mounted) setState(() => _remoteUid = null);
        },
        onLeaveChannel: (connection, stats) {
          if (mounted) context.pop();
        },
        onError: (err, msg) {
          if (mounted) setState(() => _error = 'Call error: $msg');
        },
      ));

      await _engine!.setClientRole(role: ClientRoleType.clientRoleBroadcaster);
      await _engine!.enableVideo();
      await _engine!.enableAudio();
      await _engine!.startPreview();
      await _engine!.setEnableSpeakerphone(_speakerOn);

      await _engine!.joinChannel(
        token: '',  // Replace with generated token for production
        channelId: widget.channelName,
        uid: 0,
        options: const ChannelMediaOptions(
          autoSubscribeAudio: true,
          autoSubscribeVideo: true,
          publishCameraTrack: true,
          publishMicrophoneTrack: true,
          clientRoleType: ClientRoleType.clientRoleBroadcaster,
        ),
      );

      if (mounted) setState(() => _initialized = true);
    } catch (e) {
      if (mounted) setState(() => _error = 'Failed to initialize call: $e');
    }
  }

  Future<void> _toggleMute() async {
    setState(() => _muted = !_muted);
    await _engine?.muteLocalAudioStream(_muted);
  }

  Future<void> _toggleCamera() async {
    setState(() => _cameraOff = !_cameraOff);
    await _engine?.muteLocalVideoStream(_cameraOff);
  }

  Future<void> _toggleSpeaker() async {
    setState(() => _speakerOn = !_speakerOn);
    await _engine?.setEnableSpeakerphone(_speakerOn);
  }

  Future<void> _switchCamera() async {
    await _engine?.switchCamera();
  }

  Future<void> _endCall() async {
    await _engine?.leaveChannel();
    if (mounted) context.pop();
  }

  String get _durationLabel {
    final m = (_callDuration ~/ 60).toString().padLeft(2, '0');
    final s = (_callDuration % 60).toString().padLeft(2, '0');
    return '$m:$s';
  }

  @override
  Widget build(BuildContext context) {
    // Error state
    if (_error != null) {
      return Scaffold(
        backgroundColor: Colors.black,
        body: SafeArea(
          child: Center(
            child: Padding(
              padding: const EdgeInsets.all(32),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.videocam_off, color: Colors.white70, size: 64),
                  const SizedBox(height: 20),
                  Text(
                    _error!,
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: Colors.white70, fontSize: 15, height: 1.6),
                  ),
                  const SizedBox(height: 32),
                  ElevatedButton.icon(
                    onPressed: () => context.pop(),
                    icon: const Icon(Icons.arrow_back),
                    label: const Text('Go Back'),
                    style: ElevatedButton.styleFrom(backgroundColor: AppColors.error),
                  ),
                ],
              ),
            ),
          ),
        ),
      );
    }

    // Loading state
    if (!_initialized) {
      return Scaffold(
        backgroundColor: Colors.black,
        body: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const CircularProgressIndicator(color: Colors.white),
              const SizedBox(height: 20),
              const Text('Connecting...', style: TextStyle(color: Colors.white, fontSize: 16)),
            ],
          ),
        ),
      );
    }

    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Stack(
          children: [
            // Remote video (full screen)
            _remoteUid != null
                ? AgoraVideoView(
                    controller: VideoViewController.remote(
                      rtcEngine: _engine!,
                      canvas: VideoCanvas(uid: _remoteUid),
                      connection: RtcConnection(channelId: widget.channelName),
                    ),
                  )
                : Center(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.person, color: Colors.white54, size: 80),
                        const SizedBox(height: 16),
                        const Text('Waiting for the other person...',
                            style: TextStyle(color: Colors.white70, fontSize: 15)),
                        const SizedBox(height: 8),
                        Text(_durationLabel,
                            style: const TextStyle(
                                color: Colors.white54, fontSize: 13)),
                      ],
                    ),
                  ),

            // Local video (PiP, top-right)
            if (_localUserJoined && !_cameraOff)
              Positioned(
                top: 16,
                right: 16,
                child: GestureDetector(
                  onTap: _switchCamera,
                  child: Container(
                    width: 110,
                    height: 150,
                    decoration: BoxDecoration(
                      color: Colors.black,
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(color: Colors.white30, width: 1),
                    ),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(13),
                      child: AgoraVideoView(
                        controller: VideoViewController(
                          rtcEngine: _engine!,
                          canvas: const VideoCanvas(uid: 0),
                        ),
                      ),
                    ),
                  ),
                ),
              ),

            // Camera-off overlay on PiP
            if (_localUserJoined && _cameraOff)
              Positioned(
                top: 16,
                right: 16,
                child: Container(
                  width: 110,
                  height: 150,
                  decoration: BoxDecoration(
                    color: Colors.grey[900],
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: Colors.white30, width: 1),
                  ),
                  child: const Center(
                    child: Icon(Icons.videocam_off, color: Colors.white54, size: 32),
                  ),
                ),
              ),

            // Top bar — duration + channel name
            Positioned(
              top: 0,
              left: 0,
              right: 0,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [Colors.black.withOpacity(0.6), Colors.transparent],
                  ),
                ),
                child: Row(
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Text('Video Consultation',
                            style: TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.w600,
                                fontSize: 16)),
                        Text(
                          _remoteUid != null ? 'Connected · $_durationLabel' : 'Waiting...',
                          style: const TextStyle(color: Colors.white70, fontSize: 13),
                        ),
                      ],
                    ),
                    const Spacer(),
                    if (_remoteUid != null)
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: AppColors.success.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: AppColors.success, width: 0.5),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Container(
                              width: 6,
                              height: 6,
                              decoration: const BoxDecoration(
                                color: AppColors.success,
                                shape: BoxShape.circle,
                              ),
                            ),
                            const SizedBox(width: 5),
                            const Text('Live',
                                style: TextStyle(
                                    color: AppColors.success,
                                    fontSize: 12,
                                    fontWeight: FontWeight.w600)),
                          ],
                        ),
                      ),
                  ],
                ),
              ),
            ),

            // Bottom controls
            Positioned(
              bottom: 0,
              left: 0,
              right: 0,
              child: Container(
                padding: const EdgeInsets.fromLTRB(24, 20, 24, 32),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.bottomCenter,
                    end: Alignment.topCenter,
                    colors: [Colors.black.withOpacity(0.8), Colors.transparent],
                  ),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _controlBtn(
                      icon: _muted ? Icons.mic_off : Icons.mic,
                      label: _muted ? 'Unmute' : 'Mute',
                      onTap: _toggleMute,
                      active: !_muted,
                    ),
                    _controlBtn(
                      icon: _cameraOff ? Icons.videocam_off : Icons.videocam,
                      label: _cameraOff ? 'Cam On' : 'Cam Off',
                      onTap: _toggleCamera,
                      active: !_cameraOff,
                    ),
                    _controlBtn(
                      icon: Icons.flip_camera_ios,
                      label: 'Flip',
                      onTap: _switchCamera,
                      active: true,
                    ),
                    _controlBtn(
                      icon: _speakerOn ? Icons.volume_up : Icons.volume_off,
                      label: _speakerOn ? 'Speaker' : 'Earpiece',
                      onTap: _toggleSpeaker,
                      active: _speakerOn,
                    ),
                    // End call button
                    GestureDetector(
                      onTap: _endCall,
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Container(
                            width: 60,
                            height: 60,
                            decoration: const BoxDecoration(
                              color: AppColors.error,
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(Icons.call_end,
                                color: Colors.white, size: 28),
                          ),
                          const SizedBox(height: 6),
                          const Text('End',
                              style: TextStyle(
                                  color: Colors.white70, fontSize: 12)),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _controlBtn({
    required IconData icon,
    required String label,
    required VoidCallback onTap,
    required bool active,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 52,
            height: 52,
            decoration: BoxDecoration(
              color: active ? Colors.white.withOpacity(0.15) : Colors.white.withOpacity(0.08),
              shape: BoxShape.circle,
              border: Border.all(
                color: active ? Colors.white30 : Colors.white12,
                width: 0.8,
              ),
            ),
            child: Icon(icon,
                color: active ? Colors.white : Colors.white54, size: 22),
          ),
          const SizedBox(height: 6),
          Text(label,
              style: TextStyle(
                  color: active ? Colors.white70 : Colors.white38,
                  fontSize: 11)),
        ],
      ),
    );
  }
}
