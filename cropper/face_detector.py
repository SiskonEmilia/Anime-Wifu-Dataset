import cv2
import sys
from tqdm import tqdm
import os.path

def detect(source_dir, target_dir,cascade_file='./lbpcascade_animeface.xml'):
  if not os.path.isfile(cascade_file):
    raise RuntimeError(f'{cascade_file} not found')
  
  cascade = cv2.CascadeClassifier(cascade_file)

  pbar = tqdm(os.walk(source_dir))

  for dirpath, dirnames, filenames in pbar:
    for filename in filenames:
      src_path  = os.path.join(dirpath, filename)
      tar_path  = os.path.join(target_dir, dirpath.split('/')[-1], filename)
      image     = cv2.imread(src_path, cv2.IMREAD_COLOR)
      gray      = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      gray      = cv2.equalizeHist(gray)
      faces     = cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(64, 64))
      for i, (x, y, w, h) in enumerate(faces):
        cv2.imwrite(tar_path, image[y:y+h, x:x+w])

detect(sys.argv[1], sys.argv[2])

