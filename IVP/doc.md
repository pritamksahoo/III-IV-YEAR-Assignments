## Marks extraction from Answersheets (Image) in Tabular Form
There are three python files which act as modules and perform three seperate functions, and one main.py.
The Three files are - 
- **extract_ROI.py** <br>
  - Rectifies the orientation of the image to portrait form.<br>
  - Extract the ROI (Table containing marks), with help of Canny Edge Detection, Contour Detection, and Perspective Transformation.<br>
  - Detect each individual cell of the table, using Hough Transformation (Line Detection).<br>
- **number_extraction.py** <br>
  - Remove extra border pixels from the cells using color based thresholding in HSV color space.<br>
  - Binary Thresholding and morphological closing on each cell.<br>
  - Used Contour Detection to extract individual digits and decimal point using some area approximation.<br>
- **number_detection.py** <br>
  - Thresholded (OTSU's Binarization) and resized the image of each digit into 28x28.
  - Used MNIST based digit prediction model (After some manual training upon pre-existed model) to detect each digit of the cells.
