from kfp import dsl

@dsl.component(
    base_image="fraud-training:latest"
)
def preprocess_data():
    import subprocess
    subprocess.run(["python", "-m", "src.data.preprocess"], check=True)
    subprocess.run(["python", "-m", "src.features.feature_engineering"], check=True)