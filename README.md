# Automated Security Pipeline

![DevSecOps](https://img.shields.io/badge/DevSecOps-Pipeline-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![SonarCloud](https://img.shields.io/badge/SonarCloud-SAST-orange)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-black)
![OWASP](https://img.shields.io/badge/OWASP-Top%2010-red)

A DevSecOps pipeline that integrates SonarCloud via GitHub Actions to automate Static Application Security Testing (SAST), identifying OWASP Top 10 vulnerabilities and enforcing secure coding gates prior to deployment.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Vulnerabilities Detected](#vulnerabilities-detected)
- [Pipeline Flow](#pipeline-flow)
- [Setup and Installation](#setup-and-installation)
- [Running Tests Locally](#running-tests-locally)
- [SonarCloud Configuration](#sonarcloud-configuration)
- [GitHub Actions Workflow](#github-actions-workflow)
- [Results](#results)

---

## Overview

This project demonstrates a complete DevSecOps pipeline that automatically scans code for security vulnerabilities on every push to the `main` branch. By integrating SonarCloud's SAST capabilities into GitHub Actions, security issues are caught before they reach production.

### Key Features

- Automated security scanning on every push and pull request
- OWASP Top 10 vulnerability detection
- Code coverage reporting with pytest-cov
- Quality gate enforcement before deployment
- Zero manual intervention required

---

## Project Structure

```
automated-security-pipeline/
├── .github/
│   └── workflows/
│       └── devsecops.yml        # GitHub Actions pipeline
├── app/
│   └── app.py                   # Flask app with intentional vulnerabilities
├── tests/
│   └── test_app.py              # Pytest test suite
├── sonar-project.properties     # SonarCloud configuration
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Application language |
| Flask | Web framework |
| pytest + pytest-cov | Testing and coverage |
| GitHub Actions | CI/CD automation |
| SonarCloud | SAST security scanning |
| Git | Version control |

---

## Vulnerabilities Detected

The sample Flask app contains intentional OWASP Top 10 vulnerabilities for demonstration:

| Vulnerability | OWASP Category | Location |
|---------------|----------------|----------|
| SQL Injection | A03 - Injection | app.py /user endpoint |
| Command Injection | A03 - Injection | app.py /ping endpoint |
| XSS (Cross-Site Scripting) | A03 - Injection | app.py /greet endpoint |
| Path Traversal | A01 - Broken Access Control | app.py /read endpoint |
| Weak Cryptography (MD5) | A02 - Cryptographic Failures | app.py /hash endpoint |
| Hardcoded Secret | A02 - Cryptographic Failures | app.py SECRET_KEY |
| Debug Mode in Production | A05 - Security Misconfiguration | app.py app.run() |

> NOTE: These vulnerabilities are intentional for educational purposes. Never use this code in production.

---

## Pipeline Flow

```
Developer pushes code
        |
        v
+-------------------+
|  GitHub Actions   |  Triggers automatically on push/PR
+--------+----------+
         |
         |---> Checkout repository
         |
         |---> Set up Python 3.11
         |
         |---> Install dependencies
         |
         |---> Run tests with coverage
         |       generates coverage.xml
         |
         |---> SonarCloud SAST Scan
         |       Analyzes Python code
         |       Checks OWASP Top 10
         |       Uploads results to SonarCloud
         |
         └---> Quality Gate Check
                 PASS --> Deployment allowed
                 FAIL --> Deployment blocked
```

---

## Setup and Installation

### Prerequisites

- Python 3.11+
- Git
- GitHub account
- SonarCloud account (free at sonarcloud.io)

### Step 1 - Clone the Repository

```bash
git clone https://github.com/Rahul7259/automated-security-pipeline.git
cd automated-security-pipeline
```

### Step 2 - Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 - Set Up SonarCloud

1. Log in to sonarcloud.io with your GitHub account
2. Create a new project and select your GitHub repo
3. Choose GitHub Actions as the analysis method
4. Disable Automatic Analysis (Administration > Analysis Method)
5. Generate a token (My Account > Security > Generate Token)
6. Add the token to GitHub Secrets as SONAR_TOKEN

---

## Running Tests Locally

```bash
# Run tests
python -m pytest tests/ -v

# Run tests with coverage report
python -m pytest tests/ --cov=app --cov-report=xml:coverage.xml --cov-report=term-missing
```

---

## SonarCloud Configuration

The `sonar-project.properties` file configures how SonarCloud scans the project:

```properties
sonar.projectKey=Rahul7259_automated-security-pipeline
sonar.organization=rahul7259
sonar.projectName=Automated Security Pipeline
sonar.projectVersion=1.0
sonar.sources=app
sonar.tests=tests
sonar.python.version=3.11
sonar.python.coverage.reportPaths=coverage.xml
sonar.coverage.exclusions=tests/**
```

---

## GitHub Actions Workflow

The pipeline is defined in `.github/workflows/devsecops.yml` and triggers on:
- Every push to the main branch
- Every pull request to the main branch

### Workflow Steps

```
1. Checkout repository      - Full git history for blame data
2. Set up Python 3.11       - Configure Python environment
3. Install dependencies     - Flask, pytest, pytest-cov
4. Run tests with coverage  - Generates coverage.xml for SonarCloud
5. SonarCloud Scan          - SAST analysis and OWASP Top 10 check
6. Quality Gate Check       - Enforce secure coding standards
```

---

## Results

After the pipeline runs, visit your SonarCloud dashboard to see:

- Security Hotspots - SQL Injection, Command Injection, XSS, etc.
- Code Smells - Bad coding practices
- Bugs - Potential runtime errors
- Code Coverage - Percentage of code covered by tests
- Quality Gate Status - Pass or Fail

---

## Author

Rahul - https://github.com/Rahul7259

---

## License

This project is for educational purposes only. The vulnerabilities in the sample app are intentional and should never be used in production code.