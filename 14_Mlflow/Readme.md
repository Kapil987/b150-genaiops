### MLFLOW On AWS

## MLflow on AWS Setup:

1. Login to AWS console.
2. Create IAM user with AdministratorAccess
3. Export the credentials in your AWS CLI by running "aws configure"
4. Create a s3 bucket
5. Create EC2 machine (Ubuntu) & add Security groups 5000 port

Run the following command on EC2 machine
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install unzip net-tools -y
## Install aws CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

## Then set aws credentials
aws configure

mkdir mlflow_setup
cd mlflow_setup
## Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

uv init
uv venv
source .venv/bin/activate
uv add mlflow dvc dvc_s3 boto3



# Run Mlflow server
# export MLFLOW_HOST=0.0.0.0
# export MLFLOW_PORT=5000
# export MLFLOW_SERVER_ALLOWED_HOSTS="52.207.241.237:5000"
# export MLFLOW_SERVER_CORS_ALLOWED_ORIGINS="http://52.207.241.237:5000"
# export MLFLOW_TRACKING_URI="http://52.207.241.237:5000"
# mlflow server --host $MLFLOW_HOST --port $MLFLOW_PORT

mlflow server \
--host 0.0.0.0 \
--port 5000 \
--backend-store-uri sqlite:///mlflow.db \
--default-artifact-root s3://mlflow-prod-299029453147-us-east-1-an \
--allowed-hosts "34.207.117.242:5000" \
--cors-allowed-origins "http://34.207.117.242:5000"

#open Public IPv4 DNS to the port 5000


#set uri in your local terminal and in your code 
export MLFLOW_TRACKING_URI=YOUR_INSTANCEIP:5000/

## Using tmux for handling disconnections
tmux new -s mlflow_server
mlflow server ...
# Ctrl + B → D (detach)
tmux attach -t mlflow

tmux ls

vi ~/.tmux.conf
set -g history-limit 50000
set -g mouse off
tmux source-file ~/.tmux.conf

## mlflow related commands
mlflow experiments search
for id in $(mlflow experiments search | awk '{print $1}' | tail -n +2); do
  mlflow experiments delete --experiment-id $id
done

pkill -f mlflow
# restart server

git then dvc, then git push dvc push, experiment run, git code modify, dvc data modify , experiment run --> track all of them in UI