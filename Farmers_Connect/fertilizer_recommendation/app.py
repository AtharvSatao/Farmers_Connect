from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

model = pickle.load(open("model.pkl", "rb"))
le_soil = pickle.load(open("le_soil.pkl", "rb"))
le_crop = pickle.load(open("le_crop.pkl", "rb"))
le_stage = pickle.load(open("le_stage.pkl", "rb"))
le_season = pickle.load(open("le_season.pkl", "rb"))
le_fert = pickle.load(open("le_fert.pkl", "rb"))

def safe_transform(le, value):
    if value in le.classes_:
        return le.transform([value])[0]
    return 0

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    soil = safe_transform(le_soil, data["soilType"])
    crop = safe_transform(le_crop, data["cropType"])
    stage = safe_transform(le_stage, data["growthStage"])
    season = safe_transform(le_season, data["season"])

    n = float(data["nitrogen"])
    p = float(data["phosphorus"])
    k = float(data["potassium"])

    input_data = [[
        soil,
        float(data["ph"]),
        n,
        p,
        k,
        float(data["temperature"]),
        float(data["humidity"]),
        float(data["rainfall"]),
        crop,
        stage,
        season
    ]]

    prediction = model.predict(input_data)
    fertilizer = le_fert.inverse_transform(prediction)[0]

    if n < 50:
        dosage = "150 kg/acre (Low Nitrogen)"
    elif p < 30:
        dosage = "120 kg/acre (Low Phosphorus)"
    elif k < 30:
        dosage = "110 kg/acre (Low Potassium)"
    else:
        dosage = "80 kg/acre (Balanced Soil)"

    return jsonify({
        "fertilizer": fertilizer,
        "dosage": dosage
    })

if __name__ == "__main__":
    app.run(debug=True)