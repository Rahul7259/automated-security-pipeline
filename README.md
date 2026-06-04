# Automated Security Pipeline

![DevSecOps](https://img.shields.io/badge/DevSecOps-Pipeline-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![SonarCloud](https://img.shields.io/badge/SonarCloud-SAST-orange)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-black)
![OWASP](https://img.shields.io/badge/OWASP-Top%2010-red)

A DevSecOps pipeline that integrates SonarCloud via GitHub Actions to automate Static Application Security Testing (SAST), detect OWASP Top 10 vulnerabilities, and enforce role-based access control (RBAC) on deployments — combining application security with identity and access management principles.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Access Control Enforcement](#access-control-enforcement)
- [Vulnerabilities Detected](#vulnerabilities-detected)
- [Pipeline Flow](#pipeline-flow)
- [Setup and Installation](#setup-and-installation)
- [Running Tests Locally](#running-tests-locally)
- [SonarCloud Configuration](#sonarcloud-configuration)
- [Results](#results)

---

## Overview

This project demonstrates a complete DevSecOps pipeline that enforces both **access control** and **secure coding** before code is allowed through. On every push to `main`, the pipeline verifies the deploying user is authorized, enforces role-based deployment policies, runs tests with coverage, and scans the code for security vulnerabilities using SonarCloud's SAST engine.

### Key Features

- Role-based access control (RBAC) on deployments, enforced in Python and PowerShell
- Least-privilege deployment policies per role and environment
- Audit trail logging every access decision
- Automated security scanning on every push and pull request
- OWASP Top 10 vulnerability detection via SonarCloud
- Code coverage reporting with pytest-cov
- Quality gate enforcement before deployment

---

## Project Structure

```
automated-security-pipeline/
├── .github/
│   └── workflows/
│       └── devsecops.yml          # GitHub Actions pipeline
├── app/
│   └── app.py                     # Flask app with intentional vulnerabilities
├── config/
│   └── authorized_users.txt       # Authorized deployers (like an AD security group)
├── docs/
│   └── provisioning_procedures.md # Access provisioning SOP
├── scripts/
│   ├── access_control.py          # Python RBAC enforcement
│   └── access_control.ps1         # PowerShell authorization check
├── tests/
│   ├── conftest.py                # Test database setup fixture
│   └── test_app.py                # Pytest test suite
├── sonar-project.properties       # SonarCloud configuration
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Application language and access control scripts |
| Flask | Web framework |
| PowerShell | Authorized deployer verification |
| pytest + pytest-cov | Testing and coverage |
| GitHub Actions | CI/CD automation |
| SonarCloud | SAST security scanning |
| Git | Version control |

---

## Access Control Enforcement

The pipeline enforces role-based access control using both Python and PowerShell, applying IAM principles directly to the deployment process.

### How It Works

1. Developer pushes code
2. Python script enforces role-based deployment policies (RBAC + least privilege)
3. PowerShell script verifies the deployer is in the authorized users list
4. Every access decision is logged to an audit trail
5. Pipeline proceeds to security scanning only if access checks pass

### Access Roles

| Role | Can Deploy | Environments | Requires Approval |
|------|-----------|--------------|-------------------|
| developers | Yes | development, staging | No |
| senior_developers | Yes | development, staging, production | Yes |
| viewers | No | none | No |

> Note the least-privilege design — developers cannot deploy to production, and production deployments by senior developers require approval (a separation-of-duties control).

### Audit Trail

Every deployment attempt is logged with:
- Timestamp
- User identity
- Role
- Target environment
- Access decision (GRANTED / DENIED)

See `docs/provisioning_procedures.md` for the full provisioning SOP, including joiner and leaver procedures for managing the authorized users list.

---

## Vulnerabilities Detected

The sample Flask app contains intentional OWASP Top 10 vulnerabilities for demonstration:

| Vulnerability | OWASP Category | Location |
|---------------|----------------|----------|
| SQL Injection | A03 - Injection | app.py `/user` endpoint |
| Command Injection | A03 - Injection | app.py `/ping` endpoint |
| XSS (Cross-Site Scripting) | A03 - Injection | app.py `/greet` endpoint |
| Path Traversal | A01 - Broken Access Control | app.py `/read` endpoint |
| Weak Cryptography (MD5) | A02 - Cryptographic Failures | app.py `/hash` endpoint |
| Hardcoded Secret | A02 - Cryptographic Failures | app.py SECRET_KEY |
| Debug Mode in Production | A05 - Security Misconfiguration | app.py `app.run()` |

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
         |---> Access Control (Python)      RBAC + least-privilege check
         |
         |---> Authorized Deployer (PowerShell)  Verify user in allow-list
         |
         |---> Run tests with coverage      generates coverage.xml
         |
         |---> SonarCloud SAST Scan         OWASP Top 10 analysis
         |
         └---> Upload Audit Trail           access decisions logged
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
6. Add the token to GitHub Secrets as `SONAR_TOKEN`

---

## Running Tests Locally

```bash
# Run tests
python -m pytest tests/ -v

# Run tests with coverage report
python -m pytest tests/ --cov=app --cov-report=xml:coverage.xml --cov-report=term-missing
```

The `tests/conftest.py` fixture automatically creates and seeds the `users.db` table before the test session, so the `/user` endpoint returns a valid response during testing.

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

## Results

After the pipeline runs, visit your SonarCloud dashboard to see:

- Security Hotspots - SQL Injection, Command Injection, XSS, etc.
- Code Smells - Bad coding practices
- Bugs - Potential runtime errors
- Code Coverage - Percentage of code covered by tests
- Quality Gate Status - Pass or Fail

The access audit trail is available as a downloadable artifact from each pipeline run under the Actions tab.

---

## Author

Rahul - https://github.com/Rahul7259

---

## License

This project is for educational purposes only. The vulnerabilities in the sample app are intentional and should never be used in production code.
