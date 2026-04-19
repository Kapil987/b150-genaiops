## docker and kube on AWS Setup:

1. Login to AWS console.
2. Create IAM user with AdministratorAccess
3. Export the credentials in your AWS CLI by running "aws configure"
4. Create a s3 bucket
5. Create EC2 machine (Ubuntu) & add Security groups 5000 port

Run the following command on EC2 machine
```bash
sudo apt update && sudo apt upgrade -y;
sudo apt install unzip net-tools -y ;
## Install aws CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

## Then set aws credentials
aws configure

## Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
exit bash, then re-enter


## Install docker
https://docs.docker.com/engine/install/ubuntu/
sudo usermod -aG docker $USER
exit bash, then re-enter

## Install kind
https://kind.sigs.k8s.io/docs/user/quick-start/#installation

sudo mv kind /usr/local/bin
# sudo chmod +x /usr/local/bin/kind
## Install kubectl
https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

## Docker commands
docker build -t dockerHubRepoName/ImageName:tagName pathToDockerFile
docker build -t myapp .
docker images
kubectl apply -f deployment.yaml
docker ps -a

## kind commands
kind create cluster --config kind-config.yml
kind load docker-image myapp:latest --name demo1
kind get clusters
kind delete clusters clusterName

## AWS
make sure to open NodePort in security group of you ec2

## Troubleshooting
alias k='kubectl'
k delete -f deploy.yml

kubectl run test --rm -it --image=busybox -- sh
wget -qO- http://flask-service

kind delete clusters demo1

ubuntu@ip-172-31-26-169:~/15_Docker_Kubernetes/app$ kubectl get svc
NAME            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
flask-service   NodePort    10.96.29.170   <none>        80:30007/TCP   2m2s
kubernetes      ClusterIP   10.96.0.1      <none>        443/TCP        33m
ubuntu@ip-172-31-26-169:~/15_Docker_Kubernetes/app$

