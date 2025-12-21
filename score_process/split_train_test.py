import os
import random

def split_train_test(txt_path, test_size=50, shuffle=False, seed=42):
    """
    将 txt 文件拆分为 train.txt 和 test.txt（互斥）

    Args:
        txt_path (str): 原始 txt 路径
        test_size (int): 测试集条数，默认 50
        shuffle (bool): 是否打乱顺序，默认 False
        seed (int): 随机种子（仅在 shuffle=True 时生效）
    """
    assert os.path.isfile(txt_path), f"文件不存在: {txt_path}"

    with open(txt_path, "r", encoding="utf-8") as f:
        lines = [line for line in f if line.strip()]

    total = len(lines)
    assert test_size < total, f"test_size({test_size}) >= 总行数({total})"

    if shuffle:
        random.seed(seed)
        random.shuffle(lines)

    test_lines = lines[:test_size]
    train_lines = lines[test_size:]

    base_dir = os.path.dirname(txt_path)
    train_path = os.path.join(base_dir, "train.txt")
    test_path = os.path.join(base_dir, "test.txt")

    with open(train_path, "w", encoding="utf-8") as f:
        f.writelines(train_lines)

    with open(test_path, "w", encoding="utf-8") as f:
        f.writelines(test_lines)

    print(f"[OK] 总数: {total}")
    print(f"[OK] train: {len(train_lines)} -> {train_path}")
    print(f"[OK] test : {len(test_lines)} -> {test_path}")

if __name__ == "__main__":
    split_train_test(
        "/data7/fwh/data/rock_train/opencpop.txt",
        test_size=50
    )

