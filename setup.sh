#!/bin/bash

conda create -n nilearn_tutorial python=3.6
source activate nilearn_tutorial
pip install -U --user nilearn
conda install matplotlib scikit-learn jupyter pandas
pip install -U --user scipy
