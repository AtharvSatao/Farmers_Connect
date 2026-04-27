import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

data = pd.read_csv("fertilizer_recommendation.csv")

data.columns = data.columns.str.strip()

le_soil = LabelEncoder()
le_crop = LabelEncoder()
le_stage = LabelEncoder()
le_season = LabelEncoder()
le_fert = LabelEncoder()

data["Soil_Type"] = le_soil.fit_transform(data["Soil_Type"])
data["Crop_Type"] = le_crop.fit_transform(data["Crop_Type"])
data["Crop_Growth_Stage"] = le_stage.fit_transform(data["Crop_Growth_Stage"])
data["Season"] = le_season.fit_transform(data["Season"])
data["Recommended_Fertilizer"] = le_fert.fit_transform(data["Recommended_Fertilizer"])

X = data[[
"Soil_Type",
"Soil_pH",
"Nitrogen_Level",
"Phosphorus_Level",
"Potassium_Level",
"Temperature",
"Humidity",
"Rainfall",
"Crop_Type",
"Crop_Growth_Stage",
"Season"
]]

y = data["Recommended_Fertilizer"]

model = RandomForestClassifier()
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(le_soil, open("le_soil.pkl", "wb"))
pickle.dump(le_crop, open("le_crop.pkl", "wb"))
pickle.dump(le_stage, open("le_stage.pkl", "wb"))
pickle.dump(le_season, open("le_season.pkl", "wb"))
pickle.dump(le_fert, open("le_fert.pkl", "wb"))