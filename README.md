# AeroDrift

AeroDrift is an Agentic Cloud Topology & Remediation Platform that monitors cloud infrastructure, detects issues, analyzes risks, and recommends or automates remediation.

## Key Features

- AWS resource collection
- Cloud topology analysis
- Drift detection
- Remediation planning
- FastAPI backend
- Rich CLI dashboard
- API health monitoring
- AWS resource caching
- Automated API validation and endpoint testing

## Architecture

AWS Infrastructure
↓
Resource Collector
↓
Topology Adapter
↓
Topology / Drift Detection
↓
Remediation Planning
↓
FastAPI Backend
↓
Rich CLI Dashboard

## Technology Stack

Technology| Purpose
Python| Core development
FastAPI| Backend API
AWS / Boto3| Cloud resource collection
NetworkX| Cloud topology graph
Rich| CLI dashboard
Requests| API communication
Jinja2| Web dashboard templates
Pytest| Automated testing

## Project Structure

aerodrift/
├── ingestion/
├── topology/
├── remediation/
├── tests/
├── web/
├── dashboard.py
├── main.py
└── README.md

## Installation

Install Dependencies

pip install -r requirements.txt

Install Testing Dependencies

python -m pip install pytest

## AWS Configuration

Configure AWS credentials using the AWS CLI or another secure AWS credential provider.

The project uses the configured AWS region for resource collection.

«Security: Never commit AWS access keys, secret keys, or other credentials to the repository.»

## Running the API

Start the FastAPI server:

python -m uvicorn main:app --reload

The API will be available locally at:

http://127.0.0.1:8000

## Running the Dashboard

Open a separate terminal and run:

python dashboard.py

The Rich CLI dashboard displays:

- Topology information
- Drift detection results
- Remediation status
- API health
- Data source
- Environment information

## API Endpoints

Endpoint| Purpose
"/"| API welcome message
"/health"| API health status
"/topology"| Cloud topology information
"/drift"| Drift detection results
"/remediation"| Remediation plans
"/dashboard"| Web dashboard

## Testing

Run the automated test suite:

python -m pytest

The project includes tests for:

- API response validation
- FastAPI API endpoints
- Dashboard integration
- Topology data structures
- Drift data structures
- Remediation data structures

## Project Status

AeroDrift currently supports:

- AWS resource collection
- Cloud topology analysis
- Drift detection
- Remediation planning
- API health monitoring
- Resource caching
- Dashboard integration
- Automated API and endpoint testing

The project has been tested through automated validation and FastAPI endpoint tests.
