from preprocessing.preprocess_pipeline import preprocess
from models.mkf_ads import train_mkf_ads

dataset = preprocess(window_size=16)
model = train_mkf_ads(dataset, epochs=10)

print("[INFO] MKF-ADS training completed")