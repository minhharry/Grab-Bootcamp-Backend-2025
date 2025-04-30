import torch
import open_clip
from contextlib import asynccontextmanager

ml_models = {}

def load_model():
    print("[INFO] Loading model...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model, _, preprocess = open_clip.create_model_and_transforms(
        'ViT-H-14-378-quickgelu', pretrained='dfn5b'
    )
    model.to(device)
    model.eval()
    ml_models["clip_model"] = model
    ml_models["preprocess"] = preprocess
    ml_models["device"] = device
    print("[INFO] Model loaded on", device)

def cleanup_model():
    print("[INFO] Cleaning up model...")
    ml_models.clear()

