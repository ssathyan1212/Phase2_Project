from preprocessing.preprocess_pipeline import preprocess
from models.mkf_ads import train_mkf_ads
dataset = preprocess()
train_mkf_ads(dataset)
