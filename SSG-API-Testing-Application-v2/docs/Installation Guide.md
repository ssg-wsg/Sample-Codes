# Installation Guide

Welcome to the SSG-WSG Sample Application Installation Guide!

This guide will walk you through the steps to install the SSG-WSG Sample Application on your local environment and
start the application.

## Table of Contents

- [Requirements](#Requirements)
- [Downloading Code Files](#Downloading-Code-Files)
    - [Method 1: Downloading the Code via Web UI](#Method-1-Downloading-the-Code-via-Web-UI)
    - [Method 2: Downloading the Code via `git`](#Method-2-Downloading-the-Code-via-git)
- [Installation](#Installation)
    - [Python](#Python)
        - [Installation of Python](#Installation-of-Python)
        - [Python Libraries](#Python-Libraries)
    - [Docker](#Docker)
        - [Installation of Docker](#Installation-of-Docker)
- [Usage](#Usage)
    - [Running the Application in Python](#Running-the-Application-in-Python)
    - [Running the Application in Docker](#Running-the-Application-in-Docker)
        - [Building the Docker Container](#Building-the-Docker-Container)
        - [Running the Docker Container](#Running-the-Docker-Container)

## Requirements

To install the application on your local environment, you would need the following tools:

1. Python `3.12`
2. A terminal (Command Prompt, Terminal, etc.)
3. Docker (if you do not wish to install Python on your machine)
4. `git` (if you wish to obtain the code files directly from the GitHub repository)

## Downloading Code Files

Before installing Python or Docker, you will need to first get a copy of the application source code from the GitHub
repository where the code is hosted on.

There are 2 methods to obtain the files: directly downloading the code via the Web UI, or using `git` to clone the
repository where the Sample Code is stored.

### Method 1: Downloading the Code via Web UI

To obtain the code directly off of GitHub's UI, follow the steps below:

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
> to [this guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git))
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
   where this command prompt is opened is where the source code files will be downloaded into!
    1. Use the `cd` command to *change directory* to the correct directory (folder) and use `ls` command to *list* the
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
> If you are using Linux, make sure explicitly specify the Python version when running the commands that require
> the specification of Python version!

> [!TIP]
> To verify if you have successfully installed Python on your system, open up a command prompt or terminal and run
> the following command
> ```python -V```
> If your installation is successful, you should be able to see Python `3.12.X` printed out on your screen. `X` refers
> to the minor version of Python that is part of the Python `3.12` major release. This number is irrelevant for
> the installation of the SSG-WSG Sample Application.

#### Python Libraries

> [!TIP]
> You are highly recommended to use package managers like pyenv or conda to manage your Python packages, as it helps to
> prevent dependency clashes between different Python projects on your system!
>
> Click on the respective links to learn more about [pyenv](https://github.com/pyenv/pyenv)
> and [conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html)!
>
> Make sure to activate the environment where the required Python libraries are installed before
> following the steps outlined below to avoid installing the libraries in the wrong location!

The application leverages on several libraries to run. To install these libraries, follow the steps below:

1. Open up a command prompt or terminal on your environment
2. Navigate to the directory (folder) `SSG-API-Testing-Application-v2/app` where the `requirements.txt` file is located
    1. Use the `cd` command to *change directory* to the correct directory (folder) and use `ls` command to *list* the
       files in the directory (folder)
3. Run the command:
    ```shell
    pip install -r requirements.txt
    ```

> [!NOTE]
> If the command fails to execute, try replacing `pip` with `pip3`!

> [!TIP]
> To verify if you have successfully installed the required libraries, run the following command on a command prompt
> or terminal:
>
> ```shell
> python
> ```
>
> ```python
> import streamlit, pycodestyle, requests, cryptography, streamlit_nested_layout, requests_oauthlib, \
>     apscheduler, certifi, OpenSSL, coverage, email_validator
> ```

### Docker

The application also comes with a Dockerfile that you can use to quickly create Docker containers with
the application running inside it.

#### Installation of Docker

To follow this method of installing the application, you need to have Docker installed in your environment.

If you do not have Docker installed in your environment, head over
the [Docker Engine Installation Guide](https://docs.docker.com/engine/install/)
and follow the instructions in the guide on how to install the Docker Engine on your environment.

The Docker Engine is required to build and run Docker containers on your environment.

## Usage

### Running the Application in Python

> [!WARNING]
> If you are using any package managers like pyenv or conda, make sure to activate the environment where the
> required Python libraries are installed before running the application!

To run the application in Python, follow the steps below:

1. Open up a command prompt or terminal in the directory (folder) where the above source code for the application is
   downloaded into
2. Navigate to the `app` directory (folder) located within the `SSG-API-Testing-Application-v2` directory (folder). This
   directory (folder) should have a `requirements.txt` file present in it
    1. Use the `cd` command to *change directory* to the correct directory (folder) and use `ls` command to *list* the
       files in the directory (folder)
3. Run the command:
   ```shell
   streamlit run Home.py
   ```
4. If successful, your browser should open up and the application should be running on `http://localhost:8502`

### Running the Application in Docker

Before you can run the application in Docker, you will need to first build the Docker container.

#### Building the Docker Container

To build and run the Docker container with the application running inside it, follow the steps below:

1. Open up a command prompt or terminal in the directory (folder) where the above source code for the application is
   downloaded into
2. Navigate to the `app` directory (folder) located within the `SSG-API-Testing-Application-v2` directory (folder). This
   directory (folder) should have a `Dockerfile` present in it
    1. Use the `cd` command to *change directory* to the correct directory (folder) and use `ls` command to *list* the
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
    docker run -it -p 8502:8502 app
    ```
    1. The `docker run` command is used to run the Docker container
    2. The `-it` flag is used to run the Docker container in interactive mode
    3. The `-p` flag is used to map the port `8502` on the host machine to the port `8502` on the Docker container
    4. The `app` at the end of the command specifies the name of the Docker container to run. This should match the name
       that you have tagged the Docker container with in the previous step
2. Open your web browser and navigate to `http://localhost:8502` to access the application running inside the Docker
   container

> [!NOTE]
> Refer to the [Docker CLI References](https://docs.docker.com/reference/cli/docker/) for more information about the
> different Docker commands used!
