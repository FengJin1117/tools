import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="删除没有乐谱的音频文件")
    parser.add_argument("--wav_path", type=str, required=True, help="音频文件目录")
    parser.add_argument("--score_path", type=str, required=True, help="乐谱文件路径（txt）")
    return parser.parse_args()

def load_valid_ids(score_path):
    """从score文件中读取所有存在的ID"""
    valid_ids = set()
    with open(score_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "|" not in line:
                continue
            audio_id = line.split("|")[0].strip()
            valid_ids.add(audio_id)
    return valid_ids

def delete_no_score_wavs(wav_path, valid_ids):
    """删除不在score文件中的wav音频"""
    deleted = 0
    total = 0
    for file in os.listdir(wav_path):
        if not file.lower().endswith(".wav"):
            continue
        total += 1
        audio_id = os.path.splitext(file)[0]  # 去掉.wav后缀
        if audio_id not in valid_ids:
            os.remove(os.path.join(wav_path, file))
            print(f"🗑️ 已删除无乐谱音频：{file}")
            deleted += 1
    print(f"\n✅ 共扫描 {total} 个音频文件，删除 {deleted} 个无乐谱文件。")

def main():
    args = parse_args()
    if not os.path.exists(args.wav_path):
        raise FileNotFoundError(f"音频目录不存在: {args.wav_path}")
    if not os.path.exists(args.score_path):
        raise FileNotFoundError(f"乐谱文件不存在: {args.score_path}")

    valid_ids = load_valid_ids(args.score_path)
    print(f"🎵 从 {args.score_path} 中读取到 {len(valid_ids)} 个有效ID。")
    delete_no_score_wavs(args.wav_path, valid_ids)

if __name__ == "__main__":
    main()
