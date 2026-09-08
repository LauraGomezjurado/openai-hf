"""Rebuild the completed local research package without network or GPU access."""
from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parents[1]
for script in ['audit_public_data.py','analyze_timing.py','analyze_read_anchored.py','analyze_workstreams.py',
               'prepare_wiki.py','build_evidence_ledger.py','validate_cpu.py']:
    print('Running',script,flush=True)
    subprocess.run([sys.executable,str(root/'scripts'/script)],cwd=root,check=True)
