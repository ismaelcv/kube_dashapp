# Repo Skeleton
This repository contains a barebone repository skeleton
The idea is that you can clone and rename this repo and start a new project with all the tools you need


the [repository](https://github.com/source-ag/assignment-data-science) for the assignment is public and Github does not allow the creation of private forks for public repositories.

The correct way of creating a private frok by duplicating the repo is documented [here](https://help.github.com/articles/duplicating-a-repository/).

For this assignment the commands are:

 1. Create a bare clone of the repository.
    (This is temporary and will be removed so just do it wherever.)
    ```bash
    git clone --bare git@github.com:source-ag/assignment-data-science.git
    ```

 2. [Create a new private repository on Github](https://help.github.com/articles/creating-a-new-repository/) and give it a good name, for example `source-assignment-data-science`.

 3. Mirror-push your bare clone to your new `source-assignment-data-science` repository.
    > Replace `<your_username>` with your actual Github username in the url below.

    ```bash
    cd assignment-data-science
    git push --mirror git@github.com:<your_username>/source-assignment-data-science.git
    ```

 4. Remove the temporary local repository you created in step 1.
    ```bash
    cd ..
    rm -rf assignment-data-science
    ```

 5. You can now clone your `source-assignment-data-science` repository on your machine (in my case in the `code` folder).
    ```bash
    git clone git@github.com:<your_username>/source-assignment-data-science.git
    ```


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
