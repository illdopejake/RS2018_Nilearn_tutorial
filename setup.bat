@echo off
title Setting up nilearn tutorial
conda create -n nilearn_tutorial python=3.6
activate nilearn_tutorial
pip install -U --user nilearn
conda install numpy matplotlib scikit-learn jupyter pandas h5py
pip install -U --user scipy
python download.py