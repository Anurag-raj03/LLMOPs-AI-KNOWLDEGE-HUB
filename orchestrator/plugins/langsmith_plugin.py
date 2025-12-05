from airflow.plugins_manager import AirflowPlugin
from langsmith import Client

class LangSmithPlugin(AirflowPlugin):
    name = "langsmith_plugin"

def log_to_langsmith(task_id, status, metadata=None):
    client = Client()
    client.log_event(name=f"Airflow-{task_id}", event_type="task", metadata={"status": status, **(metadata or {})})
