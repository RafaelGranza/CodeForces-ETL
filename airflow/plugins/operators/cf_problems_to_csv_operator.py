import json
import pandas as pd

from datetime import datetime
from airflow.models import DAG, BaseOperator, TaskInstance
from airflow.utils.decorators import apply_defaults
from hooks.cf_api_hook import CfApiHook

class CfApiToCsvOperator(BaseOperator):

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
        # jsn = json.loads(hook.run(), indent=4,sort_keys=True)
        jsn = hook.run()['result']['problems']
        df = pd.read_json(json.dumps(jsn))
        print(df)
        # print(df.to_csv())
        # python3 plugins/operators/cf_problems_to_csv_operator.py
        


if __name__ == "__main__":
    with DAG(dag_id="CfTest", start_date=datetime.now()) as dag:
        cfo = CfApiToCsvOperator(
            query="problemset.problems",
            task_id="test_run" 
        )
        ti = TaskInstance(task=cfo, execution_date=datetime.now())
        cfo.execute(ti.get_template_context)
