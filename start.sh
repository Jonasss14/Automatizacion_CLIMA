pip install -r requirements.txt
prefect cloud login --key $prefect cloud login -k pnu_F2AUoIZCHeizaWmuS9oQN0TQIRqCWV0vHkUy --workspace $prefect cloud workspace set --workspace "jonas-luna/default"
prefect worker start --pool "clima" --work-queue "default"