import os
import argparse
import soundfile as sf
from tqdm import tqdm

def count_wavs_info(folder):
    total_duration = 0.0
    total_files = 0

    for root, _, files in os.walk(folder):
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
    args = parser.parse_args()

    total_files, total_duration = count_wavs_info(args.folder)
    print(f"总wav文件数: {total_files}")
    print(f"总时长: {total_duration/60:.2f} 分钟 ({total_duration/3600:.2f} 小时)")
