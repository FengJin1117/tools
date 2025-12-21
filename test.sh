#!/usr/bin/env bash
set -euo pipefail

# 源路径（包含星号结构）
SRC_BASE="/data7/fwh/benchdata"
SRC_SUB="suno_score"        # suno_score 目录名
PATTERN="${SRC_BASE}/${SRC_SUB}/*/test.txt"

# 目标根目录（会保留 genre 层级）
DEST_BASE="${SRC_BASE}/suno_score_only"

# 如果需要覆盖已有文件，可将 CP_OPTS=""（默认 -n: 不覆盖）
CP_OPTS="-p -n"   # -p 保留属性，-n 不覆盖已有文件

# 确保目标根目录存在
mkdir -p "${DEST_BASE}"

# 使用 find 遍历匹配文件，安全处理空格与特殊字符
find "${SRC_BASE}/${SRC_SUB}" -type f -name "test.txt" -mindepth 2 -maxdepth 2 -print0 |
while IFS= read -r -d '' file; do
    # file 示例: /data7/fwh/benchdata/suno_score/<genre>/test.txt

    # 取出 genre/... 相对路径（去掉前缀 ".../suno_score/"）
    rel="${file#${SRC_BASE}/${SRC_SUB}/}"    # 例如 "<genre>/test.txt"

    # 目标路径： DEST_BASE/<genre>/test.txt
    target="${DEST_BASE}/${rel}"

    # 创建目标目录（如果不存在）
    mkdir -p "$(dirname "$target")"

    # 复制文件（-p 保留属性；-n 不覆盖已有文件）
    cp ${CP_OPTS} -- "$file" "$target" && \
        echo "copied: $file -> $target" || \
        echo "skipped (exists or error): $file"
done
