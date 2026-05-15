#!/usr/bin/env python3
"""
Video Kitchen — Source Analyzer v3
Uses PySceneDetect for content-aware scene detection + cutlist generation.
Falls back to fixed-interval segmentation if no scenes detected.
Also extracts thumbnails, analyzes brightness/motion, extracts audio,
and outputs a structured manifest.json.

Usage:
  python3 analyze-source.py video.mp4
  python3 analyze-source.py video.mp4 --threshold 27 --min-scene 1.0 --fallback-interval 5
"""

import os, sys, json, subprocess, argparse
from pathlib import Path

# PySceneDetect
from scenedetect import SceneManager, open_video
from scenedetect.detectors import ContentDetector


def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.stdout.strip(), r.returncode


def probe(path):
    out, rc = run(f'ffprobe -v quiet -show_format -show_streams -print_format json "{path}"')
    return json.loads(out) if rc == 0 else None


# ─── PySceneDetect ───────────────────────────────────────────────

def detect_scenes(video_path, threshold=27.0, min_scene_len=1.0):
    """
    Run PySceneDetect ContentDetector on the source video.
    Returns list of (start_timecode, end_timecode) tuples in seconds.
    """
    print("🎬 Running PySceneDetect...")
    try:
        vid = open_video(video_path)
        scene_mgr = SceneManager()
        scene_mgr.add_detector(
            ContentDetector(
                threshold=threshold,
                min_scene_len=int(min_scene_len * vid.frame_rate)  # frames
            )
        )
        scene_mgr.detect_scenes(vid, show_progress=False)
        scene_list = scene_mgr.get_scene_list()

        scenes = []
        for i, (start_tc, end_tc) in enumerate(scene_list):
            scenes.append({
                'index': i,
                'start': round(start_tc.get_seconds(), 3),
                'end': round(end_tc.get_seconds(), 3),
                'duration': round(end_tc.get_seconds() - start_tc.get_seconds(), 3),
                'method': 'scenedetect',
            })

        if scenes:
            print(f"  ✂️  {len(scenes)} scenes detected (threshold={threshold}, min={min_scene_len}s)")
            # Print summary
            for s in scenes[:10]:
                print(f"     [{s['start']:7.1f}s → {s['end']:7.1f}s] {s['duration']:.1f}s")
            if len(scenes) > 10:
                print(f"     ... and {len(scenes) - 10} more")
        else:
            print(f"  ⚠️  No scenes detected — will use fixed-interval fallback")

        return scenes

    except Exception as e:
        print(f"  ⚠️  PySceneDetect error: {e} — falling back to fixed interval")
        return []


def build_fallback_clips(duration, interval):
    """Fixed-interval segmentation (legacy mode)."""
    clips = []
    count = int(duration / interval)
    for i in range(count):
        start = i * interval
        end = round(min((i + 1) * interval, duration), 2)
        clips.append({
            'index': i,
            'start': start,
            'end': end,
            'duration': round(end - start, 3),
            'method': 'fixed_interval',
        })
    # Remaining tail
    if clips and clips[-1]['end'] < duration - 0.5:
        tail_start = clips[-1]['end']
        clips.append({
            'index': len(clips),
            'start': tail_start,
            'end': round(duration, 2),
            'duration': round(duration - tail_start, 3),
            'method': 'fixed_interval',
        })
    return clips


# ─── Thumbnails & Analysis ────────────────────────────────────────

def extract_thumbnails_for_clips(video, outdir, clips):
    """Extract one mid-frame thumbnail per clip."""
    td = os.path.join(outdir, 'thumbnails')
    os.makedirs(td, exist_ok=True)
    thumbs = []

    for clip in clips:
        mid = clip['start'] + clip['duration'] / 2
        name = f"thumb_{clip['index']:03d}.jpg"
        path = os.path.join(td, name)
        run(f'ffmpeg -y -ss {mid} -i "{video}" -vframes 1 '
            f'-vf "scale=640:360:force_original_aspect_ratio=decrease,pad=640:360:(ow-iw)/2:(oh-ih)/2:black" '
            f'-q:v 4 "{path}" 2>/dev/null')
        if os.path.exists(path):
            thumbs.append({'index': clip['index'], 'time': round(mid, 2), 'path': path, 'file': name})
        else:
            thumbs.append({'index': clip['index'], 'time': round(mid, 2), 'path': None, 'file': None})

    found = sum(1 for t in thumbs if t['path'])
    print(f"  📷 {found}/{len(clips)} thumbnails extracted")
    return thumbs


