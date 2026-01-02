import os
import argparse
import soundfile as sf


def count_wavs_info(folder, recursive=False):
    """
    统计文件夹下所有 wav 文件的数量和总时长
    """
    total_duration = 0.0
    file_count = 0

    if recursive:
        walker = os.walk(folder)
    else:
        walker = [(folder, [], os.listdir(folder))]

    for root, _, files in walker:
        for f in files:
            if f.lower().endswith(".wav"):
                filepath = os.path.join(root, f)
                try:
                    with sf.SoundFile(filepath) as audio:
                        duration = len(audio) / audio.samplerate
                        total_duration += duration
                        file_count += 1
                except Exception as e:
                    print(f"⚠️ 读取 {filepath} 出错: {e}")

    return file_count, total_duration


def summarize_wav_folder(wav_folder: str, recursive: bool = False):
    """
    【对外调用接口】
    输入音频文件夹，统计并打印结果
    """
    if not os.path.exists(wav_folder):
        raise FileNotFoundError(f"音频目录不存在: {wav_folder}")

    file_count, total_duration = count_wavs_info(wav_folder, recursive)

    print(f"📁 音频目录: {wav_folder}")
    print(f"🎵 wav 文件数: {file_count}")
    print(f"⏱️ 总时长: {total_duration:.2f} 秒 "
          f"({total_duration / 60:.2f} 分钟, {total_duration / 3600:.2f} 小时)")

    return {
        "file_count": file_count,
        "total_duration_sec": total_duration,
        "total_duration_min": total_duration / 60,
        "total_duration_hour": total_duration / 3600,
    }


# ================= CLI 入口（可选） =================

def main():
    parser = argparse.ArgumentParser(description="统计文件夹下 wav 文件的数量和总时长")
    parser.add_argument("folder", type=str, help="输入文件夹路径")
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        default=False,
        help="是否递归搜索子文件夹（默认: 否）"
    )
    args = parser.parse_args()

    summarize_wav_folder(args.folder, args.recursive)


if __name__ == "__main__":
    main()
