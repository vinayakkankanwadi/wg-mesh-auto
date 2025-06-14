import streamlit as st
import subprocess
from pathlib import Path
import pandas as pd
from datetime import datetime
import os

# -------------------------------
# Constants
# -------------------------------
WG_DIR = Path("/home/ws/wg")
DATABASE_PATH = WG_DIR / "database.csv"
OUTPUT_DIR = WG_DIR / "output"

# -------------------------------
# Helper Functions
# -------------------------------
def run_command(args):
    cmd = ["wg-meshconf", "-d", str(DATABASE_PATH)] + args
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

def load_database():
    if DATABASE_PATH.exists():
        try:
            return pd.read_csv(DATABASE_PATH)
        except Exception as e:
            st.error(f"Error reading database: {e}")
    return pd.DataFrame(columns=["name", "address", "endpoint", "allowedips", "listenport"])

def list_config_files():
    if OUTPUT_DIR.exists():
        files = sorted(OUTPUT_DIR.glob("*.conf"))
        data = []
        for f in files:
            stat = f.stat()
            data.append({
                "Filename": f.name,
                "Size (KB)": round(stat.st_size / 1024, 2),
                "Last Modified": datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
        return pd.DataFrame(data)
    return pd.DataFrame(columns=["Filename", "Size (KB)", "Last Modified"])

# -------------------------------
# Title
# -------------------------------
st.title("🔧 WireGuard Mesh Network Automation")
st.caption("Automate managing your WireGuard mesh network using wg-meshconf")

# -------------------------------
# PEERS Table
# -------------------------------
st.subheader("📄 PEERS")
df = load_database()
st.dataframe(df, use_container_width=True)

# -------------------------------
# Config Files Table
# -------------------------------
st.subheader("📁 Generated Config Files")
config_df = list_config_files()
st.dataframe(config_df, use_container_width=True)

# -------------------------------
# Commands Section
# -------------------------------
st.markdown("---")
st.subheader("🛠️ WireGuard Commands")

command = st.selectbox("Select Command", ["init", "addpeer", "updatepeer", "delpeer", "showpeers", "genconfig"])

if command == "init":
    if st.button("Initialize Database"):
        output = run_command(["init"])
        st.code(output)
        st.rerun()

elif command == "addpeer":
    with st.form("Add Peer"):
        name = st.text_input("Peer Name", value="PEER101")
        address = st.text_input("Address", value="10.0.0.1/32")
        endpoint = st.text_input("Endpoint (Optional)", value="20.0.0.1")
        allowed_ips = st.text_input("Allowed IPs (Optional)", value="30.0.1.0/24")
        private_key = st.text_input("Private Key (Optional)")
        listen_port = st.text_input("Listen Port", placeholder="51820")
        submitted = st.form_submit_button("Add Peer")
        if submitted:
            args = ["addpeer", name, "--address", address]
            if endpoint: args += ["--endpoint", endpoint]
            if allowed_ips: args += ["--allowedips", allowed_ips]
            if private_key: args += ["--privatekey", private_key]
            if listen_port: args += ["--listenport", listen_port]
            st.code(run_command(args))
            st.rerun()

elif command == "updatepeer":
    with st.form("Update Peer"):
        name = st.text_input("Peer Name")
        address = st.text_input("Address (Optional)")
        endpoint = st.text_input("Endpoint (Optional)")
        allowed_ips = st.text_input("Allowed IPs (Optional)")
        private_key = st.text_input("Private Key (Optional)")
        listen_port = st.text_input("Listen Port (Optional)")
        submitted = st.form_submit_button("Update Peer")
        if submitted:
            args = ["updatepeer", name]
            if address: args += ["--address", address]
            if endpoint: args += ["--endpoint", endpoint]
            if allowed_ips: args += ["--allowedips", allowed_ips]
            if private_key: args += ["--privatekey", private_key]
            if listen_port: args += ["--listenport", listen_port]
            st.code(run_command(args))
            st.rerun()

elif command == "delpeer":
    name = st.text_input("Peer Name")
    if st.button("Delete Peer"):
        st.code(run_command(["delpeer", name]))
        st.rerun()

elif command == "showpeers":
    if st.button("Show Peers"):
        st.code(run_command(["showpeers"]))

elif command == "genconfig":
    with st.form("Generate Config"):
        name = st.text_input("Peer Name (optional for all)")
        output_dir = st.text_input("Output Directory", value=str(OUTPUT_DIR))
        submitted = st.form_submit_button("Generate Config")
        if submitted:
            args = ["genconfig"]
            if name: args.append(name)
            if output_dir: args += ["-o", output_dir]
            st.code(run_command(args))
            st.rerun()

# -------------------------------
# Danger Zone
# -------------------------------
st.markdown("---")
st.subheader("⚠️ Danger Zone")

if st.button("🧹 Clear All Files"):
    try:
        if DATABASE_PATH.exists():
            DATABASE_PATH.unlink()
        if OUTPUT_DIR.exists():
            for file in OUTPUT_DIR.glob("*.conf"):
                file.unlink()
        st.success("All files cleared successfully.")
        st.rerun()
    except Exception as e:
        st.error(f"Error clearing files: {e}")