def analyze_brightness(thumbs):
    """Get brightness for each thumbnail."""
    for t in thumbs:
        if not t['path'] or not os.path.exists(t['path']):
            t['brightness'] = None
            t['time_of_day'] = 'unknown'
            continue
        out, _ = run(f'ffmpeg -i "{t["path"]}" -vf "crop=iw*0.8:ih*0.8:iw*0.1:ih*0.1,signalstats" '
                     f'-frames:v 1 -f null - 2>&1 | grep YAVG')
        brightness = 0.5
        for line in out.split('\n'):
            if 'YAVG' in line:
                try:
                    val = line.split('YAVG:')[1].split()[0]
                    brightness = float(val) / 255.0
                except: pass
        t['brightness'] = round(brightness, 3)
        t['time_of_day'] = 'night' if brightness < 0.2 else 'dusk' if brightness < 0.35 else 'day'
    return thumbs


def analyze_motion(video, clips):
    """Estimate motion level per clip using frame difference."""
    for clip in clips:
        mid = clip['start'] + clip['duration'] / 2
        out, _ = run(f'ffmpeg -ss {max(0, mid - 0.3)} -t 0.6 -i "{video}" '
                     f'-vf "tblend=all_mode=difference128,signalstats" '
                     f'-frames:v 1 -f null - 2>&1 | grep YAVG')
        motion = 0.0
        for line in out.split('\n'):
            if 'YAVG' in line:
                try:
                    val = line.split('YAVG:')[1].split()[0]
                    motion = abs(float(val) - 128) / 128.0
                except: pass
        clip['motion'] = round(motion, 3)
    return clips


def extract_audio(video, outdir):
    """Extract audio as 16kHz mono WAV."""
    ap = os.path.join(outdir, 'audio.wav')
    run(f'ffmpeg -y -i "{video}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{ap}" 2>/dev/null')
    if os.path.exists(ap):
        mb = os.path.getsize(ap) / (1024*1024)
        print(f"  🎵 audio.wav ({mb:.1f}MB)")
        return ap
    return None


# ─── Manifest ──────────────────────────────────────────────────────

def build_manifest(video, outdir, probe_data, clips, thumbs, duration, audio_path, detection_method):
    """Build the final manifest.json with scene-based clips."""
    thumb_map = {t['index']: t for t in thumbs}

    manifest_clips = []
    for clip in clips:
        idx = clip['index']
        thumb = thumb_map.get(idx, {})
        manifest_clips.append({
            'id': f"clip_{idx:03d}",
            'source_start': clip['start'],
            'source_end': clip['end'],
            'duration': clip['duration'],
            'thumbnail': f"thumbnails/{thumb.get('file', '')}" if thumb.get('file') else None,
            'brightness': thumb.get('brightness'),
            'time_of_day': thumb.get('time_of_day'),
            'motion': clip.get('motion', 0),
            'detection_method': clip['method'],
            'teaser_rating': None,    # Filled by vision analysis
            'content_type': None,     # Filled by vision analysis
            'description': None,      # Filled by vision analysis
        })

    vs = None
    astream = None
    for s in probe_data.get('streams', []):
        if s.get('codec_type') == 'video' and not vs:
            vs = {'width': s.get('width'), 'height': s.get('height'),
                   'fps': s.get('r_frame_rate'), 'codec': s.get('codec_name')}
        if s.get('codec_type') == 'audio' and not astream:
            astream = {'codec': s.get('codec_name'), 'sample_rate': s.get('sample_rate')}

    manifest = {
        'version': 3,
        'source': {
            'file': os.path.basename(video),
            'duration': round(duration, 2),
            'video': vs,
            'audio': astream,
        },
        'analysis': {
            'detection_method': detection_method,
            'total_clips': len(manifest_clips),
            'has_thumbnails': any(t.get('file') for t in thumbs),
            'has_audio': audio_path is not None,
            'scenedetect_threshold': None,
            'scenedetect_min_scene': None,
        },
        'clips': manifest_clips,
        'audio_file': 'audio.wav' if audio_path else None,
        'transcription': None,
    }

    p = os.path.join(outdir, 'manifest.json')
    with open(p, 'w') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Also output a simple cutlist.txt for easy reference
    cutlist_path = os.path.join(outdir, 'cutlist.txt')
    with open(cutlist_path, 'w') as f:
        f.write(f"# Video Kitchen Cutlist — {os.path.basename(video)}\n")
        f.write(f"# {len(manifest_clips)} scenes via {detection_method}\n")
        f.write(f"# TIME_START  TIME_END  DURATION  CLIP_ID\n\n")
        for c in manifest_clips:
            f.write(f"{c['source_start']:8.2f}  {c['source_end']:8.2f}  {c['duration']:6.2f}  {c['id']}\n")

    print(f"\n📋 manifest.json → {len(manifest_clips)} clips via {detection_method}")
    print(f"📝 cutlist.txt → {cutlist_path}")
    return manifest


