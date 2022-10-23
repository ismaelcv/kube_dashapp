# Repo Skeleton
This repository contains a barebone repository skeleton
The idea is that you can clone and rename this repo and start a new project with all the tools you need. The correct way of creating a private fotk by duplicating the repo is documented [here](https://help.github.com/articles/duplicating-a-repository/). Following the next steps:


 1. Create a bare clone of the repository.
    (This is temporary and will be removed so just do it wherever.)
    ```bash
    git clone --bare git@github.com:source-ag/repo_skeleton.git
    ```

 2. Create a new private repository on Github and give it a good name, for example `my-project-repo`.

 3. Mirror-push your bare clone to your new `my-project-repo`.
    Replace your_username with your actual Github username in the url below.

    ```bash
    cd assignment-data-science
    git push --mirror git@github.com:ismaelcv/my-project-repo.git
    ```

 4. Remove the temporary local repository you created in step 1.
    ```bash
    cd ..
    rm -rf assignment-data-science
    ```

 5. You can now clone your repository on your machine.
    ```bash
    git clone git@github.com:<your_username>/my-project-repo.git
    ```
<Br>
<Br>
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
1. CI/CD github action pipeline for code formating and testing
    * The code is automatically checked with ``pre-commit`` everytime the code is commited to main
    * To check the code is compliant run ``pre-commit run -a`` before commiting
    * you can write new tests under the ``/test`` folder
1. All python libraries are managed by ``poetry``
    * To add a new package use ``poetry add python_package_name``
    * To add a new package in development use ``poetry add -g dev python_package_name``
1. A pre-configured ``.gitignore, .pre-commit-config.yaml`` and ``pyproject.toml`` file
1. And of course this amazing ``readme.md`` file
