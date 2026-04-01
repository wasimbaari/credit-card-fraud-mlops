import os
from pathlib import Path

def create_repo_structure():
    # Define the directory structure
    folders = [
        "configs",
        "data/raw",
        "data/processed",
        "data/external",
        ".dvc",
        "src/data",
        "src/features",
        "src/training",
        "src/inference",
        "src/monitoring",
        "src/utils",
        "notebooks",
        "models",
        "infra/terraform/vpc",
        "infra/terraform/eks",
        "infra/terraform/s3",
        "infra/terraform/ecr",
        "infra/terraform/iam",
        "infra/kubernetes/namespaces",
        "infra/kubernetes/mlflow",
        "infra/kubernetes/kubeflow",
        "infra/kubernetes/kserve",
        "infra/kubernetes/monitoring",
        "infra/kubernetes/logging",
        "infra/kubernetes/argocd",
        "pipelines/kubeflow/components",
        "docker",
        "deployment/kserve",
        "deployment/helm/charts",
        "deployment/manifests",
        "monitoring/evidently/dashboards",
        "monitoring/prometheus",
        "monitoring/grafana",
        "monitoring/alerts",
        "tests/unit",
        "tests/integration",
        "tests/data",
        ".github/workflows",
        "scripts"
    ]

    # Define the files to be created
    files = [
        ".env",
        "pyproject.toml",
        "requirements.txt",
        "Makefile",
        "configs/base.yaml",
        "configs/dev.yaml",
        "configs/prod.yaml",
        "configs/model_config.yaml",
        "configs/data_config.yaml",
        "dvc.yaml",
        "dvc.lock",
        ".dvc/config",
        "src/data/ingest.py",
        "src/data/validate.py",
        "src/data/preprocess.py",
        "src/data/schema.yaml",
        "src/features/feature_engineering.py",
        "src/features/feature_store.py",
        "src/training/train.py",
        "src/training/evaluate.py",
        "src/training/hyperparameter_tuning.py",
        "src/training/pipeline.py",
        "src/inference/predictor.py",
        "src/inference/model_loader.py",
        "src/inference/schemas.py",
        "src/monitoring/data_drift.py",
        "src/monitoring/model_monitor.py",
        "src/monitoring/alerting.py",
        "src/utils/logger.py",
        "src/utils/config_loader.py",
        "src/utils/common.py",
        "notebooks/eda.ipynb",
        "notebooks/experimentation.ipynb",
        "infra/terraform/main.tf",
        "infra/terraform/variables.tf",
        "infra/terraform/outputs.tf",
        "infra/kubernetes/namespaces/mlflow.yaml",
        "infra/kubernetes/namespaces/kubeflow.yaml",
        "infra/kubernetes/namespaces/monitoring.yaml",
        "infra/kubernetes/mlflow/deployment.yaml",
        "infra/kubernetes/mlflow/service.yaml",
        "infra/kubernetes/mlflow/ingress.yaml",
        "infra/kubernetes/kubeflow/pipelines.yaml",
        "infra/kubernetes/kubeflow/katib.yaml",
        "infra/kubernetes/kserve/inference-service.yaml",
        "infra/kubernetes/kserve/custom-predictor.yaml",
        "infra/kubernetes/monitoring/prometheus.yaml",
        "infra/kubernetes/monitoring/grafana.yaml",
        "infra/kubernetes/monitoring/alertmanager.yaml",
        "infra/kubernetes/logging/openobserve.yaml",
        "infra/kubernetes/argocd/application.yaml",
        "infra/kubernetes/argocd/project.yaml",
        "pipelines/kubeflow/training_pipeline.py",
        "pipelines/kubeflow/components/data_component.py",
        "pipelines/kubeflow/components/preprocess_component.py",
        "pipelines/kubeflow/components/train_component.py",
        "pipelines/kubeflow/components/evaluate_component.py",
        "pipelines/kubeflow/components/register_component.py",
        "pipelines/kubeflow/compiled_pipeline.yaml",
        "docker/training.Dockerfile",
        "docker/inference.Dockerfile",
        "docker/base.Dockerfile",
        "deployment/kserve/deploy.yaml",
        "monitoring/evidently/drift_report.py",
        ".github/workflows/ci.yaml",
        ".github/workflows/cd.yaml",
        ".github/workflows/retraining.yaml",
        "scripts/setup.sh",
        "scripts/deploy.sh",
        "scripts/train.sh",
        "scripts/monitor.sh"
    ]

    print("🚀 Starting repository generation...")

    # Create directories
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        # Create an empty .gitkeep to ensure folders are tracked by git
        Path(os.path.join(folder, ".gitkeep")).touch()

    # Create files
    for file_path in files:
        Path(file_path).touch()
    
    print("✅ Structure created successfully!")

if __name__ == "__main__":
    create_repo_structure()