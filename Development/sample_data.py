from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

credentials = service_account.Credentials.from_service_account_file(
    'E:\Semester-2\DIVA\Project\Diva-pypi-3aa345f82143.json')

project_id = 'diva-pypi'
client = bigquery.Client(credentials= credentials,project=project_id)



query_job = client.query("""
  SELECT * 
  FROM `the-psf.pypi.downloads20190225` LIMIT 50000""")
results = query_job.result()  # Waits for job to complete.

df = pd.DataFrame(results.to_dataframe())
print(df.shape)
df.to_csv("sample_data.csv", index= False)
print("Successfully saved sample_data.csv")
#print(pd.DataFrame(results.to_dataframe()).sort_values(by = ['cnt'], axis = 1))