# ─── Main ──────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description='Video Kitchen — Source Analyzer v3 (PySceneDetect)')
    p.add_argument('video', help='Source video path')
    p.add_argument('-o', '--output', default=None, help='Output dir (default: <video_stem>_analysis/)')
    p.add_argument('-t', '--threshold', type=float, default=27.0,
                   help='PySceneDetect ContentDetector threshold (default: 27)')
    p.add_argument('--min-scene', type=float, default=1.0,
                   help='Minimum scene length in seconds (default: 1.0)')
    p.add_argument('--fallback-interval', type=float, default=5.0,
                   help='Fixed-interval fallback if no scenes detected (default: 5)')
    p.add_argument('--force-interval', action='store_true',
                   help='Force fixed-interval mode (skip PySceneDetect)')
    a = p.parse_args()

    video = os.path.abspath(a.video)
    if not os.path.exists(video):
        print(f"❌ Not found: {video}"); sys.exit(1)

    outdir = a.output or os.path.join(os.path.dirname(video), Path(video).stem + '_analysis')
    os.makedirs(outdir, exist_ok=True)

    print(f"🍳 Video Kitchen — Source Analyzer v3")
    print(f"   {video}")
    print(f"   → {outdir}\n")

    # Probe
    print("📡 Probing...")
    data = probe(video)
    dur = float(data['format']['duration'])
    for s in data['streams']:
        if s.get('codec_type') == 'video':
            print(f"   {s['width']}x{s['height']} {s['codec_name']} @ {s['r_frame_rate']}fps")
        if s.get('codec_type') == 'audio':
            print(f"   {s['codec_name']} {s['sample_rate']}Hz")
    print(f"   {dur:.1f}s\n")

    # Scene detection
    clips = []
    detection_method = 'fixed_interval'

    if not a.force_interval:
        scenes = detect_scenes(video, threshold=a.threshold, min_scene_len=a.min_scene)
        if scenes:
            clips = scenes
            detection_method = 'scenedetect'

    if not clips:
        print(f"📏 Using fixed-interval mode ({a.fallback_interval}s)")
        clips = build_fallback_clips(dur, a.fallback_interval)
        detection_method = 'fixed_interval'

    # Thumbnails
    print("\n📷 Extracting thumbnails...")
    thumbs = extract_thumbnails_for_clips(video, outdir, clips)

    # Brightness
    print("☀️  Analyzing brightness...")
    thumbs = analyze_brightness(thumbs)

    # Motion
    print("🏃 Analyzing motion...")
    clips = analyze_motion(video, clips)

    # Audio
    print("🔊 Extracting audio...")
    audio = extract_audio(video, outdir)

    # Manifest
    print("\n📋 Building manifest...")
    manifest = build_manifest(video, outdir, data, clips, thumbs, dur, audio, detection_method)

    # Store threshold/min_scene in manifest if scenedetect was used
    if detection_method == 'scenedetect':
        manifest['analysis']['scenedetect_threshold'] = a.threshold
        manifest['analysis']['scenedetect_min_scene'] = a.min_scene
        with open(os.path.join(outdir, 'manifest.json'), 'w') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Done! {len(clips)} clips via {detection_method}")
    print("   Next:")
    print("   1. Run vision analysis on thumbnails (automatic or manual)")
    print("   2. Transcribe audio: bash openai-whisper-api/scripts/transcribe.sh analysis/audio.wav")
    print("   3. Feed manifest to recipe skill → build HyperFrames composition")


if __name__ == '__main__':
    main()
