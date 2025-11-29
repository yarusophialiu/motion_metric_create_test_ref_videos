Python code to prepare videos for experiment
Experiment code is in matlab, 
Resides in D:\motion-metric\motion-metric-experiment

##############################
# make pilot video
##############################
rename_files.py # rename frames to 00000.png, frames from some scenes are not well named
create_videos_by_scene.py # scene start from different frame
run_all_jobs.py



flashing point
    zeroday: 3 points (video_0 to video_3) 3 seconds
        614， 299 frame 0
        626， 533 frame 50
        670， 99 frame 280
    bistro_interior：
        465， 351 frame 0 - 616
        980， 492 frame 400 - 960
        427， 553 frame 616 - 1199
    subway:
        530， 229 frame 0-500
        736， 455 entire sequence
        990， 70 frame 0-875





motion-metric/
├─ data/
│  ├─ frames/
│  │  ├─ reference/
│  │  │  ├─ scene01/
│  │  │  │  └─ %06d.png      # reference frames
│  │  │  ├─ scene02/
│  │  │  │  └─ %06d.png
│  │  ├─ test-trim/
│  │  │  ├─ scene01/
│  │  │  │  └─ %06d.png      # trimmed or modified frames
│  │  │  ├─ scene02/
│  │  │  │  └─ %06d.png
│  │  └─ ... (future test variants)
│  │
│  ├─ videos/
│  │  ├─ reference/
│  │  │  ├─ scene01.mp4
│  │  │  ├─ scene02.mp4
│  │  ├─ test-trim/
│  │  │  ├─ scene01.mp4
│  │  │  ├─ scene02.mp4
│  │  └─ ...
│  │
│  └─ meta.yaml             # global fps / resolution info (optional)
│
├─ create_test_ref_videos/
│  └─ build_videos.py
└─ README.md
