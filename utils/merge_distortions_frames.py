import os
import shutil

# merge frames to all_sequences
# 2 level subfolders
root = r"D:\motion-metric"
dist_type = "stutter"
src_root = f"{root}/{dist_type}"
dst_root = f"{root}/all_sequences"
DRYRUN = True # False

print(f'Distortion {dist_type}')
for scene_name in os.listdir(src_root):
    print(f'\nscene_name {scene_name}')
    scene_path = os.path.join(src_root, scene_name)
    if not os.path.isdir(scene_path):
        continue

    # Example: D:\motion-metric\motion_noise\bistro\level0
    for level_name in os.listdir(scene_path):
        print(f'level_name {level_name}')
        level_path = os.path.join(scene_path, level_name)
        if not os.path.isdir(level_path):
            continue

        # Destination: D:\motion-metric\all_sequences\bistro\motion_noise\level0
        dst_dir = os.path.join(dst_root, scene_name, dist_type, level_name)
        os.makedirs(dst_dir, exist_ok=True)

        for file_name in os.listdir(level_path):
            src_file = os.path.join(level_path, file_name)
            dst_file = os.path.join(dst_dir, file_name)
            if os.path.isfile(src_file):
                if DRYRUN:
                    print(f'Move from {src_file} -> {dst_file}')
                else:
                    shutil.move(src_file, dst_file)
    # break

print("✅ All images moved successfully.")
