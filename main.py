import pandas as pd
from src.train_model import train_model # type: ignore

# Load dataset
df = pd.read_csv("data/crime_dataset_india.csv")

# Train model
train_model(df)
