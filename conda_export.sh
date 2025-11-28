# 指定环境名称
conda_env_name=""

conda env export -n ${conda_env_name} > ${conda_env_name}.yml
