# AeroDrift

**Agentic Cloud Topology & Remediation Platform**

AeroDrift is a CloudOps and Infrastructure Automation project that continuously collects AWS infrastructure state, builds an in-memory cloud topology graph, detects security drift, and performs controlled automated remediation.

The project combines AWS resource ingestion, graph-based topology analysis, drift detection, AST-based remediation, historical topology tracking, Rich CLI visualization, and PDF incident reporting.

---

## Key Features

- Asynchronous AWS resource collection using `boto3` and `asyncio`
- AWS infrastructure topology using NetworkX
- Public ingress exposure detection (`0.0.0.0/0`)
- Continuous AWS drift monitoring
- Internet-to-private-database path detection
- Critical security drift identification
- Python AST-based remediation generation
- Controlled remediation execution
- Automatic Security Group ingress revocation
- SQLite historical topology snapshots
- Historical graph comparison and diff
- Rich terminal topology visualization
- Rich audit CLI
- Automatic PDF incident reports

---

## Architecture

```text
AWS Cloud
   |
   v
Async Resource Ingestion
   |
   v
Resource Normalization
   |
   v
NetworkX Topology Graph
   |
   +----------------------+
   |                      |
   v                      v
Drift Detection      Path Detection
   |                      |
   +----------+-----------+
              |
              v
       Security Event
              |
              v
       AST Remediation
              |
              v
      Controlled Executor
              |
              v
        AWS Self-Healing
              |
              v
     PDF Incident Report

Topology Graph
      |
      v
SQLite Snapshots
      |
      v
Historical Graph Diff
      |
      v
Rich Audit CLI
```

---

## AWS Resources Collected

AeroDrift currently collects:

- VPCs
- Subnets
- EC2 Instances
- Security Groups
- Route Tables
- Internet Gateways
- Network ACLs

---

## Project Structure

```text
aerodrift/
|
|-- ingestion/
|   |-- aws_client.py
|   |-- resource_collector.py
|   |-- async_collector.py
|   |-- topology_adapter.py
|   |-- exposure_detector.py
|   |-- drift_event.py
|   |-- state_snapshot.py
|   `-- drift_monitor.py
|
|-- topology/
|   |-- node.py
|   |-- edge.py
|   |-- graph_builder.py
|   |-- path_detector.py
|   |-- rich_dashboard.py
|   `-- demo_private_db_path.py
|
|-- remediation/
|   |-- ast_generator.py
|   |-- action_validator.py
|   |-- remediation_engine.py
|   `-- executor.py
|
|-- storage/
|   |-- history_db.py
|   |-- graph_diff.py
|   `-- rich_diff.py
|
|-- reports/
|   `-- incident_report.py
|
|-- aerodrift_cli.py
|-- self_healing.py
|-- requirements.txt
`-- README.md
```

---

## Technologies Used

- Python
- AWS Boto3
- Asyncio
- NetworkX
- Python AST
- Rich
- SQLite
- ReportLab
- AWS CLI
- Git / GitHub

---

## Installation

Clone the repository:

```bash
git clone https://github.com/nandysubham/aerodrift.git
cd aerodrift
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure AWS CLI:

```bash
aws configure
```

Verify AWS authentication:

```bash
aws sts get-caller-identity
```

Use least-privilege AWS credentials. Read-only permissions are sufficient for topology collection and audit features. Remediation requires only the specific write permission needed for the controlled remediation action.

---

## Run AeroDrift Audit CLI

```bash
python aerodrift_cli.py
```

The CLI:

1. Collects current AWS resources
2. Normalizes AWS data
3. Builds the NetworkX topology
4. Displays topology using Rich
5. Saves a SQLite topology snapshot
6. Compares the latest topology with the previous snapshot
7. Displays an audit summary

---

## Run Security Path Demo

The repository contains a safe simulated topology for demonstrating Internet-to-private-database path detection.

```bash
python -m topology.demo_private_db_path
```

Example path:

```text
0.0.0.0/0
    |
    v
Security Group
    |
    v
