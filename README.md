# Penguin Classifier
* Build and train a machine learning classification model for penguin type
* Deploy the trained model using FastAPI and Docker
* Streamlit App to showcase the model &amp; present data anlysis results. 
* You can test the app on <https://share.streamlit.io/terbouchehacene/penguin_ml/main/streamlit_app/penguin_streamlit.py>

![Alt text](/images/species.png "The data frame head")

## How to run 
---
* Clone this repo, it contains everything you need
* Install [poetry](https://python-poetry.org/docs/) (a tool for dependency management and packaging in Python)
    ```bash
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
    ```
* Install the dependencies:
    ```
    poetry install
    ```
* Execute the following command to activate the environment:
    ```
    poetry shell
    ```

## Data:
---
Data were collected and made available by [Dr. Kristen Gorman](https://www.uaf.edu/cfos/people/faculty/detail/kristen-gorman.php) and [ Palmer Station, Antarctica LTER](https://pal.lternet.edu/). It is also available on [Kaggle](https://www.kaggle.com/parulpandey/palmer-archipelago-antarctica-penguin-data?select=penguins_size.csv). It has observations about 3 different kinds of penguins, for the years between **2007** and **2009**, with the following features:

- `species`: penguin species (Chinstrap, Adélie, or Gentoo). This is the the target variable.
- `bill_length_mm`: culmen length (mm)
- `bill_depth_mm`: culmen depth (mm)
- `flipper_length_mm`: flipper length (mm)
- `body_mass_g`: body mass (g)
- `island`: island name (Dream, Torgersen, or Biscoe) in the Palmer Archipelago (Antarctica)
- `sex`: penguin sex

The data is a csv file in [/data/penguins.csv](/data/penguins.csv) that has **344** rows and **8** columns. 

![Alt text](/images/data_head.png "The data frame head")

## Modeling
---
A basic *Random Forest* Classifier is used to predict the species of penguins (see [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)). This is not the best model ever but can be a good baseline for further finetuning. The variables `bill_length_mm`, `bill_depth_mm`, `flipper_length_mm` and `body_mass_g` are numeric variables and can be fed directly to the algorithm. On the other hand, `island`, and `sex` are categorical variables and are transformed to **one-hot encoding**. This results in 9 inputs. 
![Alt text](/images/model_input.png "Model Input")

the features used in this prediction are ranked by relative importance below:

![Alt text](/images/feature_importance.png "Model Input")


## Streamlit App
---
A simple streamlit app is built to showcase the model as you see in the following figure:

![Alt text](/images/streamlit_app.png "Model Input")


* You can test the app locally:  
    ```bash
    streamlit run streamlit_app/penguin_streamlit.py
    ```
* Or test the model online using this [link](https://share.streamlit.io/terbouchehacene/penguin_ml/main/streamlit_app/penguin_streamlit.py) 

## Deployment using FastAPI and Docker
---
We deploy the model as an HTTP endpoint using [FastAPI](https://fastapi.tiangolo.com/), and then dockerize the code in a [docker](https://www.docker.com/) image. 

We first define the schemas for the input and the output of the prediction route of the REST API:
* `PenguinDataInput`: the schema of the input of the prediction function of the REST API
* `PenguinModelInput`: the input of the prediction model (the difference in the categorical variables)

```python
class PenguinBase(BaseModel):
    bill_length_mm: float
    bill_depth_mm: float
    flipper_length_mm: float
    body_mass_g: int


class PenguinDataInput(PenguinBase):
    island: Island
    sex: Sex


class PenguinModelInput(PenguinBase):
    island_biscoe: int
    island_dream: int
    island_torgerson: int
    sex_female: int
    sex_male: int
```
* `PenguinClassOutput`: The prediction of the model (categorical variable)
```python
class PenguinClassOutput(BaseModel):
    species: Species
```

We use this docker [image](https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-fastapi/) as the base image (from the developper of the FastAPI package)

* To build the image:
    ```bash
    docker image build -t penguin_app .
    ```
* To run the container locally:
    ```
    docker container run -d -p 8080:80 --name myapp penguin_app
    ```
* To run the app using docker-compose:
    ```
    docker-compose up 
    ```
* To run the app using docker swarm:
    ```
    docker stack deploy -c docker-compose.yml MyApp
    ```


