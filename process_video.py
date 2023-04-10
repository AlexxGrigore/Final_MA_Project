#!/usr/bin/env python
import subprocess
import re
import warnings
from fractions import Fraction
import os

import librosa
import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import glob
from scipy.io.wavfile import read
# from mfcc import *
import mfcc as compute_mfcc
from video_features import *
from database import *
import time

# import librosa
from sklearn.decomposition import PCA


def save_entry_to_database(id, video_name, mfccs, colorhist_diffs, connection):
    descr = {}
    aux_list = np.zeros((len(mfccs) - 1, len(mfccs[0]) - 1, len(mfccs[0][0])))
    for i in range(len(mfccs) - 1):
        for j in range(len(mfccs[0]) - 1):
            for k in range(len(mfccs[0][0])):
                aux_list[i][j][k] = mfccs[i][j][k]
    # for aux_mfcc in mfccs:
    #     aux_list

    descr['mfcc'] = aux_list
    # descr['audio'] = np.array(audio_powers)
    # descr['colhist'] = np.array(colorhists)
    # descr['tempdiff'] = np.array(sum_of_differences)
    descr['chdiff'] = np.array(colorhist_diffs)
    add_video_descriptor(id, video_name, descr, connection)
    print('added ' + video_name + ' to database')


# Processing of videos
def process_videos(video_list, connection):
    start_database_time = time.time()
    total = len(video_list)
    progress_count = 0
    for video in video_list:
        star_time = time.time()
        progress_count += 1
        print('processing: ', video, ' (', progress_count, ' of ', total, ')')
        cap = cv2.VideoCapture(video)

        if not cap.isOpened():
            raise Exception("No video file found at the path specified")

        frame_rate = cap.get(cv2.CAP_PROP_FPS)

        # get corresponding audio file
        filename, fileExtension = os.path.splitext(video)
        audio = filename + '.wav'
        fs, wav_data = read(audio)

        colorhists = []
        sum_of_differences = []
        audio_powers = []
        mfccs = []
        colorhist_diffs = []

        prev_colorhist = None
        prev_frame = None
        frame_nbr = 0
        timestamp = 2 * 75

        while (cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break

            audio_frame = frame_to_audio(frame_nbr, frame_rate, fs, wav_data).astype(float)

            # check if audio frame is long enough for mfcc transformation
            if len(audio_frame) >= int(0.01 * fs):
                # power = np.mean(audio_frame ** 2)
                # audio_powers.append(power)
                # ceps = librosa.feature.mfcc(y=audio_frame, sr=16000, n_mfcc=13, n_fft=512, win_length=256)

                # ----------------------------------------------------
                # APPLY PCA TO REDUCE CEPS SIZE

                # Compute MFCCs
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", message="n_fft=512 is too large for input signal of length=2")
                    ceps = librosa.feature.mfcc(y=audio_frame, sr=16000, n_mfcc=13, n_fft=512, hop_length=256)

                ceps = np.squeeze(ceps)

                # Apply PCA to reduce dimensionality
                pca = PCA(n_components=min(12, len(ceps[0])))
                ceps_pca = pca.fit_transform(ceps.T).T

                # Reshape MFCCs to 13x13 matrix
                ceps_final = np.zeros((13, 13))
                ceps_final[:ceps_pca.shape[0], :ceps_pca.shape[1]] = ceps_pca

                ceps = ceps_final
                # ----------------------------------------------------

                # ceps, _, _ = compute_mfcc.mfcc(audio_frame)
                # ceps = np.nan_to_num(ceps)

                # ceps = librosa.feature.mfcc(y=audio_frame, sr=fs, n_mfcc=20)
                # ----------------------------------------------------
                # ceps = np.squeeze(ceps)
                # pca = PCA(n_components=13)
                # ceps = pca.fit_transform(ceps.T).T[:, :13]
                # ----------------------------------------------------

                mfccs.append(ceps)

            # calculate sum of differences
            # if not prev_frame is None:
            #     tdiv = temporal_diff(prev_frame, frame, 10)
            #     # diff = np.absolute(prev_frame - frame)
            #     # sum = np.sum(diff.flatten()) / (diff.shape[0]*diff.shape[1]*diff.shape[2])
            #     sum_of_differences.append(tdiv)
            color_hist = colorhist(frame)
            # colorhists.append(color_hist)
            if not prev_colorhist is None:
                ch_diff = colorhist_diff(prev_colorhist, color_hist)
                colorhist_diffs.append(ch_diff)
            prev_colorhist = color_hist
            prev_frame = frame
            frame_nbr += 1

            current_timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            if current_timestamp >= timestamp:
                descr = {}
                aux_list = np.zeros((len(mfccs) - 1, len(mfccs[0]) - 1, len(mfccs[0][0])))
                for i in range(len(mfccs) - 1):
                    for j in range(len(mfccs[0]) - 1):
                        for k in range(len(mfccs[0][0])):
                            aux_list[i][j][k] = mfccs[i][j][k]
                # for aux_mfcc in mfccs:
                #     aux_list

                descr['mfcc'] = aux_list
                # descr['audio'] = np.array(audio_powers)
                # descr['colhist'] = np.array(colorhists)
                # descr['tempdiff'] = np.array(sum_of_differences)
                descr['chdiff'] = np.array(colorhist_diffs)
                video_name = video
                video_name.replace('dataset/', '')
                add_video_descriptor(progress_count, video_name, descr, connection)
                print('added ' + video + ' to database')
                progress_count += 1
                colorhist_diffs = []
                mfccs = []
                timestamp *= 2

        print('end:', frame_nbr)

        # prepare descriptor for database
        # mfccs = descr['mfcc'] # Nx13 np array (or however many mfcc coefficients there are)
        # audio = descr['audio'] # Nx1 np array
        # colhist = descr['colhist'] # Nx3x256 np array
        # tempdif = descr['tempdiff'] # Nx1 np array
        descr = {}
        aux_list = np.zeros((len(mfccs) - 1, len(mfccs[0]) - 1, len(mfccs[0][0])))
        for i in range(len(mfccs) - 1):
            for j in range(len(mfccs[0]) - 1):
                for k in range(len(mfccs[0][0])):
                    aux_list[i][j][k] = mfccs[i][j][k]
        # for aux_mfcc in mfccs:
        #     aux_list

        descr['mfcc'] = aux_list
        # descr['audio'] = np.array(audio_powers)
        # descr['colhist'] = np.array(colorhists)
        # descr['tempdiff'] = np.array(sum_of_differences)
        descr['chdiff'] = np.array(colorhist_diffs)
        video_name = video
        video_name.replace('dataset/', '')
        add_video_descriptor(progress_count, video_name, descr, connection)
        print('added ' + video + ' to database')

        end_time = time.time()
        print('it took {} seconds to process the video'.format(int(end_time - star_time)))

    end_database_time = time.time()
    print(' it took {} seconds to create the database'.format(int(end_database_time - start_database_time)))
    connection.commit()
