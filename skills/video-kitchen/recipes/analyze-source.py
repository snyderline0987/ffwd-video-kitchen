#!/usr/bin/env python3
"""
Video Kitchen — Source Analyzer v2
Splits source video into segments, extracts thumbnails, analyzes brightness/motion,
extracts audio, and outputs a structured manifest.json for the recipe skill.

Usage:
  python3 analyze-source.py video.mp4
  python3 analyze-source.py video.mp4 --interval 3 --output ./analysis
"""

import os, sys, json, subprocess, argparse
from pathlib import Path


def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.stdout.strip(), r.returncode


def probe(path):
    out, rc = run(f'ffprobe -v quiet -show_format -show_streams -print_format json "{path}"')
    return json.loads(out) if rc == 0 else None


def extract_thumbnails(video, outdir, interval, duration):
    """Extract mid-frame thumbnails for each segment."""
    td = os.path.join(outdir, 'thumbnails')
    os.makedirs(td, exist_ok=True)
    count = int(duration / interval)
    thumbs = []

    for i in range(count):
        t = i * interval + interval / 2
        name = f"thumb_{i:03d}.jpg"
        path = os.path.join(td, name)
        run(f'ffmpeg -y -ss {t} -i "{video}" -vframes 1 '
            f'-vf "scale=640:360:force_original_aspect_ratio=decrease,pad=640:360:(ow-iw)/2:(oh-ih)/2:black" '
            f'-q:v 4 "{path}" 2>/dev/null')
        thumbs.append({'index': i, 'time': round(t, 2), 'path': path, 'file': name})

    print(f"  📷 {len(thumbs)} thumbnails extracted")
    return thumbs


def analyze_brightness(thumbs):
    """Get brightness for each thumbnail."""
    for t in thumbs:
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


def analyze_motion(video, thumbs, interval):
    """Estimate motion level per segment using frame difference."""
    for t in thumbs:
        mid = t['time']
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
        t['motion'] = round(motion, 3)
    return thumbs


def extract_audio(video, outdir):
    """Extract audio as 16kHz mono WAV."""
    ap = os.path.join(outdir, 'audio.wav')
    run(f'ffmpeg -y -i "{video}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{ap}" 2>/dev/null')
    if os.path.exists(ap):
        mb = os.path.getsize(ap) / (1024*1024)
        print(f"  🎵 audio.wav ({mb:.1f}MB)")
        return ap
    return None


def build_manifest(video, outdir, probe_data, thumbs, interval, duration, audio_path):
    clips = []
    for t in thumbs:
        i = t['index']
        clips.append({
            'id': f"clip_{i:03d}",
            'source_start': i * interval,
            'source_end': round(min((i + 1) * interval, duration), 2),
            'duration': round(min(interval, duration - i * interval), 2),
            'thumbnail': f"thumbnails/{t['file']}",
            'brightness': t['brightness'],
            'time_of_day': t['time_of_day'],
            'motion': t.get('motion', 0),
            'teaser_rating': None,  # Filled by vision analysis
            'content_type': None,   # Filled by vision analysis: "talking_head" / "crowd" / "action"
            'description': None,    # Filled by vision analysis
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
        'version': 2,
        'source': {
            'file': os.path.basename(video),
            'duration': round(duration, 2),
            'video': vs,
            'audio': astream,
        },
        'analysis': {
            'interval': interval,
            'total_clips': len(clips),
            'has_thumbnails': True,
            'has_audio': audio_path is not None,
        },
        'clips': clips,
        'audio_file': 'audio.wav' if audio_path else None,
        'transcription': None,
    }

    p = os.path.join(outdir, 'manifest.json')
    with open(p, 'w') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"\n📋 manifest.json → {len(clips)} clips analyzed")
    return manifest


def main():
    p = argparse.ArgumentParser(description='Video Kitchen Source Analyzer v2')
    p.add_argument('video', help='Source video path')
    p.add_argument('-o', '--output', default=None, help='Output dir')
    p.add_argument('-i', '--interval', type=float, default=5, help='Segment interval in seconds (default: 5)')
    a = p.parse_args()

    video = os.path.abspath(a.video)
    if not os.path.exists(video):
        print(f"❌ Not found: {video}"); sys.exit(1)

    outdir = a.output or os.path.join(os.path.dirname(video), Path(video).stem + '_analysis')
    os.makedirs(outdir, exist_ok=True)

    print(f"🍳 Video Kitchen — Source Analyzer v2")
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

    # Thumbnails
    print("📷 Extracting thumbnails...")
    thumbs = extract_thumbnails(video, outdir, a.interval, dur)

    # Brightness
    print("☀️  Analyzing brightness...")
    thumbs = analyze_brightness(thumbs)

    # Motion
    print("🏃 Analyzing motion...")
    thumbs = analyze_motion(video, thumbs, a.interval)

    # Audio
    print("🔊 Extracting audio...")
    audio = extract_audio(video, outdir)

    # Manifest
    print("\n📋 Building manifest...")
    build_manifest(video, outdir, data, thumbs, a.interval, dur, audio)

    print("\n✅ Done! Next:")
    print("   1. Run vision analysis on thumbnails (automatic or manual)")
    print("   2. Transcribe audio: npx hyperframes transcribe analysis/audio.wav")
    print("   3. Feed manifest to recipe skill → build HyperFrames composition")


if __name__ == '__main__':
    main()
