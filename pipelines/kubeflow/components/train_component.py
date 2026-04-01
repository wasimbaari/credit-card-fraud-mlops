from kfp import dsl

@dsl.component(
    base_image="fraud-training:latest"
)
def train_model():
    import subprocess
    subprocess.run(["python", "-m", "src.training.train"], check=True)