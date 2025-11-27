#!/bin/bash

root_dir="/data7/fwh/benchdata/suno_score"

for genre in "$root_dir"/*; do
    # 必须是目录才处理
    if [ -d "$genre" ]; then
        wav_dir="$genre/wavs"
        score_file="$genre/test.txt"

        if [ -d "$wav_dir" ] && [ -f "$score_file" ]; then
            echo "=== 处理 Genre: $(basename "$genre") ==="
            python3 clean_no_score_audio.py \
                --wav_path "$wav_dir" \
                --score_path "$score_file"
        else
            echo "⚠️ 跳过 $(basename "$genre")（wavs 或 test.txt 缺失）"
        fi
    fi
done
