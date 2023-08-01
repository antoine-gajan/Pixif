# Pixif

## 💻︎ Contents of the repository :

This repository contains the source code of the Pixif application, which allows you to sort or find your photos and videos according to the place where they were taken.

## 💡Proposed Features:

The application offers 2 main features:
- sort photos by location and/or date of taking
- find photos taken in a certain place

### Sort your pictures

You have the choice to sort your photos by location, date or both. You must then choose a source directory (containing the photos) and a destination directory (containing the sorted photos). It is possible to choose the same folder for simplicity.
![alt text](https://github.com/antoine-gajan/Pixif/blob/master/assets/sort.png)
![alt text](https://github.com/antoine-gajan/Pixif/blob/master/assets/sorting.png)
![alt text](https://github.com/antoine-gajan/Pixif/blob/master/assets/sorted.png)

The application gives you the choice to generate or not a world map with your photos on it. If you choose this option, then you will get a map.html file in the sorted folder containing the different photos instead of taking them. In particular, if you want to enlarge a photo in a pop-up, just click on the photo in question.
![alt text](https://github.com/antoine-gajan/Pixif/blob/master/assets/map.png)


### Find your pictures

Thanks to the EXIF data, the application allows you to find the photos taken in a certain place. You can choose an exact or approximate match. The application will show all the corresponding photos if it found any.
![alt text](https://github.com/antoine-gajan/Pixif/blob/master/assets/find.png)

## 💡Execute the code:

To run the application in the best conditions, you will need to load the Exiftool tool to allow you to extract the EXIF data from the videos. Otherwise, the code will only work for image files.
In the file file_metadata.py, it is necessary to modify the variable "exe" so that it contains the path to exiftool.exe to be able to obtain the exif data of the videos.

## 🧑‍💻 Technologies used:

This application was encoded in Python using different libraries that allow to analyze the EXIF data of files.

