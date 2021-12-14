import json
import os

import pandas as pd

from datetime import datetime
from airflow.models import DAG, BaseOperator, TaskInstance
from airflow.utils.decorators import apply_defaults
from hooks.cf_sttm_hook import CfSttmHook

CSV_HOME = os.environ["CSV_HOME"]

class LoadSttmsToCsvOperator(BaseOperator):

    @apply_defaults
    def __init__(
        self,
        csv_source_filename,
        csv_source_path,
        csv_dist_path,
        csv_dist_filename,    
        conn_id = None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.csv_source_filename = csv_source_filename
        self.csv_source_path = csv_source_path
        self.csv_dist_filename = csv_dist_filename
        self.csv_dist_path = csv_dist_path


    def execute(self, context):
        df = self.get_sttmts_df(self.get_df_from_csv())
        self.save_df_as_csv(df)


    def get_df_from_csv(self):
        filepath = f"{CSV_HOME}/{self.csv_source_path}{self.csv_source_filename}"
        data = pd.read_csv(f"{filepath}.csv")
        data = data.where(pd.notnull(data), None)
        return data[:5]


    def get_sttmts_df(self, data):
        sttmts = list()
        for i in range(len(data)):
            query = f"{data['contestId'][i]}/{data['index'][i]}"
            hook = CfSttmHook(
                query=query,
                conn_id=self.conn_id,
            )
            sttmts.append(hook.run())
        data["statment"] = sttmts
        return data


    def save_df_as_csv(self, df):
        filepath = f"{CSV_HOME}/{self.csv_dist_path}{self.csv_dist_filename}"
        df.to_csv (f"{filepath}.csv", index = False, header=True)
        


if __name__ == "__main__":
    # python3 plugins/operators/load_sttms_to_csv__operator.py
    with DAG(dag_id="CfTest", start_date=datetime.now()) as dag:
        cfo = LoadSttmsToCsvOperator(
            csv_source_filename ="jorge",
            csv_source_path="",
            csv_dist_filename ="pronto",
            csv_dist_path="",
            task_id="test_run"
        )
        ti = TaskInstance(task=cfo, execution_date=datetime.now())
        cfo.execute(ti.get_template_context)
