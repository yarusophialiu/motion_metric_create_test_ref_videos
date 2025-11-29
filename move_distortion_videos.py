import os
import shutil
import argparse

# a folder distortion_videos have scene/levelx/videox.mp4 x is 0-2, 
# move the videos to D:\motion-metric\experiment_videos with structure like 
# experiment_videos\scene\distortion\levelx/videox.mp4



def move_videos(src_root, dst_root, distortion, dryrun=False):
    # Walk over all scenes inside distortion_videos
    for scene_name in os.listdir(src_root):
        scene_path = os.path.join(src_root, scene_name)
        if not os.path.isdir(scene_path):
            continue  # skip non-folders

        # Inside each scene: level0, level1, level2, ...
        for level_name in os.listdir(scene_path):
            level_path = os.path.join(scene_path, level_name)
            if not os.path.isdir(level_path):
                continue

            # Destination directory: experiment_videos\scene\distortion\levelx
            dst_level_dir = os.path.join(dst_root, scene_name, distortion, level_name)

            # Create destination directory (or log in dryrun)
            if dryrun:
                print(f"[DRYRUN] Would create directory: {dst_level_dir}")
            else:
                os.makedirs(dst_level_dir, exist_ok=True)

            # For each video file in this level
            for fname in os.listdir(level_path):
                if not fname.lower().endswith(".mp4"):
                    continue

                # Expect names like video0.mp4, video1.mp4, video2.mp4
                stem, ext = os.path.splitext(fname)
                if not stem.startswith("video"):
                    print(f"[WARN] Skipping unexpected file name: {fname}")
                    continue

                suffix = stem[5:]  # part after "video"
                if not suffix.isdigit():
                    print(f"[WARN] Skipping unexpected file name: {fname}")
                    continue

                new_name = f"video_{suffix}{ext}"  # video_0.mp4 etc.

                src_file = os.path.join(level_path, fname)
                dst_file = os.path.join(dst_level_dir, new_name)

                if dryrun:
                    print(f"[DRYRUN] Would move: {src_file} -> {dst_file}")
                else:
                    # Safety: warn if overwriting
                    if os.path.exists(dst_file):
                        print(f"[WARN] Destination already exists, skipping: {dst_file}")
                        continue
                    print(f"Moving: {src_file} -> {dst_file}")
                    shutil.move(src_file, dst_file)

# python move_distortion_videos.py --dryrun
# python move_distortion_videos.py --dryrun  # no dryrun
if __name__ == "__main__":
    distortion = 'motion_noise'
    parser = argparse.ArgumentParser(description="Move distortion videos into experiment_videos structure.")
    parser.add_argument(
        "--src",
        default=f"D:/{distortion}_videos/{distortion}_videos",
        help="Source root folder (default: distortion_videos in current directory)."
    )
    parser.add_argument(
        "--dst",
        default=r"D:\motion-metric\experiment_videos",
        help="Destination root folder (default: D:\\motion-metric\\experiment_videos)."
    )
    parser.add_argument(
        "--dryrun",
        action="store_true",
        help="Print what would be done, but do not move any files."
    )

    args = parser.parse_args()
    move_videos(args.src, args.dst, distortion, dryrun=args.dryrun)
