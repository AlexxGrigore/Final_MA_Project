import os

import numpy as np
from scipy.io import wavfile
import librosa
from sklearn.decomposition import PCA
import mfcc as compute_mfcc
import video_features

def get_query_descriptor(video, path):
    if len(video.frames) == 0:
        raise Exception("Video length is 0")

    fs, audio_data = get_audio_info(path)

    # Compute the number of audio samples per video frame
    audio_samples_per_frame = int((1 / video.fps) * fs)

    # Initialize feature vectors
    # colorhist = []
    # tempdiff = []
    # audiopowers = []
    mfccs = []
    colorhistdiffs = []

    prev_frame = None
    prev_colorhist = None
    counter = 0

    # Parse video frame-by-frame
    for frame in video.frames:
        # Compute frame color histogram
        hist = video_features.colorhist(frame)
        # colorhist.append(hist)

        # Compute color histogram difference
        diff = 0
        if prev_colorhist is not None:
            diff = video_features.colorhist_diff(prev_colorhist, hist)
        colorhistdiffs.append(diff)

        # Compute temporal difference
        # diff = 0
        # if prev_frame is not None:
        #     diff = video_features.temporal_diff(prev_frame, frame, 10)
        # tempdiff.append(diff)

        # Check if audio frame exceeds the length of the audio
        if counter + audio_samples_per_frame < len(audio_data):
            # Take audio sample
            sample = audio_data[counter: counter + audio_samples_per_frame].astype(float)

            # Extract MFCCs
            # ceps = librosa.feature.mfcc(y=sample, sr=16000, n_mfcc=13)
            ceps = librosa.feature.mfcc(y=sample, sr=16000, n_mfcc=13, n_fft=512, win_length=256)
            #ceps, _, _ = compute_mfcc.mfcc(sample)
            # ----------------------------------------------------
            ceps = np.squeeze(ceps)
            # pca = PCA(n_components=13)
            # ceps = pca.fit_transform(ceps.T).T[:, :13]
            # ----------------------------------------------------

            mfccs.append(ceps)

            counter += audio_samples_per_frame

        prev_frame = frame
        prev_colorhist = hist

    # Build a descriptor for the query video
    descriptor = {'mfcc': np.array(np.squeeze(mfccs)),
                  'chdiff': np.array(colorhistdiffs)}

    return descriptor

def get_audio_info(video_path):
    filename, _ = os.path.splitext(video_path)
    audio_file = "audio_files/" + filename + ".wav"

    # Get the corresponding audio
    sample_rate, data = wavfile.read(audio_file)

    return sample_rate, data
