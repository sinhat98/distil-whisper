#!/bin/bash
module load cuda/11.8.0
if conda env list | grep -q 'distil-whisper'; then
    conda env remove -n distil-whisper
fi
conda create -y -n distil-whisper python=3.10
conda activate distil-whisper
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
