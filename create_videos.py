import subprocess
from pathlib import Path
import re
import math
import time


# make videos using all frames
# SRC_ROOT = Path(r"C:\Users\15142\Projects\motion-metric\all_sequences")
# DST_ROOT = Path(r"C:\Users\15142\Projects\motion-metric\all_sequences_videos")
base_dir = r'D:\motion-metric'
SRC_ROOT = Path(f"{base_dir}/all_sequences_pilot")
DST_ROOT = Path(f"{base_dir}/pilot_videos_crf5")

FRAMERATE = 240  
DURATION_SEC = 5
FRAMES_PER_VIDEO = int(FRAMERATE * DURATION_SEC)
EXT = ".png"

NUM_STEM = re.compile(r"^(\d+)$")  # match 00000, 00001, etc.

skipped_videos = []

def detect_sequence(folder: Path):
    """Find numeric PNG frames and return sorted indices and padding width."""
    frames = []
    pad_width = None
    for p in folder.iterdir():
        if p.suffix.lower() != EXT or not p.is_file():
            continue
        m = NUM_STEM.match(p.stem)
        if not m:
            continue
        idx_str = m.group(1)
        if pad_width is None:
            pad_width = len(idx_str)
        if len(idx_str) != pad_width:
            continue
        frames.append((int(idx_str), p))
    if not frames:
        return [], None
    frames.sort(key=lambda x: x[0])
    indices = [i for i, _ in frames]
    return indices, pad_width


def make_videos_for_folder(folder: Path):
    indices, pad_width = detect_sequence(folder)
    if not indices:
        return False, "No numbered PNG frames found"

    total_frames = len(indices)
    num_videos = math.ceil(total_frames / FRAMES_PER_VIDEO)
    print(f'Num of videos per scene: {num_videos}')

    rel = folder.relative_to(SRC_ROOT)
    out_dir = DST_ROOT / rel
    out_dir.mkdir(parents=True, exist_ok=True)

    input_pattern = folder / f"%0{pad_width}d{EXT}"

    for i in range(num_videos):
        start_idx = i * FRAMES_PER_VIDEO
        # start_number = indices[start_idx]
        out_path = out_dir / f"video_{i}.mp4"
        if out_path.exists():
            print(f"[SKIP] {out_path} already exists")
            skipped_videos.append(out_path)   # or append(i) / out_path.name, as you prefer
            continue
        
        # # # hevc lossless
        # cmd = [
        #     'ffmpeg', '-y',
        #     '-framerate', str(FRAMERATE),
        #     '-i', str(input_pattern),
        #     '-c:v', 'libx265',
        #     '-preset', 'slow',
        #     '-pix_fmt', 'yuv444p',
        #     '-x265-params', 'lossless=1:profile=main444-8',
        #     str(out_path),
        # ]

        # crf visually lossless
        cmd = [
            'ffmpeg', '-y',
            '-framerate', str(FRAMERATE),
            '-i', str(input_pattern),
            "-c:v", "libx265",
            "-preset", "slow",
            "-pix_fmt", "yuv444p",
            "-x265-params", "crf=5:profile=main444-8",
            str(out_path),
        ]

        # # chroma subsampling, further filesize reduction
        # cmd = [
        #     'ffmpeg', '-y',
        #     '-framerate', str(FRAMERATE),
        #     '-i', str(input_pattern),
        #     "-c:v", "libx265",
        #     "-preset", "slow",
        #     "-pix_fmt", "yuv420p",
        #     "-x265-params", "profile=main",
        #     str(out_path),
        # ]



        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print(f"[OK] {folder} -> {out_path.name} ({FRAMES_PER_VIDEO} frames, {FRAMERATE} fps)")
            print(f'out_path {out_path}\n')
        except subprocess.CalledProcessError as e:
            print(f"[ERR] FFmpeg failed in {folder}: {e}")

    return True, f"{num_videos} video(s) created"


def main():
    for folder in SRC_ROOT.rglob("*"):
        if folder.is_dir():
            folder_name = folder.name.lower()
            skip_keywords = ("restir", "motion_noise", "motion_resolution")

            # if any(keyword in folder_name for keyword in skip_keywords):
            #     print(f"Skipping folder: {folder}")
            #     continue

            # # if "restir" in str(folder).lower() or "motion_noise" in str(folder).lower() or "motion_resolution" in str(folder).lower():
            # if "stutter" in str(folder).lower():
            #     # Optional: see what you're skipping
            #     # print(f"Skipping folder: {folder}")
            #     print(f"\nProcessing folder: {folder}")
            #     make_videos_for_folder(folder)

            # print(f"Skipping folder: {folder}")
            print(f"\nProcessing folder: {folder}")
            make_videos_for_folder(folder)


if __name__ == "__main__":
    start_time = time.time()

    main()
    print(f'Skipped {len(skipped_videos)} videos.')
    
    elapsed = time.time() - start_time
    print(f"Skipped {len(skipped_videos)} videos.")
    print(f"Total time: {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")


# D:\motion-metric\all_sequences have scene_name/distortion_name/level_name frames in png format, go through all folders that have frames, run ffmpeg "-c:v", "libx265", 
# "-preset", "slow",
# "-pix_fmt", "yuv444p",
# "-x265-params", "lossless=1:profile=main444-8",
# f"{save_path}/video0.mkv"] 