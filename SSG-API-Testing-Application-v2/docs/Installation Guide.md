# Installation Guide

Welcome to the SSG-WSG Sample Application Installation Guide!

This guide will walk you through the steps to install the SSG-WSG Sample Application on your local environment and
start the application.

## Table of Contents

* [Usage of the Guide](#usage-of-the-guide)
* [Requirements](#requirements)
* [Downloading Code Files](#downloading-code-files)
    * [Method 1: Downloading the Code via Web UI](#method-1-downloading-the-code-via-web-ui)
    * [Method 2: Downloading the Code via `git`](#method-2-downloading-the-code-via-git)
* [Installation](#installation)
    * [Python](#python)
        * [Installation of Python](#installation-of-python)
        * [Python Libraries](#python-libraries)
    * [Docker](#docker)
        * [Installation of Docker](#installation-of-docker)
* [Usage](#usage)
    * [Running the Application in Python](#running-the-application-in-python)
    * [Running the Application in Docker](#running-the-application-in-docker)
        * [Building the Docker Container](#building-the-docker-container)
        * [Running the Docker Container](#running-the-docker-container)
* [Conclusion](#conclusion)

## Usage of the Guide

Some special notation will be used throughout the Developer Guide. Do make sure to familiarise yourself with the
notation below to avoid misunderstandings and confusion regarding the content of the guide!

Text in **green** callout boxes are some tips and tricks that you should be aware of:

> [!TIP]
> This is a tip!

Text in **blue** callout boxes are informational messages that you should take note of:

> [!NOTE]
> This is a note!

Text in **yellow** callout boxes are warnings that you should take note of to ensure that you do not encounter an error:

> [!WARNING]
> This is a warning!

## Requirements

To install the application on your local environment, you would need the following tools:

1. Python `3.12`
2. A terminal (Command Prompt, Terminal, etc.)
3. Docker (if you do not wish to install Python on your machine)
4. `git` (if you wish to obtain the code files directly from the GitHub repository)

## Downloading Code Files

Before installing Python or Docker, you will need to first get a copy of the application source code from the GitHub
repository where the code is hosted on.

There are 2 methods to obtain the files: directly downloading the code via the Web UI or using `git` to clone the
repository where the Sample Code is stored.

### Method 1: Downloading the Code via Web UI

To obtain the code directly from GitHub's UI, follow the steps below:

1. Head over to the [code repository](https://github.com/ssg-wsg/Sample-Codes) where the code is hosted
2. Click on the green `Code` button. You should be able to see a dropdown with 2 tabs, titled `Local` and `Codespaces`
    1. Select `Local` if it is not already selected
    2. You should be able to see the following options:
       ![GitHub Code button](assets/installation-guide/code-button.png | width=200)
3. Click on the `Download ZIP` option. This should trigger a download action that downloads a zipped file
   containing the application source codes.
4. Extract the contents of the zipped file to a directory (folder) of your choice. Make sure to choose a location that
   is convenient for you as you will require it for the following sections.

### Method 2: Downloading the Code via `git`

> [!WARNING]
> This method requires you to have `git` installed in your environment.
>
> If you do not have `git` installed, you can refer
> to [this guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
> to learn more about how to install `git` on your environment.
>
> To verify if your environment has `git` installed, run the following command on a command prompt or terminal:
>
> ```shell
> git --version
> ```
>
> If successful, you should be able to see the version of `git` installed on your environment.

To obtain the code using `git`, follow the steps below:

1. Open a new command prompt or terminal in a location that is convenient for you. You should take note that the
   location
   where this command prompt is opened is where the source code files will be downloaded!
    1. Use the `cd` command to *change directory* to the correct directory (folder) and use the `ls` command to *list*
       the
       files in the directory (folder)
2. Run the following command:
   ```shell
   git clone https://github.com/ssg-wsg/Sample-Codes
   ```
3. The command should clone the repository files into your current working directory. You should be able to see a new
   directory (folder) named `Sample-Codes` in your current working directory.
4. Navigate into the `Sample-Codes` directory (folder) using the `cd` command:
   ```shell
   cd Sample-Codes
   ```
5. You should be able to see the source code files in the directory (folder) that you have navigated into.

## Installation

The application supports 2 methods of installation: Python and Docker.

For Python, you will need to prepare your local environment and install the necessary runtimes and

### Python

Follow this section of the guide if you wish to install the application manually using Python.

If you already have Python `3.12` installed on your system, you can skip to the [installation of the required Python
libraries](#Python-Libraries). If not, you can follow the steps below to install Python `3.12` on your system.

#### Installation of Python

To install Python `3.12` on your system, follow the steps below:

1. Head over to the [Python Releases](https://www.python.org/downloads/release/python-3123/) page
2. Download the correct installation package for your operating system of choice
3. If you are using Windows or MacOS, run the downloaded installation package and follow the installation steps
4. If you are using Linux, refer to [this guide](https://www.geeksforgeeks.org/how-to-install-python-in-ubuntu/)
   on how you can install Python `3.12` on your system

> [!WARNING]
> If you are using Linux, make sure to explicitly specify the Python version when running the commands that require
> the specification of the Python version!

> [!TIP]
> To verify if you have successfully installed Python on your system, open up a command prompt or terminal and run
> the following command
> ```python -V```
> If your installation is successful, you should be able to see Python `3.12.X` printed out on your screen. `X` refers
> to the minor version of Python that is part of the Python `3.12` major release. This number is irrelevant for
> the installation of the SSG-WSG Sample Application.

#### Python Libraries

> [!TIP]
> You are highly recommended to use package managers like `pyenv` or `conda` to manage your Python packages, as it helps
> to
> prevent dependency clashes between different Python projects on your system!
>
> Click on the respective links to learn more about [pyenv](https://github.com/pyenv/pyenv)
> and [conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html)!
>
> Make sure to activate the environment where the required Python libraries are installed before
> following the steps outlined below to avoid installing the libraries in the wrong location!

The application leverages several libraries to run. To install these libraries, follow the steps below:

1. Open up a command prompt or terminal on your environment
2. Navigate to the directory (folder) `SSG-API-Testing-Application-v2/app` where the `requirements.txt` file is located
    1. Use the `cd` command to *change directory* to the correct directory (folder) and use the `ls` command to *list*
       the
       files in the directory (folder)
3. Run the command:
    ```shell
    pip install -r requirements.txt
    ```

> [!NOTE]
> If the command fails to execute, try replacing `pip` with `pip3`! If that also fails, try `python -m pip`!

> [!TIP]
> To verify if you have successfully installed the required libraries, run the following command on a command prompt
> or terminal:
>
> ```shell
> python
> ```
>
> ```python
> import streamlit, pycodestyle, requests, cryptography, streamlit_nested_layout, \
>     apscheduler, certifi, OpenSSL, coverage, email_validator
> ```

### Docker

The application also comes with a Dockerfile that you can use to quickly create Docker containers with
the application running inside it.

#### Installation of Docker

To follow this method of installing the application, you need to have Docker installed in your environment.

If you do not have Docker installed in your environment, head over
the [Docker Engine Installation Guide](https://docs.docker.com/engine/install/)
and follow the instructions in the guide on how to install the Docker Engine in your environment.

The Docker Engine is required to build and run Docker containers in your environment.

## Usage

### Running the Application in Python

> [!WARNING]
> If you are using any package managers like `pyenv` or `conda`, make sure to activate the environment where the
> required Python libraries are installed before running the application!

To run the application in Python, follow the steps below:

1. Open up a command prompt or terminal in the directory (folder) where the above source code for the application is
   downloaded into
2. Navigate to the `app` directory (folder) located within the `SSG-API-Testing-Application-v2` directory (folder). This
   directory (folder) should have a `requirements.txt` file present in it
    1. Use the `cd` command to *change directory* to the correct directory (folder) and use the `ls` command to *list*
       the files in the directory (folder)
3. Run the command:
   ```shell
   streamlit run Home.py
   ```
4. If successful, your browser should open up and the application should be running on `http://localhost:80`

### Running the Application in Docker

Before you can run the application in Docker, you will need to first build the Docker container.

#### Building the Docker Container

To build and run the Docker container with the application running inside it, follow the steps below:

1. Open up a command prompt or terminal in the directory (folder) where the above source code for the application is
   downloaded into
2. Navigate to the `app` directory (folder) located within the `SSG-API-Testing-Application-v2` directory (folder). This
   directory (folder) should have a `Dockerfile` present in it
    1. Use the `cd` command to *change directory* to the correct directory (folder) and use the `ls` command to *list*
       the
       files in the directory (folder)
3. Run the following command to build the Docker container:
    ```shell
    docker build -t app .
    ```
    1. The `docker build` command will build the Docker container using the `Dockerfile` present in the current
       directory
       (folder)
    2. The `-t` flag is used to tag the Docker container with the name `app`
    3. The `.` at the end of the command specifies the current directory (folder) as the build context for the Docker
       container

#### Running the Docker Container

Once your build is successful, follow the steps below to run your container:

1. Run the Docker container using the following command:
    ```shell
    docker run -it -p 80:80 app
    ```
    1. The `docker run` command is used to run the Docker container
    2. The `-it` flag is used to run the Docker container in interactive mode
    3. The `-p` flag is used to map the port `80` on the host machine to the port `80` on the Docker container
    4. The `app` at the end of the command specifies the name of the Docker container to run. This should match the name
       that you have tagged the Docker container within the previous step
2. Open your web browser and navigate to `http://localhost:80` to access the application running inside the Docker
   container

> [!NOTE]
> Refer to the [Docker CLI References](https://docs.docker.com/reference/cli/docker/) for more information about the
> different Docker commands used!

## Conclusion

Congratulations! You have successfully installed and executed the Sample Application on your local environment.

If you wish to learn more on how to set up your AWS account and AWS Organization, refer to the
[AWS Account Setup Guide](AWS%20Account%20Setup%20Guide.md).

If you wish to learn more about how to deploy the application onto AWS, refer to the
[Deployment Guide](Deployment%20Guide.md).

If you wish to learn more about how to set up the application locally and develop it, refer to the
[Developer Guide](Developer%20Guide.md).

If you wish to learn more about how to use the application from a user's perspective, refer to the
[User Guide](User%20Guide.md).
