##############################
# lossless 2 seconds
##############################
encode yuv 420, crf 5








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
