import os
import soundfile as sf

def delete_short_wavs(root_dir, min_duration=0.3):
    """
    递归删除时长小于 min_duration 秒的 wav 文件
    """
    removed = 0

    for root, _, files in os.walk(root_dir):
        for fname in files:
            if fname.lower().endswith(".wav"):
                wav_path = os.path.join(root, fname)
                try:
                    info = sf.info(wav_path)
                    duration = info.frames / info.samplerate
                    if duration < min_duration:
                        os.remove(wav_path)
                        removed += 1
                except Exception as e:
                    print(f"[ERROR] {wav_path}: {e}")

    print(f"Done. Removed {removed} wav files.")


if __name__ == "__main__":
    # root_dir = "/data7/fwh/benchmark/suno_svs_infer/suno_techsinger"
    # delete_short_wavs(root_dir)

    # root_dirs = [
    #     "/data7/fwh/espnet/egs2/opencpop_benchmark/svs1/checkpoints/opencpop_naive_rnn_dp/exp/svs_train_naive_rnn_dp_raw_phn_None_zh",
    #     "/data7/fwh/espnet/egs2/opencpop_benchmark/svs1/checkpoints/opencpop_xiaoice/exp/svs_train_xiaoice_raw_phn_None_zh",
    #     "/data7/fwh/espnet/egs2/opencpop_benchmark/svs1/checkpoints/opencpop_visinger/exp/svs_visinger_normal",
    #     "/data7/fwh/espnet/egs2/opencpop_benchmark/svs1/checkpoints/opencpop_visinger2/exp/svs_visinger2_normal",
    # ]
    root_dirs = [
        # "/data7/fwh/benchmark/fix_svs_infer/suno_rnn",
        "/data7/fwh/benchmark/fix_svs_infer/suno_visinger",
        "/data7/fwh/benchmark/fix_svs_infer/suno_visinger2",
        "/data7/fwh/benchmark/fix_svs_infer/suno_xiaoicesing",
        "/data7/fwh/benchmark/fix_svs_infer/suno_stylesinger",
    ]
    for root_dir in root_dirs:
        delete_short_wavs(root_dir)