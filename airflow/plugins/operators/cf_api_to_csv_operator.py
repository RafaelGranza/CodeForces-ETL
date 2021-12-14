import json
import os

import pandas as pd

from datetime import datetime
from airflow.models import DAG, BaseOperator, TaskInstance
from airflow.utils.decorators import apply_defaults
from hooks.cf_api_hook import CfApiHook

CSV_HOME = os.environ["CSV_HOME"]

class CfApiToCsvOperator(BaseOperator):

    @apply_defaults
    def __init__(
        self,
        query,
        csv_filename,
        csv_source_path,    
        field_name = None,
        conn_id = None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.query = query
        self.conn_id = conn_id
        self.field_name = field_name
        self.csv_filename = csv_filename
        self.csv_source_path = csv_source_path

    def execute(self, context):
        self.save_df_as_csv(self.get_df())

    
    def get_df(self):
        hook = CfApiHook(
            query=self.query,
            conn_id=self.conn_id,
        )
        jsn = hook.run()['result'][self.field_name]
        return pd.read_json(json.dumps(jsn))    


    def save_df_as_csv(self, df):
        filepath = f"{CSV_HOME}/{self.csv_source_path}{self.csv_filename}"
        df.to_csv (f"{filepath}.csv", index = False, header=True)
        


if __name__ == "__main__":
    # python3 plugins/operators/cf_api_to_csv_operator.py
    with DAG(dag_id="CfTest", start_date=datetime.now()) as dag:
        cfo = CfApiToCsvOperator(
            query="problemset.problems",
            field_name="problems",
            csv_filename ="jorge",
            csv_source_path="",
            task_id="test_run"
        )
        ti = TaskInstance(task=cfo, execution_date=datetime.now())
        cfo.execute(ti.get_template_context)
