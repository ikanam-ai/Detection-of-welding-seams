import pandas as pd
import streamlit as st
import requests
import json
import cv2
import numpy as np
from PIL import Image

def draw_bounding_box(image, box, class_id, class_names, color=(255, 0, 0), box_thickness=1, font_scale=0.5, font_thickness=1):
    """
    Рисует bounding box на изображении.
    
    image: изображение в формате numpy array
    box: кортеж (x_center, y_center, width, height) в формате YOLO
    class_id: идентификатор класса
    class_names: список имен классов
    color: цвет bounding box и текста (по умолчанию синий)
    box_thickness: толщина линий bounding box
    font_scale: масштаб шрифта для текста
    font_thickness: толщина шрифта для текста
    """
    height, width, _ = image.shape
    x_center, y_center, w, h = box
    
    # Преобразование из нормализованных координат YOLO в пиксели
    xmin = int((x_center - w / 2) * width)
    xmax = int((x_center + w / 2) * width)
    ymin = int((y_center - h / 2) * height)
    ymax = int((y_center + h / 2) * height)
    
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, box_thickness)
    
    label = f"{class_names[class_id]}"
    (label_width, label_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
    
    # Рисуем фон для текста
    cv2.rectangle(image, (xmin, ymin - label_height - baseline), (xmin + label_width, ymin), color, cv2.FILLED)
    # Рисуем текст
    cv2.putText(image, label, (xmin, ymin - baseline), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)

def visualize_annotations(image, annotation_content, class_names, color=(255, 0, 0), box_thickness=1, font_scale=0.5, font_thickness=1):
    """
    Визуализирует аннотации на изображении.
    
    image: изображение в формате PIL Image
    annotation_content: содержимое YOLO файла аннотаций
    class_names: список имен классов
    color: цвет bounding box и текста (по умолчанию синий)
    box_thickness: толщина линий bounding box
    font_scale: масштаб шрифта для текста
    font_thickness: толщина шрифта для текста
    """
    # Конвертация изображения в формат numpy
    image = np.array(image)
    for line in annotation_content.splitlines():
        parts = line.strip().split()
        class_id = int(parts[0])
        box = tuple(map(float, parts[1:]))
        draw_bounding_box(image, box, class_id, class_names, color, box_thickness, font_scale, font_thickness)
    
    # Преобразование изображения из BGR (формат OpenCV) в RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image



def main():
    #st.header("ikanam-ai✔️", divider='rainbow')

    st.title("Приведение номенклатуры к официальному Классификатору Строительных Ресурсов")
    txt = st.text_area(
        "⚙️ Как это работает?",
        "Модель на основе ИИ анализирует введенные данные, "
        "используя NLP для распознавания и сопоставления с классификатором,"
        "и возвращает результат с процентом точности."
        )

    tab1, tab2 = st.tabs(["Одно наименование😎📊", "CSV-файл🚀💻"])
    

    with tab1:
        st.title("Загрузка и отображение изображения")

# Форма для загрузки изображения
        uploaded_image = st.file_uploader("Выберите изображение...", type=["jpg", "jpeg", "png"])

# Загрузка аннотации
        uploaded_annotation = st.file_uploader("Загрузите файл аннотации YOLO...", type=["txt"])

        class_names = ['crazing', 'inclusion', 'patches', 'pitted_surface', 'rolled-in_scale', 'scratches']

        # Если файл загружен
        if uploaded_image is not None and uploaded_annotation is not None:
            image = Image.open(uploaded_image)
            annotation_content = uploaded_annotation.read().decode('utf-8')

            # Визуализация
            annotated_image = visualize_annotations(image, annotation_content, class_names)

            # Отображение с использованием Streamlit
            st.image(annotated_image, caption='Изображение с аннотациями', use_column_width=True)

        

if __name__ == "__main__":
    main()