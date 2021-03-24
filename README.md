# data_lake_testing_pipeline
Testing a data lake

**Installation**
Create a dynamodb table 'datalake-test-config'. Load the src/datalake-test-config.csv. (Add your tests in this csv)
Install the step functions src/\*.json, and the lambda functions src/\*.py

**Execute**
The src/DataLakeTestController.json is the controlling step function. Trigger this via any method such as:
- You can simply plug this in to your serverless data lake framework if you like, or
- schedule it to execute in cloudwatch, or
- trigger it via AWS Config, or
- Add it as a stage in your code pipeline.
