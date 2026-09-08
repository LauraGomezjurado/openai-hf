"""Launch the pilot GGUF server with all GPU offloading explicitly disabled."""
import json
import os
from pathlib import Path

root=Path(__file__).resolve().parents[1]
source=json.loads((root/'experiments/behavioral_pilot/gguf_source.json').read_text())
model=Path.home()/'.cache/huggingface/hub'/('models--'+source['repository'].replace('/','--'))/'snapshots'/source['revision']/source['files'][0]
assert model.exists(), 'Download must finish first'
command=['llama-server','-m',str(model),'--device','none','-ngl','0',
         '--no-op-offload','--no-kv-offload','--fit','off','-c','2048','-np','1',
         '-t','6','-tb','6','--host','127.0.0.1','--port','18973']
out=root/'results/behavioral_pilot/v3-7b';out.mkdir(parents=True,exist_ok=True)
(out/'server_pid.txt').write_text(str(os.getpid())+'\n')
(out/'server_command.json').write_text(json.dumps(command,indent=2)+'\n')
os.execvp(command[0],command)
