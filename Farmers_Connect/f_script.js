async function recommendFertilizer() {

    const soilType = document.getElementById('soilType').value;
    const ph = document.getElementById('ph').value;
    const nitrogen = document.getElementById('nitrogen').value;
    const phosphorus = document.getElementById('phosphorus').value;
    const potassium = document.getElementById('potassium').value;
    const temperature = document.getElementById('temperature').value;
    const humidity = document.getElementById('humidity').value;
    const rainfall = document.getElementById('rainfall').value;
    const cropType = document.getElementById('cropType').value;
    const growthStage = document.getElementById('growthStage').value;
    const season = document.getElementById('season').value;

    if (!soilType || !ph || !nitrogen || !phosphorus || !potassium || 
        !temperature || !humidity || !rainfall || 
        !cropType || !growthStage || !season) {

        alert("Please fill all fields");
        return;
    }

    const resultDiv = document.getElementById("fertilizer-result");
    const fertOutput = document.getElementById("fertilizer-output");
    const doseOutput = document.getElementById("dosage-output");

    fertOutput.innerText = "Analyzing...";
    doseOutput.innerText = "";

    resultDiv.classList.remove("hidden");

    const data = {
        soilType,
        ph: parseFloat(ph),
        nitrogen: parseFloat(nitrogen),
        phosphorus: parseFloat(phosphorus),
        potassium: parseFloat(potassium),
        temperature: parseFloat(temperature),
        humidity: parseFloat(humidity),
        rainfall: parseFloat(rainfall),
        cropType,
        growthStage,
        season
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error("Server error");

        const result = await response.json();

        fertOutput.innerText = "👉 " + result.fertilizer;
        doseOutput.innerText = "👉 " + result.dosage;

    } catch (error) {
        console.error(error);
        fertOutput.innerText = "Error getting result";
        doseOutput.innerText = "";
        alert("Server connection failed");
    }
}