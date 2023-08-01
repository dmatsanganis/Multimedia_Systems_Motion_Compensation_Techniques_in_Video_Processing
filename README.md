# Multimedia Systems: Motion Compensation Techniques in Video Processing

## Introduction

This project implements motion compensation techniques for video processing. The goal is to study how these techniques influence prediction errors.

## Overview

The project is divided into two main parts:

1. **Full Frame Prediction:** In the first part, we assume that we want to predict whole P-frames, not in segments. The prediction of each entire frame is based on the previous frame. We implement a procedure that takes two frames as input, calculates their difference, and returns an error frame. We do not calculate a motion vector. The error frames are displayed, and the information content of the error frame should be less compared to the frames.

2. **Motion Prediction Technique:** In the second part, we implement a motion prediction technique, which calculates motion vectors per block. Each block has the typical MPEG size of 16 × 16. We implement a function that takes two frames as input: a reference frame, which is used to search for motion vectors, and a target frame, which will be predicted. The target frame is divided into macroblocks of size 16 × 16. If the width and height of the frame are not multiples of 16, the frame is appropriately filled with black pixels. For each block in the target frame, we refer to the corresponding position in the reference frame and find the area that gives the best match.

All calculations are performed using **Python**.

## Contributors

- [x] [Dimitris Matsanganis](https://github.com/dmatsanganis)
- [x] [Alex Skarpelos](https://github.com/alexhsog)


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
