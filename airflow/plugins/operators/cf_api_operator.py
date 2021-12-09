import json

from datetime import datetime
from airflow.models import DAG, BaseOperator, TaskInstance
from airflow.utils.decorators import apply_defaults
from hooks.cf_api_hook import CfApiHook

class CfApiOperator(BaseOperator):

    @apply_defaults
    def __init__(
        self,
        query,
        conn_id = None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.query = query
        self.conn_id = conn_id

    def execute(self, context):
        hook = CfApiHook(
            query=self.query,
            conn_id=self.conn_id,
        )
        print(json.dumps(hook.run(), indent=4,sort_keys=True))


if __name__ == "__main__":
    with DAG(dag_id="CfTest", start_date=datetime.now()) as dag:
        cfo = CfApiOperator(
            query="contest.list?gym=true",
            task_id="test_run" 
        )
        ti = TaskInstance(task=cfo, execution_date=datetime.now())
        cfo.execute(ti.get_template_context)
