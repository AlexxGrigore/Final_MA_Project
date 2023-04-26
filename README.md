# ScreenCheck

###### Invention Assignment Project, by group 25

###### Members: Alexandru Grigore, Camil-Cristian Dobos

## Description

The following system recognizes the name of the video that is being recorded, if that video is included in our dataset.

## How to use the system

First you need to create a database that stores the feature descriptors of the videos from the dataset.

Follow the following steps:

1. Create a folder in the main project named **'database'**
2. In that folder create a sqlite database named 'video.sqlite'. To do that in PyCharm, you select new, Data Source
   Path, and then set the name to **'video.sqlite'**
3. Create a new folder in the main project named **'dataset'** and paste the videos (the ones from Brightspace)
4. Run the **main.py** script (it will take quite some time). If you want to skip those steps, just download teh databse from the following link and place it in the folder: -------.

Now you are ready to use the application. 

In order to do that, execute the **application.py** file and follow the steps explained there.
In summary, you press:
- 1 if you want to test the system on your own video
- 2 if you want to use the default video to test it
- 3 if you want to run the system on all the videos from the folder tests and see the evaluation metrics.





