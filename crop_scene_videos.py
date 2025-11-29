import os, subprocess, sys

SRC = r"D:\motion-metric\all_sequences_videos\zeroday_full"
DST = r"D:\motion-metric\all_sequences_videos\zeroday_cropped"

def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

def main():
    if not os.path.isdir(SRC):
        print(f"Source folder not found: {SRC}", file=sys.stderr)
        sys.exit(1)
    ensure_dir(DST)
    print(f'SRC {SRC}')

    for root, dirs, files in os.walk(SRC):
        print(files)
        if "video_0.mp4" in files:
            in_file = os.path.join(root, "video_0.mp4")
            rel = os.path.relpath(root, SRC)          # path under zeroday
            out_dir = os.path.join(DST, rel)
            ensure_dir(out_dir)
            out_file = os.path.join(out_dir, "video_0.mp4")
            print(f'out_file {out_file}')

            cmd = ["ffmpeg", "-y", "-ss", "0", "-to", "3", "-i", in_file, "-c", "copy", out_file]
            # cmd = ["ffmpeg", "-y", "-ss", "2", "-to", "5", "-i", in_file, "-c", "copy", out_file]
            print(" ".join(cmd))
            subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()
