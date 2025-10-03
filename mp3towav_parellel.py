import os
import glob
import subprocess
import argparse
import shutil
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def convert_one(mp3_path, output_dir):
    fname = os.path.splitext(os.path.basename(mp3_path))[0]
    wav_path = os.path.join(output_dir, fname + ".wav")

    if os.path.exists(wav_path):
        return f"⚠️ 已存在，跳过: {fname}.wav"

    cmd = [
        "ffmpeg", "-y",
        "-i", mp3_path,
        "-ac", "1",
        "-ar", "44100",
        "-sample_fmt", "s16",
        wav_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return f"✅ 完成: {fname}.wav"

def convert_mp3_to_wav(input_dir, output_dir=None, num_workers=8):
    if output_dir is None:
        output_dir = input_dir
    os.makedirs(output_dir, exist_ok=True)

    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg 没找到，请先安装：apt/yum/conda/brew 都可以。")

    mp3_files = glob.glob(os.path.join(input_dir, "*.mp3"))
    if not mp3_files:
        print("⚠️ 没有找到 mp3 文件。")
        return

    print(f"🔁 开始转换 {len(mp3_files)} 个文件（多线程并行，已存在 wav 文件将跳过）...")

    results = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(convert_one, mp3, output_dir): mp3 for mp3 in mp3_files}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Converting", unit="file"):
            results.append(future.result())

    # tqdm 内部 print 不会乱，用 tqdm.write 保证行整齐
    for r in results:
        tqdm.write(r)

    print("✅ 全部转换完成。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", type=str, required=True, help="mp3 所在目录")
    parser.add_argument("--output_dir", type=str, default=None, help="输出 wav 目录（默认与输入相同）")
    parser.add_argument("-j", "--jobs", type=int, default=8, help="并行线程数（默认 8）")
    args = parser.parse_args()

    convert_mp3_to_wav(args.input_dir, args.output_dir, args.jobs)
