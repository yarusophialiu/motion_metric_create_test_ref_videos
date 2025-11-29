import os
import shutil


dist_type = 'dlss_rr' # have 3 level subfolders
root = r"D:\motion-metric"
dst_root = r"D:\motion-metric\all_sequences"
DRYRUN = False # True

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def move_dir_files(src_dir, dst_dir):
    ensure_dir(dst_dir)
    for name in os.listdir(src_dir):
        src_file = os.path.join(src_dir, name)
        if os.path.isfile(src_file):
            dst_file = os.path.join(dst_dir, name)
            if DRYRUN:
                print(f'Move {src_file} -> {dst_file}')
            else:
                shutil.move(src_file, dst_file)

# --- 1) motion_noise: <scene>\levelX\ -> <scene>\motion_noise\levelX\
def handle_motion_noise():
    src_root = os.path.join(root, dist_type)
    if not os.path.isdir(src_root):
        return
    for scene in os.listdir(src_root):
        scene_path = os.path.join(src_root, scene)
        if not os.path.isdir(scene_path):
            continue
        for level in os.listdir(scene_path):
            level_path = os.path.join(scene_path, level)
            if not os.path.isdir(level_path):
                continue
            dst_dir = os.path.join(dst_root, scene, dist_type, level)
            move_dir_files(level_path, dst_dir)
            print(f"[{dist_type}] {scene}\\{level} -> {dst_dir}")

# --- 2) dlss_rr: <scene>\<Quality>\<Multiplier>\ -> <scene>\dlss_rr\<quality>_<multiplier>\
# e.g., Balanced\4_multiplier -> balanced_4_multiplier
def normalize_quality(q):
    return q.strip().lower().replace(" ", "_")

def normalize_multiplier(m):
    # keep as-is but normalize spaces/case to be safe
    return m.strip().lower().replace(" ", "_")

def handle_dlss_rr():
    src_root = os.path.join(root, "dlss_rr")
    if not os.path.isdir(src_root):
        return
    for scene in os.listdir(src_root):
        print(f'\nscene {scene}')
        scene_path = os.path.join(src_root, scene)
        if not os.path.isdir(scene_path):
            continue

        # Expect subfolders like Balanced, Quality, Performance, etc.
        for qual in os.listdir(scene_path):
            qual_path = os.path.join(scene_path, qual)
            if not os.path.isdir(qual_path):
                continue

            # Inside quality, expect multiplier folders like 4_multiplier
            for mult in os.listdir(qual_path):
                mult_path = os.path.join(qual_path, mult)
                if not os.path.isdir(mult_path):
                    continue

                level_name = f"{normalize_quality(qual)}_{normalize_multiplier(mult)}"
                dst_dir = os.path.join(dst_root, scene, "dlss_rr", level_name)
                move_dir_files(mult_path, dst_dir)
                print(f"[dlss_rr] {scene}\\{qual}\\{mult} -> {dst_dir}")
        # break

if __name__ == "__main__":
    handle_motion_noise()
    handle_dlss_rr()
    print("✅ Done.")
