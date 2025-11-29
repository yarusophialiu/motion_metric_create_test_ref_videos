import os
import shutil
import argparse


# Source: D:\motion-metric\all_sequences_pilot\scene\distortion\level_name\00000.png
# Destination: D:\motion-metric\all_sequences\distortion\level_name\00000.png
def copy_frames(src_root, dst_root, dryrun=False):
    """
    src_root structure (example):
        src_root/
            zeroday/
                motion_noise/
                    level0/
                        00000.png
                        00001.png
                dlss_rr/
                    level0/
                        ...

    dst_root structure (target):
        dst_root/
            zeroday/
                motion_noise/
                    level0/
                        00000.png
                        00001.png
                dlss_rr/
                    level0/
                        ...
    """

    # Loop over scenes (e.g. zeroday, bistro, ...)
    for scene_name in os.listdir(src_root):
        scene_path = os.path.join(src_root, scene_name)
        if not os.path.isdir(scene_path):
            continue

        # Loop over distortion-type folders inside each scene
        for distortion_name in os.listdir(scene_path):
            distortion_path = os.path.join(scene_path, distortion_name)
            if not os.path.isdir(distortion_path):
                continue

            # Loop over level folders inside each distortion
            for level_name in os.listdir(distortion_path):
                level_src = os.path.join(distortion_path, level_name)
                if not os.path.isdir(level_src):
                    continue

                # ✅ Destination now keeps scene name:
                # dst_root / scene_name / distortion_name / level_name
                level_dst = os.path.join(dst_root, scene_name, distortion_name, level_name)

                if dryrun:
                    print(f"[DRYRUN] Would create dir: {level_dst}")
                else:
                    os.makedirs(level_dst, exist_ok=True)

                # Copy all PNG frames
                for fname in os.listdir(level_src):
                    if not fname.lower().endswith(".png"):
                        continue

                    src_file = os.path.join(level_src, fname)
                    dst_file = os.path.join(level_dst, fname)

                    if dryrun:
                        print(f"[DRYRUN] Would copy: {src_file} -> {dst_file}")
                    else:
                        if os.path.exists(dst_file):
                            print(f"[WARN] Destination exists, skipping: {dst_file}")
                            continue
                        print(f"Copying: {src_file} -> {dst_file}")
                        shutil.copy2(src_file, dst_file)


# python copy_frames_all_sequences.py --dryrun
# python copy_frames_all_sequences.py
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy frames from all_sequences_pilot to all_sequences."
    )
    parser.add_argument(
        "--src",
        default=r"D:\motion-metric\all_sequences_pilot",
        help="Source root folder (default: D:\\motion-metric\\all_sequences_pilot).",
    )
    parser.add_argument(
        "--dst",
        default=r"D:\motion-metric\all_sequences",
        help="Destination root folder (default: D:\\motion-metric\\all_sequences).",
    )
    parser.add_argument(
        "--dryrun",
        action="store_true",
        help="Print what would be done, but do not copy files.",
    )

    args = parser.parse_args()
    copy_frames(args.src, args.dst, dryrun=args.dryrun)
