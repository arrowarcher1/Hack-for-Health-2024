
# all imports required
import PySimpleGUI as sg
from typing import Dict
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from google.cloud import aiplatform
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/andrewvanostrand/Downloads/ecstatic-acumen-414422-1ae2f6a24607.json"

def predict_tabular_classification_sample(
    project: str,
    endpoint_id: str,
    instance_dict: Dict,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    client_options = {"api_endpoint": api_endpoint}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    instance = json_format.ParseDict(instance_dict, Value())
    instances = [instance]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    predictions = response.predictions
    
    # Break up predictions
    prediction_result = predictions[0]

    # Find the max score
    max_score_index = prediction_result['scores'].index(max(prediction_result['scores']))
    predicted_class = prediction_result['classes'][max_score_index]

    # Calculate the percentage
    score_percentage = prediction_result['scores'][max_score_index] * 100

    return predicted_class, score_percentage

def main():
    items = {
        "Age": "Enter Age:",
        "Gender": "Enter Gender (1 for Male, 2 for Female): ",
    "AirPollution": "Enter Air Pollution level (1-10): ",
    "Alcoholuse": "Enter Alcohol use level (1-10): ",
    "DustAllergy": "Enter Dust Allergy level (1-10): ",
    "OccuPationalHazards": "Enter Occupational Hazards level (1-10): ",
    "GeneticRisk": "Enter Genetic Risk level (1-10): ",
    "chronicLungDisease": "Enter Chronic Lung Disease level (1-10): ",
    "BalancedDiet": "Enter Balanced Diet level (1-10): ",
    "Obesity": "Enter Obesity level (1-10): ",
    "Smoking": "Enter Smoking level (1-10): ",
    "PassiveSmoker": "Enter Passive Smoker level (1-10): ",
    "ChestPain": "Enter Chest Pain level (1-10): ",
    "CoughingofBlood": "Enter Coughing of Blood level (1-10): ",
    "Fatigue": "Enter Fatigue level (1-10): ",
    "WeightLoss": "Enter Weight Loss level (1-10): ",
    "ShortnessofBreath": "Enter Shortness of Breath level (1-10): ",
    "Wheezing": "Enter Wheezing level (1-10): ",
    "SwallowingDifficulty": "Enter Swallowing Difficulty level (1-10):",
    "ClubbingofFingerNails": "Enter Clubbing of Finger Nails level (1-10): ",
    "FrequentCold": "Enter Frequent Cold level (1-10): ",
    "DryCough": "Enter Dry Cough level (1-10): ",
    "Snoring": "Enter Snoring level (1-10): "
        # Add more items as needed
    }

    user_inputs = {}

    # Create PySimpleGUI layout for input window
    layout_input = []
    for item, prompt in items.items():
        layout_input.append([sg.Text(prompt, size=(40, 1)), sg.InputText(key=item, size=(20, 1))])

    layout_input.append([sg.Button('Ok'), sg.Button('Cancel')])

    # Create input window
    window_input = sg.Window('Lung Cancer Risk Screener', layout_input, size=(1728, 1117), font=("Helvetica", 29    ))

    # Event loop for input window
    while True:
        event_input, values_input = window_input.read()
        if event_input == sg.WIN_CLOSED or event_input == 'Cancel':
            break
        if event_input == 'Ok':
            # Convert input values to correct data types
            invalid_input = False
            for item in items:
                user_input = values_input[item].strip()
                if not user_input:
                    sg.popup_error(f"Please enter a value for '{item}'.")
                    invalid_input = True
                    break
                user_inputs[item] = user_input

            if invalid_input:
                continue

            window_input.close()
            break

    if event_input == 'Ok':
        # Call the predict_tabular_classification_sample function with the user inputs
        predicted_class, score_percentage = predict_tabular_classification_sample(
            project=projectID,
            endpoint_id=endpointID,
            instance_dict=user_inputs,
            location="us-central1"
        )

        # Create PySimpleGUI layout for result window
        layout_result = [
            [sg.Text("\n\n\n\n")],
            [sg.Text(f'Predicted class: {predicted_class} chance of cancer with a confidence of {score_percentage:.2f}%')],
            [sg.Button('Ok')],
            [sg.Text("\n\n\n\n\n\n\n\n\n\n\n\n\n")]
        ]

        # Create result window
        window_result = sg.Window('Prediction Result', layout_result, size=(1728, 1117), font=("Helvetica", 45, 'bold'))

        # Event loop for result window
        while True:
            event_result, _ = window_result.read()
            if event_result == sg.WIN_CLOSED or event_result == 'Ok':
                break

        window_result.close()

if __name__ == '__main__':
    main()
