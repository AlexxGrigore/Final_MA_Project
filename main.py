from process_video import process_videos
from database import *
import os


def main():
    # List of all videos in the dataset
    videos = os.listdir("dataset")
    video_and_audio_paths = ["dataset/" + s for s in videos]
    video_paths = []
    for s in video_and_audio_paths:
        _, extension = os.path.splitext(s)
        if not extension == '.wav':
            video_paths.append(s)

    # Create database
    connection = create_database("database/videos.sqlite")

    # Create database table for storing videos
    create_table(connection)
    # video_paths = ['dataset/Lemmings.mp4', 'dataset/BlackKnight.avi', 'dataset/Danger_Humans.mp4']
    # video_paths = ['dataset/Lemmings.mp4']

    process_videos(video_paths, connection)

    connection.close()


if __name__ == '__main__':
    main()
