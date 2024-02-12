#!/bin/bash
unamem="$(uname -m)"
output_dir="./anaconda"

script="Miniconda3-latest-Linux-${unamem}.sh"
if [ ! -e $script ]; then
    wget --tries=3 "https://repo.anaconda.com/miniconda/${script}"
fi

if [ ! -d $output_dir ]; then
    bash "${script}" -b -p "${output_dir}"
fi
activate_conda="source ${output_dir}/etc/profile.d/conda.sh"
eval $activate_conda

if [ -e $script ]; then
    rm $script
fi