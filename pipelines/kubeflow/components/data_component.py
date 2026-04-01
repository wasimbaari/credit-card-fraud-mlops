from kfp import dsl

@dsl.component(
    base_image="fraud-training:latest"
)
def data_ingestion():
    import subprocess
    subprocess.run(["python", "-m", "src.data.ingest"], check=True)