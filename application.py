import time

import CropVideo
import VideoReader
import video_query
from match import *


def run_query_for_a_video(path="test/test_danger_humans.mp4"):
    start_time = time.time()

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

    if name is None or score < 0.7:
        print("No match found for the given video")
        return 'no match'

    print("Best match found for video {} with a score of {} at frame {} and it took {} seconds".format(name, score,
                                                                                                       frame,
                                                                                                       end_time - start_time))
    return name




def evaluate_performance():
    answers_dict = {'open_education_week_1.mp4': 'Open_Education_Week1.mp4',
                    'test_crop_asteroid.mp4': 'Asteroid_Discovery.mp4', 'test_deltaiv.mp4': 'DeltaIV.mp4',
                    'test_kerbal_2.mp4': 'Kerbal_Space_Program2.mp4', 'test_oversight.mp4': 'Oversight.mp4',
                    'test_the_image_that_can_break_your_brain.mp4': 'The_Image_That_Can_Break_Your_Brain.mp4',
                    'test_TUDelft.mp4': 'TUDelft.mp4',
                    'test_tudelft_ambulance_drone.mp4': 'TUDelft_Ambulance_Drone.mp4',
                    'test_welcome_to_life.mp4': 'Welcome_To_Life.mp4', 'test_danger_humans.mp4': 'Danger_Humans.mp4',
                    'not_in_dataset.mp4': 'no match'}

    test_videos_names = ['open_education_week_1.mp4', 'test_crop_asteroid.mp4', 'test_deltaiv.mp4', 'test_kerbal_2.mp4',
                         'test_oversight.mp4', 'test_the_image_that_can_break_your_brain.mp4', 'test_TUDelft.mp4',
                         'test_tudelft_ambulance_drone.mp4', 'test_welcome_to_life.mp4', 'test_danger_humans.mp4']

    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0

    for video_name in test_videos_names:
        answer = run_query_for_a_video('test/' + video_name)

        if answer != "no match":
            if answers_dict[video_name] == answer:
                true_positive += 1
            else:
                false_positive += 1
        else:
            if answers_dict[video_name] == answer:
                true_negative += 1
            else:
                false_negative += 1

    print('true_positive = {}'.format(true_positive))
    print('true_negative = {}'.format(true_negative))
    print('false_positive = {}'.format(false_positive))
    print('false_negative = {}'.format(false_negative))

    accuracy = (true_negative + true_positive) / (true_negative + true_positive + false_negative + false_positive)
    print('The accuracy is: {}'.format(accuracy))


def main():
    print("Press 1 if you want to use your own test video")
    print("Press 2 if you want to use the default test video")
    print("Press 3 if you want to evaluate the accuracy on all test videos")

    choice = int(input("Enter a number: "))

    if choice == 1:
        print("example of a path: test/test_danger_humans.mp4")
        path = input("Enter your path: ")
        run_query_for_a_video(path)
    elif choice == 2:
        path = "test/test_danger_humans.mp4"
        run_query_for_a_video(path)
    elif choice == 3:
        evaluate_performance()
    else:
        print("that is not an option")


if __name__ == "__main__":
    main()