import streamlit as st
import os
from PIL import Image
import torch
from transformers import ViTFeatureExtractor, ViTForImageClassification
import requests
import warnings
from dotenv import load_dotenv

load_dotenv()

# Ignore warnings
warnings.filterwarnings('ignore')

# API key for nutrition information
api_key = os.getenv("api_key")

# Load the pre-trained Vision Transformer model and feature extractor
model_name = "google/vit-base-patch16-224"
feature_extractor = ViTFeatureExtractor.from_pretrained(model_name)
model = ViTForImageClassification.from_pretrained(model_name)

# Streamlit app title
st.title("Food Identification and Calorie Information")

# Image uploader in Streamlit
uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])

# Function to get food name prediction from the ViT model
def get_food_name(image):
    # Preprocess the image
    inputs = feature_extractor(images=image, return_tensors="pt")
    
    # Get model predictions
    outputs = model(**inputs)
    
    # Get predicted class label
    predicted_class_idx = outputs.logits.argmax(-1).item()
    labels = model.config.id2label
    predicted_label = labels[predicted_class_idx]
    
    return predicted_label

# Function to preprocess the food name (e.g., lowercase and strip spaces)
def preprocess_food_name(food_name):
    return food_name.lower().strip()

# Function to get calorie information using the food name
def get_calorie_info(food_name):
    # Preprocess the food name for better API compatibility
    food_name = preprocess_food_name(food_name)
    
    # Log the query to check if it's valid
    st.write(f"Querying API with: {food_name}")
    
    api_url = f'https://api.api-ninjas.com/v1/nutrition?query={food_name}'
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching calorie info: {response.status_code}")
        st.write(f"Response: {response.text}")
        return None

# Display the uploaded image and process it
if uploaded_file is not None:
    # Load image
    image = Image.open(uploaded_file)
    
    # Display the image
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Get predicted food name
    food_name = get_food_name(image)
    st.write(f"Predicted Food: {food_name}")
    
    # Get calorie information
    calorie_info = get_calorie_info(food_name)
    
    if calorie_info:
        # Display calorie information
        st.write("Calorie Information:")
        st.json(calorie_info)

# Footer instructions
st.write("Upload an image of food, and the app will identify the food and provide its calorie information.")
