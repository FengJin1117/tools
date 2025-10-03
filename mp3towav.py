import os
import glob
import subprocess
import argparse
import shutil
from tqdm import tqdm  # 进度条

def convert_mp3_to_wav(input_dir, output_dir=None):
    if output_dir is None:
        output_dir = input_dir
    os.makedirs(output_dir, exist_ok=True)

    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg 没找到，请先安装：apt/yum/conda/brew 都可以。")

    mp3_files = glob.glob(os.path.join(input_dir, "*.mp3"))
    if not mp3_files:
        print("⚠️ 没有找到 mp3 文件。")
        return

    print(f"🔁 开始转换 {len(mp3_files)} 个文件（已存在 wav 文件将跳过）...")
    for mp3_path in tqdm(mp3_files, desc="Converting", unit="file"):
        fname = os.path.splitext(os.path.basename(mp3_path))[0]
        wav_path = os.path.join(output_dir, fname + ".wav")

        # 如果目标 wav 已存在，跳过
        if os.path.exists(wav_path):
            # tqdm 会自动刷新，不需要 print，每个文件都显示跳过状态可用下面方式：
            # tqdm.write(f"⚠️ 已存在，跳过: {wav_path}")
            continue

        cmd = [
            "ffmpeg", "-y",
            "-i", mp3_path,
            "-ac", "1",              # 单声道
            "-ar", "44100",          # 采样率 44.1kHz
            "-sample_fmt", "s16",    # 16-bit PCM
            wav_path
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print("✅ 全部转换完成。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", type=str, required=True, help="mp3 所在目录")
    parser.add_argument("--output_dir", type=str, default=None, help="输出 wav 目录（默认与输入相同）")
    args = parser.parse_args()

    convert_mp3_to_wav(args.input_dir, args.output_dir)
