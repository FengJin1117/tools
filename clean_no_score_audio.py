import os
import argparse


def load_valid_ids(score_path):
    """从 score 文件中读取所有存在的音频 ID"""
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
    """删除不在 score 文件中的 wav 音频"""
    deleted = 0
    total = 0

    for file in os.listdir(wav_path):
        if not file.lower().endswith(".wav"):
            continue
        total += 1
        audio_id = os.path.splitext(file)[0]
        if audio_id not in valid_ids:
            os.remove(os.path.join(wav_path, file))
            deleted += 1

    return total, deleted


def clean_wavs_by_score(wav_path: str, score_path: str):
    """
    对外暴露的总函数：
    仅输入 wav 目录 和 score 路径，执行清理动作
    """
    if not os.path.exists(wav_path):
        raise FileNotFoundError(f"音频目录不存在: {wav_path}")
    if not os.path.exists(score_path):
        raise FileNotFoundError(f"乐谱文件不存在: {score_path}")

    valid_ids = load_valid_ids(score_path)
    total, deleted = delete_no_score_wavs(wav_path, valid_ids)

    print(f"🎵 从 {score_path} 中读取到 {len(valid_ids)} 个有效 ID")
    print(f"✅ 共扫描 {total} 个音频文件，删除 {deleted} 个无乐谱文件")

    return {
        "total_wavs": total,
        "deleted_wavs": deleted,
        "valid_ids": len(valid_ids),
    }


# ================= CLI 入口（可选） =================

def parse_args():
    parser = argparse.ArgumentParser(description="删除没有乐谱的音频文件")
    parser.add_argument("--wav_path", type=str, required=True)
    parser.add_argument("--score_path", type=str, required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    clean_wavs_by_score(args.wav_path, args.score_path)


if __name__ == "__main__":
    main()