Private Database
```

AeroDrift detects this path as a **CRITICAL** security drift.

This demo is simulated and does not modify AWS resources.

---

## Drift Detection

AeroDrift continuously compares AWS state snapshots.

Example security drift:

```text
Security Group:
0.0.0.0/0 -> TCP Port 22
```

The system creates a critical `PUBLIC_INGRESS` drift event when unauthorized public ingress is detected.

---

## Automated Remediation

For supported Security Group drift events, AeroDrift:

```text
Detect Drift
    |
Validate Event
    |
Generate Python AST
    |
Compile AST
    |
Controlled exec()
    |
boto3 revoke_security_group_ingress()
    |
Generate Incident PDF
```

The remediation engine generates the exact AWS API operation programmatically using Python AST.

---

## Historical Topology

AeroDrift stores topology snapshots in SQLite.

It can identify:

- Added nodes
- Removed nodes
- Modified nodes
- Added relationships
- Removed relationships
- No-change states

Generated SQLite database files are excluded from Git.

---

## PDF Incident Reports

After successful remediation, AeroDrift can automatically generate a PDF incident report containing:

- Event type
- Resource type
- Resource ID
- Severity
- CIDR
- Protocol
- Port information
- Remediation status
- Remediation action
- Report timestamp

Generated incident PDF files are excluded from Git.

---

## Safety

AeroDrift follows these safety principles:

- Do not use root AWS credentials.
- Use least-privilege IAM permissions.
- Use read-only access for normal monitoring.
- Validate drift events before remediation.
- Execute only generated and validated remediation AST.
- Never test destructive operations on production resources.
- Use dedicated test resources for remediation testing.

---

## Demo Flow

For a project demonstration:

### 1. Run AWS topology audit

```bash
python aerodrift_cli.py
```

### 2. Run it again

```bash
python aerodrift_cli.py
```

The historical diff should show `NO CHANGE` when AWS topology remains unchanged.

### 3. Run security path detection demo

```bash
python -m topology.demo_private_db_path
```

The CLI displays the simulated Internet-to-private-database path as `CRITICAL`.

### 4. Explain self-healing flow

```text
AWS Drift
   ->
Public Ingress Detection
   ->
Drift Event
   ->
AST Remediation
   ->
Controlled Execution
   ->
Security Group Rule Revoked
   ->
PDF Incident Report
```

---

## Current Scope

AeroDrift currently focuses on AWS infrastructure and Security Group public-ingress remediation.

The architecture can be extended in the future for:

- Additional AWS resources
- Additional drift policies
- GCP/Azure support
- More remediation actions
- Advanced topology risk analysis
- Persistent audit and compliance reporting

---

## Project Goal

The goal of AeroDrift is to reduce manual CloudOps remediation by combining real-time cloud state collection, graph-based security analysis, controlled automated remediation, and auditable incident reporting.

## Final AeroDrift Features

AeroDrift currently provides the following features:

- Asynchronous AWS resource collection using `boto3` and `asyncio`
- Collection of VPCs, Subnets, EC2 Instances, Security Groups, Route Tables, Internet Gateways, Network ACLs, and RDS Databases
- AWS resource normalization for topology processing
- Directed cloud topology graph using NetworkX
- VPC → Subnet relationships
- Subnet → EC2 relationships
- EC2 → Security Group relationships
- Security Group → Database relationships
- Detection of public IPv4 ingress (`0.0.0.0/0`)
- Detection of Internet → exposed Security Group → private Database paths
- Rich terminal topology visualization
- Red highlighting of detected drift
- Standard CRITICAL drift event generation
- Continuous AWS drift monitoring
- AST-based generation of `revoke_security_group_ingress()` remediation
- Validation of remediation actions before execution
- Controlled execution of generated remediation code
- Optional automatic remediation using the `--remediate` flag
- SQLite historical topology snapshots
- Historical graph change detection
- Rich historical topology diff visualization
- Persistent remediation success/failure history
- Rich remediation history table
- Automatic PDF incident report generation
- Audit-only mode that performs no AWS modifications

## Running the Final CLI

Run AeroDrift in safe audit-only mode:

```powershell
python aerodrift_cli.py