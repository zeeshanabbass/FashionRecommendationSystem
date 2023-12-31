import tensorflow
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50,preprocess_input
import numpy as np
from numpy.linalg import norm
import pickle
from sklearn.neighbors import NearestNeighbors
import cv2

model=ResNet50(weights='imagenet',include_top=False,input_shape=(224,224,3))
model.trainable = False
model = tensorflow.keras.Sequential([
    model,
    GlobalMaxPooling2D()
])

feature_list = pickle.load(open('embeddings.pkl','rb'))
filenames = pickle.load(open('filenames.pkl','rb'))

img = image.load_img('sample/n02788148_10.JPEG', target_size=(224,224,3))
img_array = image.img_to_array(img)
expanded_img_array = np.expand_dims(img_array, axis=0)
preprocess_img = preprocess_input(expanded_img_array)
result = model.predict(preprocess_img).flatten()
normalized_result = result / norm(result)

neighbours = NearestNeighbors(n_neighbors=6,algorithm='brute',metric='euclidean')
neighbours.fit(feature_list)

distances,indices = neighbours.kneighbors([normalized_result])

print(indices)

for file in indices[0][1:6]:
    temp_img = cv2.imread(filenames[file])
    cv2.imshow('output',cv2.resize(temp_img,(224,224)))
    cv2.waitKey(0)
