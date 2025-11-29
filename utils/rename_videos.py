import os

root_dir = r"D:\motion-metric\experiment_videos_crf5"

for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "video0.mp4":
            old_path = os.path.join(dirpath, filename)
            new_path = os.path.join(dirpath, "video_0.mp4")
            os.rename(old_path, new_path)
            print(f"Renamed: {old_path} -> {new_path}")
