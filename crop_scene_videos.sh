$src = "D:\motion-metric\all_sequences_videos#zeroday"
$dst = "D:\motion-metric\all_sequences_videos\zeroday_cropped"

Get-ChildItem -Path $src -Filter "video_0.mkv" -Recurse | ForEach-Object {
    $relPath = Resolve-Path $_.FullName -Relative
    $relUnderSrc = $relPath.Substring($src.Length).TrimStart('\','/')
    $outDir = Join-Path $dst (Split-Path $relUnderSrc -Parent)
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null

    $inFile  = $_.FullName
    $outFile = Join-Path $outDir "video_0.mkv"

    ffmpeg -y -ss 0 -to 3 -i "$inFile" -c copy "$outFile"
}
