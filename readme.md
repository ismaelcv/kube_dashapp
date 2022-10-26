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
