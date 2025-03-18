# photo-composition-detector

This repo will be using computer vision techniques on photos focusing on photo composition. This is inspired by my dissertation work using the Golden Spiral for visual privacy scoring. 

Photo composition is the arrangement of visual elements within a photograph's frame. The photo's composition can influence how people look at your photo; this can direct the eye to an object or subject. A few techniques this repo will look at are: 
- Fill the frame (Object Area Ratio - Dissertation Ch 5)
- Rule of Thirds 
- Golden Spiral (Dissertation Ch 5)
- Leading Lines (TBD)
- Similarity (New)

This repo will also look at image bounding and segmentation.


## Project Setup 
I have used ```pyenv``` for python version management and virtual envirnoment management.
This repo uses ```Python 3.11``` since [```Pytorch```](https://pytorch.org/get-started/locally/) has not been updated to the latest version of Python (3.13).

```sh
pyenv install 3.11
pyenv virtualenv 3.11 composer
pyenv activate composer
pip install -r requirements.txt
```

## Image Similarity
A system that can compare two images and determine how similar they are. Uses ORB (a fast and efficient method) to extract features from images. ORB is less computationally expensive than SIFT.
The code can be found in ```similarity/``` folder with run details.
![image](https://github.com/user-attachments/assets/57aead9a-9107-442b-9f17-248bdc580055)


### Notes: 

I ran into an issue with Torch and Numpy 2.2.4. Downgraded Numpy to 1.26.4
```
RuntimeError: Numpy is not available
pip install numpy==1.26.4
```


### Other notes:
To save modules and verisons using pipreqs
```sh
pip install pipreqs
```

To generate a requirements.txt file, all you have to do is run the following command.
``` sh
 pipreqs
 ```

If the requirements.txt file already exists, then run the following command:
```sh
pipreqs --force
```


