import cv2
from moviepy.editor import *

class VideoReader:
    def __init__(self, path=None, fps=None, frames=None):
        self.path = path
        if fps is None or frames is None:
            # Read videos
            self.fps, self.frames = self.readVideo(path)
        else:
            self.fps = fps
            self.frames = frames

        self.read_audio()


    def readVideo(self, path):
        cap = cv2.VideoCapture(path)

        # Get video frames per second
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if not cap.isOpened():
            raise Exception("Not read file")
        # Initialize frames as an empty list
        frames = []
        for i in range(total_frames):
            # Read video frame by frame
            ret, frame = cap.read()

            if ret == True:
                # Append frame to the list of frames
                frames.append(frame)
            else:
                break
        # Close video file
        cap.release()
        cv2.destroyAllWindows()

        return fps, frames

    def read_audio(self):
        # Extract audio from video
        audio = AudioFileClip(self.path)

        filename, _ = os.path.splitext(self.path)

        # Extract the name of the video
        #name = filename.split("/", 1)[0].rstrip()

        # Create new file for audio
        audio_file = filename + ".wav"

        # Write audio to file
        audio.write_audiofile("audio_files/" + audio_file)

    def display_video(self):
        for frame in self.frames:
            cv2.imshow('Video', frame)

            if cv2.waitKey(self.fps) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
