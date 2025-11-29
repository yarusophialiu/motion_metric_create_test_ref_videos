import subprocess
from pathlib import Path

# create pilot videos for given jobs
# =============================
# 🔧 GLOBAL SETTINGS (shared)
# =============================
input_root = Path(r"D:\motion-metric\all_sequences_pilot")
output_root = Path(r"D:\motion-metric\pilot_videos")
ffmpeg_path = "ffmpeg"          # or r"C:\ffmpeg\bin\ffmpeg.exe"
input_pattern = "%05d.png"
framerate = 240
overwrite = False               # True to overwrite existing outputs
# =============================

# Jobs: (scene, start_number, vframes, video_index)
jobs = [
    ("zeroday",          50,  720, 1),
    ("zeroday",         280,  720, 2),
    ("bistro_interior",   0,  617, 0),
    ("bistro_interior", 400,  561, 1),
    ("bistro_interior", 616,  583, 2),
    ("subway",            0,  501, 0),
    ("subway",            0, 1199, 1),
    ("subway",            0,  876, 2),
]

def run_job(scene: str, start_number: int, vframes: int, video_index: int):
    scene_dir = input_root / scene
    if not scene_dir.exists():
        print(f"❌ Scene folder not found: {scene_dir}")
        return []

    # Find every directory under the scene that directly contains PNG frames
    candidate_dirs = []
    for d in scene_dir.rglob("*"):
        if d.is_dir():
            try:
                has_png = any(p.suffix.lower() == ".png" for p in d.iterdir())
            except PermissionError:
                has_png = False
            if has_png:
                candidate_dirs.append(d)
    candidate_dirs = sorted(candidate_dirs)

    if not candidate_dirs:
        print(f"❌ No PNG-containing folders found under: {scene_dir}")
        return []

    print(f"\n================= SCENE: {scene}  (start={start_number}, vframes={vframes}, index={video_index}) =================")
    failed = []

    for fdir in candidate_dirs:
        # Mirror folder structure relative to the scene folder
        rel = fdir.relative_to(scene_dir)        # e.g. "reference" or "H264/level1"
        out_dir = output_root / scene / rel
        out_dir.mkdir(parents=True, exist_ok=True)

        out_path = out_dir / f"video_{video_index}.mp4"

        if out_path.exists() and not overwrite:
            print(f"⏩ Skipping existing: {out_path}")
            continue

        cmd = [
            ffmpeg_path,
            "-y" if overwrite else "-n",
            "-framerate", str(framerate),
            "-start_number", str(start_number),
            "-i", input_pattern,
            "-vframes", str(vframes),
            "-c:v", "libx265",
            "-preset", "slow",
            "-pix_fmt", "yuv444p",
            "-x265-params", "lossless=1:profile=main444-8",
            str(out_path)
        ]

        print(f"\n=== Encoding ==="
              f"\nFrames dir: {fdir}"
              f"\nOutput:     {out_path}"
              f"\nCommand:    {' '.join(map(str, cmd))}\n")

        try:
            subprocess.run(cmd, check=True, cwd=fdir)
        except subprocess.CalledProcessError as e:
            failed.append(fdir)
            print(f"❌ FAILED ({fdir}) with error code {e.returncode}. Continuing...")

    return failed

def main():
    all_failed = []
    for scene, start_number, vframes, video_index in jobs:
        failed = run_job(scene, start_number, vframes, video_index)
        if failed:
            all_failed.extend([(scene, d) for d in failed])

    if all_failed:
        print("\n⚠️  Some jobs failed:")
        for scene, d in all_failed:
            print(f" - {scene}: {d}")
    else:
        print("\n✅ All jobs completed without ffmpeg errors.")

if __name__ == "__main__":
    main()
