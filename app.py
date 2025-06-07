import streamlit as st
import subprocess
from pathlib import Path

st.title("🔧 Wireguard Mesh Network Automation")
st.caption("Automate managing your wireguard mesh network using wg-meshconf")

WG_DIR = Path("/home/ws/wg")
DATABASE_PATH = WG_DIR / "database.csv"

def run_command(args):
    #cmd = ["wg-meshconf"] + args
    cmd = ["wg-meshconf", "-d", str(DATABASE_PATH)] + args
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

command = st.selectbox("Select Command", ["init", "addpeer", "updatepeer", "delpeer", "showpeers", "genconfig"])

if command == "init":
    if st.button("Initialize Database"):
        st.code(run_command(["init"]))
        #st.code(run_command(["init", "-d", str(DATABASE_PATH)]))

elif command == "addpeer":
    with st.form("Add Peer"):
        name = st.text_input("Peer Name")
        address = st.text_input("Address", placeholder="10.0.0.1/32")
        endpoint = st.text_input("Endpoint (Optional)")
        allowed_ips = st.text_input("Allowed IPs (Optional)")
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

elif command == "delpeer":
    name = st.text_input("Peer Name")
    if st.button("Delete Peer"):
        st.code(run_command(["delpeer", name]))

elif command == "showpeers":
    if st.button("Show Peers"):
        st.code(run_command(["showpeers"]))

elif command == "genconfig":
    with st.form("Generate Config"):
        name = st.text_input("Peer Name (optional for all)")
        output_dir = st.text_input("Output Directory", value=str(WG_DIR / "output"))  # default output inside ./wg/output
        submitted = st.form_submit_button("Generate Config")
        if submitted:
            args = ["genconfig"]
            if name: args.append(name)
            if output_dir: args += ["-o", output_dir]
            st.code(run_command(args))
