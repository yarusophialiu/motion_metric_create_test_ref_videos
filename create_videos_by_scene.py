import subprocess
from pathlib import Path

# =============================
# 🔧 USER CONFIGURATION
# =============================
input_root = Path(r"D:\motion-metric\all_sequences_pilot")
output_root = Path(r"D:\motion-metric\pilot-videos")
scene = "zeroday"       # e.g. "bistro_interior" or "zeroday" "subway"

framerate = 240                 # input framerate
start_number = 0              # first frame number (matches filenames like %05d.png)
vframes = 720                   # number of frames to encode
video_index = 0                 # video_0.mp4
ffmpeg_path = "ffmpeg"          # or r"C:\ffmpeg\bin\ffmpeg.exe"
input_pattern = "%05d.png"      # change if your numbering width differs
overwrite = False # True                # set False to skip existing outputs
# =============================
# ffmpeg -n -framerate 240 -start_number 0 -i "%05d.png" -vframes 720 -c:v libx265 -preset slow -pix_fmt yuv444p -x265-params "lossless=1:profile=main444-8" "../video_0.mp4"
# ffmpeg -n -framerate 240 -start_number 50 -i "%05d.png" -vframes 720 -c:v libx265 -preset slow -pix_fmt yuv444p -x265-params "lossless=1:profile=main444-8" "../video_1.mp4"


scene_dir = input_root / scene
if not scene_dir.exists():
    raise SystemExit(f"Scene folder not found: {scene_dir}")

# Find every directory under the scene that directly contains PNG frames
# (works for: scene/reference/, scene/<distortion>/<level>/)
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
    raise SystemExit(f"No PNG-containing folders found under: {scene_dir}")

failed = []
for fdir in candidate_dirs:
    print("fdir", fdir)

    # if Path(fdir) != target:
    #     print("skip", fdir)
    #     continue

    print("MATCH!", fdir)
    # Mirror folder structure relative to the scene folder
    rel = fdir.relative_to(scene_dir)        # e.g. "reference" or "H264/level1"
    out_dir = output_root / scene / rel
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"video_{video_index}.mp4"
    print(f'out_path {out_path}')

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
        # pass
    except subprocess.CalledProcessError as e:
        failed.append(fdir)
        print(f"❌ FAILED ({fdir}) with error code {e.returncode}. Continuing...")

print(f'failed {failed}')
print("\n✅ Done.")
