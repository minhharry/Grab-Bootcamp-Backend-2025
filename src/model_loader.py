import torch
import open_clip

print("[INFO] Loading model...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
model, _, preprocess = open_clip.create_model_and_transforms(
    'ViT-H-14-378-quickgelu', pretrained='dfn5b'
)
model.to(device)
model.eval()
