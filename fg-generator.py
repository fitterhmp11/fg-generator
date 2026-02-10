import os
import pandas as pd
from jinja2 import Environment, FileSystemLoader, StrictUndefined

# --- STEP 1: UNIVERSAL PATH SETTINGS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_BASE = os.path.join(SCRIPT_DIR, 'templates')
OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, 'output')
DATA_FOLDER = os.path.join(SCRIPT_DIR, 'data')

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# --- STEP 2: LOAD AND STANDARDIZE DATA ---
try:
    # Load Common Data
    df_common = pd.read_csv(os.path.join(DATA_FOLDER, 'common.csv'), dtype=str).fillna('')
    # Force headers to lowercase and strip hidden spaces
    df_common.columns = df_common.columns.str.lower().str.strip()

    # Load Interface Data
    df_interfaces = pd.read_csv(os.path.join(DATA_FOLDER, 'interfaces.csv'), dtype=str).fillna('')
    df_interfaces.columns = df_interfaces.columns.str.lower().str.strip()
    
    print(f"Successfully loaded data for {len(df_common)} device(s).")
except Exception as e:
    print(f"Error loading CSV files: {e}")
    exit()

# --- STEP 3: GENERATE CONFIGURATIONS ---
for index, firewall_row in df_common.iterrows():
    
    # Using standardized lowercase keys
    current_hostname = firewall_row['hostname']
    os_version = firewall_row['fortios_version']
    
    # Pathing based on version
    version_dir = os.path.join(TEMPLATE_BASE, f'v{os_version}')
    
    # Setup Jinja Environment with StrictUndefined to catch missing variables
    env = Environment(
        loader=FileSystemLoader(version_dir),
        undefined=StrictUndefined
    )
    
    # Filter interfaces for this specific host
    relevant_interfaces = df_interfaces[df_interfaces['hostname'] == current_hostname]
    
    # Build Context
    context = firewall_row.to_dict()
    context['interfaces'] = relevant_interfaces.to_dict(orient='records')

    try:
        # Render
        master_template = env.get_template('base.j2')
        rendered_config = master_template.render(context)

        # Save (Overwrite mode 'w')
        save_path = os.path.join(OUTPUT_FOLDER, f"{current_hostname}_baseline_{os_version}.conf")
        with open(save_path, 'w') as f:
            f.write(rendered_config)
        
        print(f"Done: {current_hostname} (v{os_version})")
        
    except Exception as e:
        print(f"Error for {current_hostname}: {e}")

print("\nGeneration complete. Check the 'output' folder.")