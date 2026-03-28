import json
from streamlit_lottie import st_lottie

def load_lottie(path):
    with open(path) as f:
        return json.load(f)

def show_lottie(path, height=200):
    animation = load_lottie(path)
    st_lottie(animation, height=height)