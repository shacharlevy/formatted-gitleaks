# Formatted Gitleaks Docker Image

## Project Description

This project wraps the Gitleaks secret-detection tool in a Python script to enhance its output format for better readability and usability. The Python script processes the raw Gitleaks output, converts it into a structured JSON format using the Pydantic library, and handles errors gracefully by generating structured error files. The project is packaged into a Docker image for ease of use and portability.

---

## Features

- **Enhanced Output Formatting**: Converts raw Gitleaks output into a structured JSON format.
- **Error Handling**: Provides meaningful error messages in JSON format in case of failures.
- **Docker Integration**: Includes both Gitleaks and the Python script in a single Docker image for seamless execution.

---

## Assumptions

- The base image `zricethezav/gitleaks:latest` is available for integration.
- Gitleaks is expected to generate a report file in JSON format.
- Missing fields in the Gitleaks output will be replaced with an empty string in the transformed output.
- The default report path is `/code/output.json` unless specified using the `--report-path` flag.
- Errors such as invalid commands or missing report files are logged in a structured JSON file (or `output.json` if not specified).
- The script assumes a Unix-like environment for Docker and command-line execution.

---

## Requirements

- **Docker**: Installed on the host machine.
- **Access to Git Repository**: To scan for secrets.
- **Python Dependencies**: Installed via `requirements.txt` during the build process.

---

## Instructions to Run the Project

### 1. Build the Docker Image

Run the following command to build the Docker image:

```bash
docker build -t formatted_gitleaks .

### 2. Run the Docker Container

To scan the current working directory with Gitleaks, use the following command:

```bash
docker run --rm -v %cd%:/code formatted_gitleaks gitleaks detect --no-git --report-path /code/output.json /code/

---

##  View the Transformed Output

- After running the container, the transformed JSON output will be printed to the console.e.
- If you need the raw output, it will be saved in output.json or in the specified path in the working directory.

