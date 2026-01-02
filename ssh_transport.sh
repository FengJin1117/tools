#!/bin/bash

# local_path: 在本地你要传的文件（夹）

target_server="taurus"
local_path="/data7/fwh/benchdata/suno_score_fix/rock/wavs"
target_local_path="/fwh/data/suno_score_only_fix/rock"

# target_server="mars"
# local_path="/data7/fwh/benchdata/suno_score_only_fix"
# target_local_path="fwh/data"

# target_server="venus"
# local_path="/data7/fwh/benchdata/suno_score_only_fix"
# target_local_path="fwh/data"

# 通用参数
ssh_dir="../ssh"

# Declare associative arrays
declare -A HOSTS
declare -A PORTS
declare -A SSH_KEYS
declare -A REMOTE_PATHS

# Taurus server
HOSTS["taurus"]="202.112.113.77"
PORTS["taurus"]=2223
SSH_KEYS["taurus"]="taurus_fwh_2223"
# REMOTE_PATHS["taurus"]="/data3/fwh"
REMOTE_PATHS["taurus"]="/data6/arllan"

# Venus server
HOSTS["venus"]="202.112.113.30"
PORTS["venus"]=2236
SSH_KEYS["venus"]="venus_tyx_2236"
REMOTE_PATHS["venus"]="/data3/tyx"

# Capri
HOSTS["capri"]="202.112.113.74"
PORTS["capri"]=2227
SSH_KEYS["capri"]="capri_tyx_2227"
REMOTE_PATHS["capri"]="/data7/fwh"

ssh -i "${ssh_dir}/${SSH_KEYS[$target_server]}" \
    -p "${PORTS[$target_server]}" \
    root@"${HOSTS[$target_server]}" \
    "mkdir -p ${REMOTE_PATHS[$target_server]}${target_local_path}"


echo "tagert path: ${REMOTE_PATHS[$target_server]}${target_local_path}"
# Build and run SCP command
scp -r \
    -i "${ssh_dir}/${SSH_KEYS[$target_server]}" \
    -P "${PORTS[$target_server]}" \
    ${local_path} \
    root@"${HOSTS[$target_server]}":"${REMOTE_PATHS[$target_server]}${target_local_path}"

# # 使用 rsync 并排除 wavs/
# rsync -avz \
#     -e "ssh -i ${ssh_dir}/${SSH_KEYS[$target_server]} -p ${PORTS[$target_server]}" \
#     --exclude "wavs/" \
#     "${local_path}/" \
#     root@"${HOSTS[$target_server]}":"${REMOTE_PATHS[$target_server]}"
