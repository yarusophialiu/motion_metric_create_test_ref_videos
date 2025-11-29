import os
import subprocess
import json

root_dir = r"D:\motion-metric\pilot_videos\zeroday"

def get_duration(path):
    try:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of", "json", path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = json.loads(result.stdout)["format"]["duration"]
        return float(duration)
    except:
        return None

for root, _, files in os.walk(root_dir):
    for f in files:
        if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
            path = os.path.join(root, f)
            dur = get_duration(path)
            if dur is not None and dur < 2:
                print(f"{dur:.2f}s  |  {path}")
