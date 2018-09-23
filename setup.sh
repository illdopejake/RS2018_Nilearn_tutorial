#!/bin/bash

conda create -n nilearn_tutorial python=3.6
source activate nilearn_tutorial
pip install -U --user nilearn
conda install scipy matplotlib scikit-learn jupyter
pip install -U --user scipy
