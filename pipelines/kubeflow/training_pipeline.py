from kfp import dsl
from pipelines.kubeflow.components.data_component import data_ingestion
from pipelines.kubeflow.components.preprocess_component import preprocess_data
from pipelines.kubeflow.components.train_component import train_model


@dsl.pipeline(
    name="fraud-detection-training-pipeline"
)
def pipeline():

    data_task = data_ingestion()

    preprocess_task = preprocess_data()
    preprocess_task.after(data_task)

    train_task = train_model()
    train_task.after(preprocess_task)