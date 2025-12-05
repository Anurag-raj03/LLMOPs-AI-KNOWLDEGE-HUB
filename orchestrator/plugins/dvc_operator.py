import subprocess
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DVCOperator(BaseOperator):
    @apply_defaults
    def __init__(self, stage_name, *args, **kwargs):
        super(DVCOperator, self).__init__(*args, **kwargs)
        self.stage_name = stage_name

    def execute(self, context):
        self.log.info(f"Running DVC stage: {self.stage_name}")
        subprocess.run(["dvc", "repro", self.stage_name], check=True)

def run_dvc_stage(stage_name):
    subprocess.run(["dvc", "repro", stage_name], check=True)
