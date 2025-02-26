from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
import sys
import time
import json

import streamlit as st
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

with open("secret.json") as f:
    secret = json.load(f)

KEY = secret["KEY"]
ENDPOINT = secret["ENDPOINT"]
computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def get_tags(filepath):
    locl_image=open(filepath, "rb")
    tags_result = computervision_client.tag_image_in_stream(locl_image)
    tags = tags_result.tags
    tags_name = []
    for tag in tags:
      tags_name.append(tag.name)
    return tags_name

def detect_objects(filepath):
    locl_image=open(filepath, "rb")
    detect_objects_results = computervision_client.detect_objects_in_stream(locl_image)
    objects = detect_objects_results.objects

    return objects

st.title("物体検出アプリ")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

if uploaded_file is not None:
  img = Image.open(uploaded_file)
    
  #アップロードしたファイルをimgフォルダに保存して読みだす
  img_path = f"img/{uploaded_file.name}"
  img.save(img_path)
  objects = detect_objects(img_path)

  #描画
  draw = ImageDraw.Draw(img)   
  for object in objects:
    x = object.rectangle.x
    y = object.rectangle.y
    w = object.rectangle.w
    h = object.rectangle.h
    caption = object.object_property 

    textsize =50
    font = ImageFont.truetype(font="Helvetica 400.ttf", size=textsize)

    a, b, text_w, text_h = draw.textbbox((x, y), caption, font=font)

    draw.rectangle([(x, y), (x+w, y+h)], fill=None,outline="green",width=5)
    draw.rectangle([(x, y), (text_w, text_h)], fill='Green', width=5)
    draw.text((x,y), caption, fill="white", font=font)



 #表示
  st.image(img)


  tags_name = get_tags(img_path)
  tags_name = ", ".join(tags_name)

  st.markdown("**認識されたコンテンツタグ**")
  st.markdown(tags_name)
