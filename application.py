import time

import CropVideo
import VideoReader
import video_query
from match import *


def main():
    start_time = time.time()

    path = "test/test_danger_humans.mp4"
    database_path = "database/videos.sqlite"

    # Create VideoReader object
    reader = VideoReader.VideoReader(path)
    print("Read the query video")

    # Crop the video only to contain the video contents
    cropped_video = CropVideo.crop_video(reader)

    # Find descriptor
    descriptor = video_query.get_query_descriptor(cropped_video, path)
    print("Got query descriptor")

    # Match with one of the videos in the database
    name, score, frame = find_match(descriptor, database_path)

    end_time = time.time()

    if name is None or score < 0.5:
        print("No match found for the given video")
    else:
        print("Best match found for video {} with a score of {} at frame {} and it took {} seconds".format(name, score,
                                                                                                           frame,
                                                                                                           end_time - start_time))


if __name__ == "__main__":
    main()


def evaluate_performance():
    answers_dict = {'open_education_week_1.mp4': 'Open_Education_Week1.mp4',
                    'test_crop_asteroid.mp4': 'Asteroid_Discovery.mp4', 'test_deltaiv.mp4': 'DeltaIV.mp4',
                    'test_kerbal_2.mp4': 'Kerbal_Space_Program2.mp4', 'test_oversight.mp4': 'Oversight.mp4',
                    'test_the_image_that_can_break_your_brain.mp4': 'The_Image_That_Can_Break_Your_Brain.mp4',
                    'test_TUDelft.mp4': 'TUDelft.mp4',
                    'test_tudelft_ambulance_drone.mp4': 'TUDelft_Ambulance_Drone.mp4',
                    'test_welcome_to_life.mp4': 'Welcome_To_Life.mp4', 'test_danger_humans.mp4': 'Danger_Humans.mp4'}

    test_videos_names = ['open_education_week_1.mp4', 'test_crop_asteroid.mp4', 'test_deltaiv.mp4', 'test_kerbal_2.mp4',
                         'test_oversight.mp4', 'test_the_image_that_can_break_your_brain.mp4', 'test_TUDelft.mp4',
                         'test_tudelft_ambulance_drone.mp4', 'test_welcome_to_life.mp4', 'test_danger_humans.mp4']
