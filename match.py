import sqlite3
import sys

import numpy as np
from video_features import *
from database import adapt_array, convert_array


def find_match(descriptor, database_path):
    # Connect to the database
    connection = None
    try:
        sqlite3.register_adapter(np.ndarray, adapt_array)
        sqlite3.register_converter("array", convert_array)
        connection = sqlite3.connect(database_path, detect_types=sqlite3.PARSE_DECLTYPES, isolation_level=None)
    except ConnectionRefusedError as e:
        print(e)

    # Create cursor object
    cursor = connection.cursor()

    # Execute query to retrieve all database entries
    cursor.execute('SELECT * FROM Video')

    # Fetch all videos in the database
    videos = cursor.fetchall()

    best_score = -2
    fr = None
    matched_video = None

    # Iterate over all videos
    for id, name, mfcc, chdiff in videos:
        if len(descriptor['mfcc']) > len(mfcc) or len(descriptor['chdiff']) > len(chdiff):
            continue

        # Pad mfcc arrays
        arr1, arr2 = pad_arrays(mfcc, descriptor['mfcc'])

        # Compute score based on MFCCs
        frame_mfcc, score_mfcc = sliding_window(arr1, arr2, cosine_similarity)

        # Pad color histogram diff arrays

        # Compute score based on MFCCs
        frame_cd, score_cd = sliding_window(chdiff, descriptor['chdiff'], cosine_similarity)

        frame = frame_mfcc

        if score_cd > score_mfcc:
            frame = frame_cd

        score = 0.8 * score_mfcc + 0.2 * score_cd

        if score > best_score:
            best_score = score
            matched_video = name
            fr = frame

    return matched_video, best_score, fr


def sliding_window(signal, window, compare_func):
    """
    Slides window over signal to find best match

    :param signal: the original signal
    :param window: the window
    :param compare_func: computes some similarity measure between window and a chunk of the original signal

    :return: the start frame and score of the best match found
    """

    window_length = len(window)
    minimum = -10
    shift = 10
    i = 0
    frame = -1

    while i < len(signal) - window_length:
        # Compute the difference between window and signal chunk
        diff = compare_func(window, signal[i: i + window_length])
        # diff = abs(diff)

        if diff > minimum:
            minimum = diff
            frame = i
        i += shift

    return frame, minimum


def cosine_similarity(p, q):
    numer = np.sum(np.multiply(p, q))
    denom = np.sqrt(np.sum(np.square(p))) * np.sqrt(np.sum(np.square(q)))

    if denom is not 0:
        return float(numer) / denom
    else:
        return 0.0


def euclidean_norm_mean(x, y):
    x = np.mean(x, axis=0)
    y = np.mean(y, axis=0)
    return np.linalg.norm(x - y)


def pad_arrays(arr1, arr2):
    max_shape = np.maximum(arr1.shape, arr2.shape)
    padded_arr1 = np.pad(arr1, ((0, 0),
                                (0, max_shape[1] - arr1.shape[1]),
                                (0, max_shape[2] - arr1.shape[2])),
                         mode='constant', constant_values=0)
    padded_arr2 = np.pad(arr2, ((0, 0),
                                (0, max_shape[1] - arr2.shape[1]),
                                (0, max_shape[2] - arr2.shape[2])),
                         mode='constant', constant_values=0)
    return padded_arr1, padded_arr2
