import cv2
import os
import numpy as np
import shutil
import random

from sklearn.cluster import KMeans
from concurrent.futures import ThreadPoolExecutor


def load_img(img_name):
    try:
        # load img - below meathod could read korean filename
        img = np.fromfile(os.path.join(image_path, img_name), np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        # Convert RGB to Gray
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Nomalization
        img = cv2.resize(img, dsize=(128, 128), interpolation=cv2.INTER_AREA)
        img = img.astype("float32") / 255.0
    except Exception as e:
        return None, None
    else:
        return img, img_name


# read image list
image_path = r"D:\PetImages"
image_list = []

for folder in ["Cat", "Dog"]:
    for img_name in os.listdir(os.path.join(image_path, folder)):
        image_list.append(f"{folder}/{img_name}")

random.shuffle(image_list)
random.shuffle(image_list)


train_data_list = []
train_img_list = []
train_label_list = []

with ThreadPoolExecutor(max_workers=10) as pool:
    train_data_list = pool.map(
        load_img,
        image_list,
    )

for result in train_data_list:
    data, label = result
    if data is not None:
        train_img_list.append(data)
        train_label_list.append(label)

train_img_list = np.array(train_img_list)
train_img_list = train_img_list.reshape(len(train_img_list), -1)

print(train_img_list.shape)

model = KMeans(init="k-means++", n_clusters=2, random_state=0, max_iter=100)
model.fit(train_img_list)
y_pred = model.labels_

dog_cnt = 0
cat_cnt = 0
for pred, name in zip(y_pred, train_label_list):
    if pred == 0:
        dog_cnt += 1
    else:
        cat_cnt += 1

print("dog_cnt", dog_cnt)
print("cat_cnt", cat_cnt)

# copy image by clustered result
new_path = r"D:\PetImages"

for label, name in zip(y_pred, train_label_list):
    os.makedirs(os.path.join(new_path, str(label)), exist_ok=True)
    shutil.copy2(
        os.path.join(image_path, name),
        os.path.join(os.path.join(new_path, str(label)), name.split("/")[-1]),
    )
