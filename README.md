# Image app
Implement a simple image app using tkinter.
## Introduction
### Functionality
* Open/Save images
* Crop images multiple times
* Image matting

### Interface
#### Basic
![app](asset/app.png)
Function buttons are **Open Image**, **Save Image**, **Crop Image**, **Mat Image**, and **Reset Image** from left to right.

#### Open/Save Image
Choose the image wanting to open and specify the filename wanting to save.
#### Crop Image
![crop](asset/crop.png)
Drag with mouse to select desired corpping window.
#### Mat Image
![mat](asset/mat.png)
Select two colors, and remove the colors thats between the two.
#### Reset
Reset the image to the original image that was loaded when **Open Image**


## Usage
### Install packages
```bash
pip3 install -r requirements.txt
```

### Run the app
```bash
python3 src/gui.py
```