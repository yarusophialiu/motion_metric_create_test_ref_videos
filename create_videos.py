import subprocess
from pathlib import Path
import re
import math

SRC_ROOT = Path(r"C:\Users\15142\Projects\motion-metric\all_sequences")
DST_ROOT = Path(r"C:\Users\15142\Projects\motion-metric\all_sequences_videos")

FRAMERATE = 120  # your chosen fps
DURATION_SEC = 2
FRAMES_PER_VIDEO = int(FRAMERATE * DURATION_SEC)
EXT = ".png"

NUM_STEM = re.compile(r"^(\d+)$")  # match 00000, 00001, etc.


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

    rel = folder.relative_to(SRC_ROOT)
    out_dir = DST_ROOT / rel
    out_dir.mkdir(parents=True, exist_ok=True)

    input_pattern = folder / f"%0{pad_width}d{EXT}"

    for i in range(num_videos):
        start_idx = i * FRAMES_PER_VIDEO
        # start_number = indices[start_idx]
        out_path = out_dir / f"video_{i}.mp4"
        
        # hevc lossless
        cmd = [
            'ffmpeg', '-y',
            '-framerate', str(FRAMERATE),
            '-i', str(input_pattern),
            '-c:v', 'libx265',
            '-preset', 'slow',
            '-pix_fmt', 'yuv444p',
            '-x265-params', 'lossless=1:profile=main444-8',
            str(out_path),
        ]

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print(f"[OK] {folder} -> {out_path.name} ({FRAMES_PER_VIDEO} frames, {FRAMERATE} fps)")
        except subprocess.CalledProcessError as e:
            print(f"[ERR] FFmpeg failed in {folder}: {e}")

    return True, f"{num_videos} video(s) created"


def main():
    for folder in SRC_ROOT.rglob("*"):
        if folder.is_dir():
            make_videos_for_folder(folder)


if __name__ == "__main__":
    main()
