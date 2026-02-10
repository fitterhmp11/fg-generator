

# README.md

```markdown
# FortiGate Baseline Configuration Generator

An automated Python tool designed to generate standardized FortiOS CLI configuration files from CSV data sources. It uses **Jinja2** templating to ensure consistency across network deployments while allowing for version-specific configurations.

## Features
- **Version-Aware Templating**: Automatically selects templates based on the `fortios_version` specified in the data (e.g., `v7.4`, `v7.6`).
- **Relational Data Modeling**: Maps global system settings and complex interface lists to specific devices using a common `hostname` key.
- **Smart Interface Logic**: Automatically handles physical ports vs. VLAN sub-interfaces, including logical naming for system services like NTP.
- **Data Hardening**: Automatically cleans CSV headers (removes spaces and forces lowercase) to prevent common manual entry errors.
- **Strict Validation**: Utilizes `StrictUndefined` to ensure no configuration is generated with missing or broken variables.

---

## Directory Structure
```text
fg-baseline-generator/
├── fg-generator.py        # Main execution script
├── requirements.txt       # Python library dependencies
├── README.md              # Documentation
├── data/
│   ├── common.csv         # Global settings (Hostname, Passwords, etc.)
│   └── interfaces.csv     # Interface, IP, Role, and VLAN mapping
├── templates/
│   ├── v7.4/              # Config templates for FortiOS 7.4
│   │   ├── base.j2        # Master template
│   │   ├── interfaces.j2  # Interface logic
│   │   ├── routing.j2     # Static routing logic
│   │   └── ...            # Other snippets (trusthosts, etc.)
│   └── v7.6/              # Future-proofed folder for v7.6 templates
└── output/                # Generated .conf files

```

---

## Installation & Setup

### 1. Initialize Virtual Environment

To keep dependencies isolated, create and activate a virtual environment:

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate

```

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

---

## Usage Guide

### 1. Prepare Data

Ensure your CSV files in the `data/` folder use the following standardized headers:

* **common.csv**: `hostname`, `fortios_version`, `timezone`, `admin_password`, `omnisupport_password`
* **interfaces.csv**: `hostname`, `local_name`, `physical_port`, `vlan_id`, `ip_address`, `netmask`, `allow_access`, `role`, `default_gateway`

### 2. Run the Generator

```bash
python3 fg-generator.py

```

### 3. Retrieve Output

Configurations will be saved to the `output/` folder as `<hostname>_baseline.conf`.

---

## Technical Standards

* **Variable Style**: `snake_case` (all lowercase with underscores).
* **Template Engine**: Jinja2 with whitespace control (`{%- ... -%}`) for clean CLI formatting.
* **Data Handling**: Pandas (Python) for robust CSV parsing and header normalization.

```

---
