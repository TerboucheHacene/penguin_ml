from fastapi import FastAPI, Depends, status
from fastapi.exceptions import HTTPException
from typing import Optional
from app.schemas import (
    PenguinDataInput,
    PenguinClassOutput,
    PenguinModelInput,
    Settings,
)
import pickle
from sklearn.ensemble import RandomForestClassifier
from app.schemas import Sex, Island

app = FastAPI()

settings = Settings(
    model_path="models/random_forest_penguin.pickle",
    unique_mapping="models/output_penguin.pickle",
)


class PredictPenguinClass:
    def load_model(self):
        rf_pickle = open(settings.model_path, "rb")
        map_pickle = open(settings.unique_mapping, "rb")
        rfc: RandomForestClassifier = pickle.load(rf_pickle)
        unique_penguin_mapping = pickle.load(map_pickle)
        rf_pickle.close()
        map_pickle.close()

        self.model = rfc
        self.mapping = unique_penguin_mapping

    async def predict(self, input: PenguinDataInput) -> PenguinClassOutput:
        if not self.model:
            raise RuntimeError
        else:
            input = input.dict()
            if input["sex"] == Sex.MALE:
                input["sex_male"] = 1
                input["sex_female"] = 0
            elif input["sex"] == Sex.FEMALE:
                input["sex_male"] = 0
                input["sex_female"] = 1

            if input["island"] == Island.BISCOE:
                input["island_biscoe"] = 1
                input["island_dream"] = 0
                input["island_torgerson"] = 0
            elif input["island"] == Island.DREAM:
                input["island_biscoe"] = 0
                input["island_dream"] = 1
                input["island_torgerson"] = 0
            elif input["island"] == Island.TORGERSEN:
                input["island_biscoe"] = 0
                input["island_dream"] = 0
                input["island_torgerson"] = 1
            input.pop("sex")
            input.pop("island")
            model_input = PenguinModelInput(**input)
            prediction = self.model.predict([[*model_input.dict().values()]])
            prediction = self.mapping[prediction][0]
        return PenguinClassOutput(species=prediction)


prediction_model = PredictPenguinClass()


@app.on_event("startup")
def startup():
    print(".... loading")
    prediction_model.load_model()
    print("Model Loaded ....")


@app.get("/", status_code=status.HTTP_200_OK, tags=["general"])
def _index():
    """Health Check"""
    return {"status": "Ok"}


@app.post("/predict", status_code=status.HTTP_200_OK)
async def predict(
    output: PenguinClassOutput = Depends(prediction_model.predict),
) -> PenguinClassOutput:
    return output
