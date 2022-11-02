# Repo Skeleton
This repository contains a barebone repository skeleton



<Br>

# ✅&nbsp; Getting Started


## 1. Personalize your project
* Change the name of the ``repo_skeleton`` folder to the name of your project
* modify ``tool.poetry`` section in the ``pyproject.toml`` file

## 2. Set up a local envrironment
```console
pyenv virtualenv 3.9.12 project_name
pyenv activate project_name
pyenv local project_name
```
## 3. Install basic dependencies
```console
poetry install
```
## 4. You are ready to go!



<Br>
<Br>
<Br>


# 🌟 &nbsp; Repository Features

This repo is configured with the following features:

1. The python version is managed by pyenv and the virtual environment by virtualenv
1. CI/CD pipeline for container deploment
    * Configure AWS_ACCESS_KEY_ID and AWS_ACCESS_KEY
1. CI/CD github action pipeline for code formating and testing
    * The code is automatically checked with ``pre-commit`` everytime the code is commited to main
    * To check the code is compliant run ``pre-commit run -a`` before commiting
    * you can write new tests under the ``/test`` folder
1. All python libraries are managed by ``poetry``
    * To add a new package use ``poetry add python_package_name``
    * To add a new package in development use ``poetry add -g dev python_package_name``
1. A pre-configured ``.gitignore, .pre-commit-config.yaml`` and ``pyproject.toml`` file
1. And of course this amazing ``readme.md`` file


# Build & Run docker image
```console
docker build -t dashapp_skeleton:latest .
docker run -p 8094:8094  dashapp_skeleton:latest
```



# To run the app in debug mode
```console
 export ENVIRONMENT=development
```



# ☁ CDK deployment

In a new folder called infra run:
```
cdk init sample-app --language python
```
The `cdk.json` file tells the CDK Toolkit how to execute your app.

To manually create a virtualenv on MacOS and Linux:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```

```
export AWS_ACCESS_REGION=$(aws --profile default configure get aws_region)
```

At this point you can now synthesize the CloudFormation template for this code.
```
cdk synth
cdk bootstraap
cdk deploy
cdk destroy
```

Steps to create a running EC2 instance

ECR - Create a new repository
	- Private 
	- name: manual-private-dashapp-repo

Push Docker image to ECR
    - Follow Push commands for manual-private-dashapp-repo
    - Or use CI/CD pipeline

ECS Create new cluster
    - Chose EC2 Linux + Networking
    - Name: manual-private-cluster
    - Instance type: t2.micro
    - Number of Instances 1
    - VPC: Select default vpc (AWS allocated)
    - Subnet: Select default subnet !!!!!!!!!!!!!!(TODO)
    - Auto assign public IP : Enabled  !!!!!!!!!!
    - Security Group: Select default SG (AWS allocated) !!! Maybe add to the ApplicationLoadBalancedEc2Service
    - Container instance IAM role: ecsInstanceRole !!!!!!!


Create a IAM Role for task definition
    - Select Elastic container service
    - Select Elastic container service task
    - Select AmazonS3FillAccess
    - Select AmazonECSTaskExecutionRolePolicy
    - Name: ManualPrivateDashappRole


Create a Task Definition in ECS > Task Definitions
    - Select EC2 instance
    - Name: manualDashappTaskDefinition
    - TaskRole: Select ManualPrivateDashappRole
    - Task memory (MiB) : 100
    - Task CPU (unit) : 1 vCPU
    - Add Container
        * Container Name: ManualPrivateDashappContainer
        * Image: Copy image URI from repo
        * Host Port 8094 
        * Container port 8094 


Port Map Inbound Rules EC2 > Instances > Security > Security group
    - Edit Inbound Rules
    - Delete Custom TCPs if not relevant
    - Add Custom TCP 8094 Custom 0.0.0.0/0
    - Add Custom TCP 8094 Custom ::/0


Run the Task Definition ECS > Cluster > manual-private-cluster > Tasks 
    - Select EC2
    - Select manualDashappTaskDefinition as task definition

Access Instance in EC2 > Intances > Instance ID 
    - Copy Public IPv4 DNS and add the port at the end
    - ec2-18-194-226-208.eu-central-1.compute.amazonaws.com:8094