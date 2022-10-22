# Lambda Skeleton
This repository contains a skeleton for a contenerized lambda CI pipeline. It uses the following technologies

* ``Poetry`` - to manage the packages
* ``Pre-commit`` - to keep the proper format an test the code.
* ``AWS S3`` - Connected to fetch data from the cloud storage service
* ``Github Actions`` - To create CI pipeline to update the code and provide formatting and storage capabilities



# 🔧&nbsp; Configuration
1. Create an AWS user:
    * Assign programmatic access with access key ID
    * Assign the ``AmazonEC2ContainerRegistryFullAccess`` to the user
1. Create a AWS lambda function with the option to update the code via a container
1. Create a repository in AWS ECR
1. ``ECR_REPOSITORY`` is the simple name of the repository created in ECR
1. ``ECR_REGISTRY`` The URL for your default private registry is ``https://aws_account_id.dkr.ecr.region.amazonaws.com.``
1. Set up your ``AWS_ACCESS_KEY_ID`` and ``AWS_ACCESS_KEY`` in github secrets
1. Set up a role ``DEPLOYMENT_ROLE_DEVELOPMENT`` with programatic access for s3, ecs and EC2

You can find a broad guide of how to do it in the following link:
https://blog.devgenius.io/build-a-docker-image-and-publish-it-to-aws-ecr-using-github-actions-step-by-step-2cd2f4e667a7

# ✅&nbsp; Getting Started


## Local envrironment
To set up your local environment run

```console
pyenv virtualenv 3.9.12 project_name
pyenv local project_name
poetry install
```
This should install all necessary dependencies into your 'lambda_skeleton' virtualenv



# 🏃 &nbsp; Running the code and Testing



# 🌟 &nbsp; Repository Features

This repo is configured with the following features: 

1. The python version is managed by pyenv and the virtual environment by virtualenv
1. CI/CD github action pipeline for code formating and testing
    * The code is automatically checked with ``pre-commit`` everytime the code is commited to main
    * To check the code is compliant run ``pre-commit run -a`` before commiting
    * you can write new tests under the ``/test`` folder
1. All python libraries are managed by ``poetry``
    * To add a new package use ``poetry add python_package_name``
    * To add a new package in development use ``poetry add -g dev python_package_name``
1. A pre-configured ``.gitignore, .pre-commit-config.yaml`` and ``pyproject.toml`` file
1. And of course this amazing ``readme.md`` file