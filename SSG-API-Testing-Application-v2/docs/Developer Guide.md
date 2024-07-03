# Developer Guide

Welcome to the SSG-WSG Sample Application Developer Guide!

## Table of Contents

1. [Acknowledgements](#Acknowledgements)
2. [Introduction](#Introduction)
   1. [Notation](#Notation)
3. [Getting Started](#Getting-Started)
   1. [Minimum Requirements](#Minimum-Requirements)
   2. [Next Steps](#Next-Steps)
4. [Design](#Design)
   1. [Architecture](#Architecture)
      1. [Pages](#Pages)
      2. [Core](#Core)
      3. [Utils](#Utils)
      4. [Tests](#Tests)
5. [Implementation](#Implementation)
6. [Logging, Housekeeping and CI/CD](#Logging-Housekeeping-and-CICD)
   1. [Logging](#Logging)
   2. [Housekeeping](#Housekeeping)
      1. [`start_scheduler()`](#start_scheduler)
      2. [`_clean_temp()`](#_clean_temp)
      3. [Extending tasks to perform](#Extending-tasks-to-perform)
   3. [CI/CD](#CICD)
7. [Glossary](#Glossary)

## Acknowledgements

Code from the application is reused from multiple sources:

* ChatGPT
  * https://chatgpt.com/share/27060ade-b2e2-4b83-9a5b-238d23e0656a
* nric.biz
  * https://nric.biz/
* Protecto.ai
  * https://www.protecto.ai/blog/personal-dataset-sample-singapore-national-registration-identity-card-number-download-pii-data-examples
* Python Docs
  * https://docs.python.org/3/library/logging.html#module-logging
  * https://docs.python.org/3/howto/logging-cookbook.html
* [samliew.com](samliew.com)
  * https://samliew.com/nric-generator
* StackOverflow
  * https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure
  * https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
  * https://stackoverflow.com/questions/1732438/how-do-i-run-all-python-unit-tests-in-a-directory
  * https://stackoverflow.com/questions/53249304/how-to-list-all-existing-loggers-using-python-logging-module
  * https://stackoverflow.com/questions/15435652/python-does-not-release-filehandles-to-logfile
  * https://stackoverflow.com/questions/45984018/python-unit-test-to-check-if-objects-are-same-at-different-location
  * https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure
  * https://stackoverflow.com/questions/4330812/how-do-i-clear-a-stringio-object
  * https://stackoverflow.com/questions/6793575/estimating-the-size-of-binary-data-encoded-as-a-b64-string-in-python
  * https://stackoverflow.com/questions/19922790/how-to-check-for-python-the-key-associated-with-the-certificate-or-not
* SingStat
  * https://www.singstat.gov.sg/-/media/files/standards_and_classifications/educational_classification/classification-of-lea-eqa-and-fos-ssec-2020.ashx
* Squash.io
  * https://www.squash.io/how-to-delete-a-file-or-folder-in-python/
* Streamlit
  * https://discuss.streamlit.io/t/st-code-on-multiple-lines/50511/8
* SAP
  * https://userapps.support.sap.com/sap/support/knowledge/en/2572734
* uen.gov.sg
  * https://www.uen.gov.sg/ueninternet/faces/pages/admin/aboutUEN.jspx.

This guide's structure is also heavily inspired by https://github.com/AY2324S1-CS2103T-T17-1/tp/blob/master/docs/DeveloperGuide.md.

## Introduction

In this guide, you will learn more about the underlying design and architecture of the application, the features of the
application, and how you can maintain or develop on them.

### Notation

Some special notation will be used througout the Developer Guide. Do make sure to familiarise yourself with the notation
below to avoid misunderstandings and confusions regarding the content of the guide!

Text in **green** callout boxes are some tips and tricks that you should be aware of:

> [!TIP]
> This is a tip!

Text in **blue** callout boxes are informational messages that you should take note of:

> [!NOTE]
> This is a note!

Text in **yellow** callout boxes are warnings that you should take note of to ensure that you do not encounter an error:

> [!WARNING]
> This is a warning!

Text in **red** callout boxes are potential errors which you may encounter:

> [!CAUTION]
> This is a potential error!


## Getting Started

Before you start, make sure that you use a device that supports the minimum requirements needed to run the Sample
Application on your device.

### Minimum Requirements

The Sample Application is developed using Python `3.12` and uses Docker for containerisation.

If you are not sure how to Python `3.12` or Docker, head over to the 
[Installation Guide](Installation%20Guide.md) for more information about the installation process.

### Next Steps

Now that you have installed the requirements for the Sample Application, you can now begin developing new features or 
fixing bugs within the application!

Refer to the [Design](#Design) section for more information about the overall architecture of the application.

Refer to the [Implementation](#Implementation) section for more information about the features of the application,
and how they are implemented in code.

Refer to [Logging, Housekeeping and CI/CD](#Logging-Housekeeping-and-CICD) for more information about the logging,
housekeeping and CI/CD processes of the application, so that you are better able to maintain the application.


## Design

The Sample Application is designed to be a simple monolithic Python application that allows for rapid prototyping 
and UI/UX development, by using a UI/UX framework called Streamlit.

Unlike traditional UI/UX frameworks and languages like React or Flutter, Streamlit blurs the line between the backend
and frontend, by allowing developers to write Python code that generates UI/UX elements and handle the logic behind the
UI/UX elements all in the same file, and often without much abstraction of logic between them.

### Architecture

The below diagram features the overall architecture of the application:

![HighLevelArchitecturalDiagram.png](assets/developer-guide/HighLevelArchitecturalDiagram.png)

The application has 4 main components:

* `pages`: This component contains the Streamlit pages that are rendered when the application is run. Each page is 
           responsible for rendering a set of UI/UX elements and handling the process behind calling a specific set of
           APIs. Pages also contain some logic to handle the rendering of UI/UX elements and the processing
           of data for the backend. This can be considered the "frontend" part of the application.
* `core`: This component contains the core logic of the application. This can be considered the "backend" part of the
          application.
* `utils`: This component contains utility functions that are used across the application.
* `tests`: This component contains the unit tests for the application.

We will explore in greater detail each of the components in the following sections.

#### Pages

#### Core

#### Utils

#### Tests


## Implementation

### API 1


## Logging, Housekeeping and CI/CD

To assist you in logging, removing unused credential files and automatically testing and deploying the Sample Application,
we have put in place some helpful features to help you achieve just that!

### Logging

We have implemented a utility `Logger` class, located under in `logger.py` under the `app.core.system` package.

The `Logger` class uses a global `StreamHandler` and `FileHandler` to print out logs to `stdout` and save the logs to a
file under `app/.log/log.txt`.

> [!NOTE]
> `StreamHandler` is used to print out the log text to `stdout`.
> 
> `FileHandler` is used to save the log text to a designated log file. 

The `Logger` class has 4 main methods to allow you to log messages of different severity:
* `Logger::debug()`: logs a DEBUG level message - use this for debugging the application
* `Logger::info()`: logs an INFO level message - use this for informative messages that you wish to log
* `Logger::warning()`: logs a WARNING level message - use this for exceptional but non-critical events that you wish to note
* `Logger::error()`: logs an ERROR level message - use this for exceptional events that are critical

The `Logger` class also has another utility method: `Logger::close()`, which is used to shut down the `Logger` instance.
You may indicate `close_handler = False` to override the default behaviour of closing the global handlers in the loggers
as well.

### Housekeeping

To help you better maintain the state of the temporary file location used to store your uploaded credentials, we have
implemented a "garbage collector" method in `cleaner.py` under the `app.core.system` package.

The "garbage collection" package used is `apscheduler`, a non-blocking task scheduling library in Python. This library
allows you to create cron (interval) tasks that will be performed at a specified time interval without blocking the 
execution of the base Sample Application.

We chose those to use this package over other packages due to its ease of use, compatability with Streamlit and the
lack of the need to write explicit multithreading/concurrent code to execute cron task.

#### `start_scheduler()`

`start_scheduler()` is the main method used to start the scheduler. The following details the steps taken when the
method is called:

1. Check if the task with job ID equals to `UNIQUE_JOB_ID` is already present in the task scheduling pool
2. If it is not in the pool, create a new task to add to the pool.
   1. Specify the time interval as 7 days
   2. Specify the job ID as `UNIQUE_JOB_ID`
   3. Specify to replace any existing jobs with the same job ID to prevent conflicts over which tasks is the latest task
   4. Start the scheduler
3. If the job ID is in the pool, return immediately and do nothing

> [!TIP]
> Do note that the interval is arbitrarily set, you may wish to use another interval for a stricter housekeeping and
> certificate and private key retention policy.

#### `_clean_temp()`

`_clean_temp()` is the task that the scheduler will execute at a fixed interval.

This (private) method does the following:

1. Iterate through all files in the temporary directory where the certificate and key files are uploaded and saved into
2. If the filename ends with `.pem`, remove it

#### Extending tasks to perform

If you wish to include more cron tasks to perform, feel free to define more methods within this file, and add them into
the scheduler within `start_scheduler()`, defining the interval in which to execute the task.

### CI/CD

Automation of unit testing and deployment is done in part using GitHub Actions.

Refer to the [GitHub Actions CI/CD workflow file](../../.github/workflows/test.yml) for a better understanding of the
process.

Here is a diagram representing the overall flow of processes implemented in the workflow file:

![Activity Diagram](assets/developer-guide/CICDActivityDiagram.png)

The steps of the CI/CD pipeline is as such:

1. Start the pipeline on all major OSes (Windows, MacOS, Linux)
2. Checkout (clone) the repository
3. Install Python `3.12` on the GitHub runner
4. Install the Python dependencies
5. Execute the unit tests
6. Upload the code coverage reports to Codecov (if the `CODECOV_TOKEN` secret is present)


## Glossary

## 