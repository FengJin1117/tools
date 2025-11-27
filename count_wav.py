import os
import argparse
import soundfile as sf
from tqdm import tqdm

def count_wavs_info(folder, recursive=False):
    total_duration = 0.0
    total_files = 0

    if recursive:
        walker = os.walk(folder)
    else:
        # 只遍历当前文件夹
        walker = [(folder, [], os.listdir(folder))]

    for root, _, files in walker:
        for f in files:
            if f.lower().endswith(".wav"):
                filepath = os.path.join(root, f)
                try:
                    with sf.SoundFile(filepath) as audio:
                        duration = len(audio) / audio.samplerate
                        total_duration += duration
                        total_files += 1
                except Exception as e:
                    print(f"读取 {filepath} 出错: {e}")

    return total_files, total_duration


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="统计文件夹下wav文件的数量和总时长")
    parser.add_argument("folder", type=str, help="输入文件夹路径")
    parser.add_argument("-r", "--recursive", action="store_true", default=False, help="是否递归搜索子文件夹（默认: 否）")
    args = parser.parse_args()

    total_files, total_duration = count_wavs_info(args.folder, args.recursive)
    print(f"总wav文件数: {total_files}")
    print(f"总时长: {total_duration/60:.2f} 分钟 ({total_duration/3600:.2f} 小时)")
