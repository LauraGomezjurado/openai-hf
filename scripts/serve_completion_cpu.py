"""Launch existing frozen public checkpoint on CPU; write this study's runtime record."""
import pathlib,json,os,sys
R=pathlib.Path(__file__).resolve().parents[1];name=sys.argv[1];assert name in ['qwen','qwen3']
p=R/('experiments/behavioral_pilot/gguf_source.json' if name=='qwen' else 'experiments/workflow_obligations/qwen3_source.json');s=json.loads(p.read_text())
model=R/s['gguf_path'] if name=='qwen3' else pathlib.Path.home()/'.cache/huggingface/hub'/('models--'+s['repository'].replace('/','--'))/'snapshots'/s['revision']/s['files'][0]
assert model.exists()
cmd=['llama-server','-m',str(model),'--device','none','-ngl','0','--no-op-offload','--no-kv-offload','--fit','off','-c','6144','-np','1','-t','6','-tb','6','--host','127.0.0.1','--port','18973']
if name=='qwen3':cmd+=['--chat-template-kwargs','{"enable_thinking":false}']
(R/f'results/workflow_completion/{name}_server.json').write_text(json.dumps({'pid':os.getpid(),'command':cmd,'source':s},indent=2)+'\n')
os.execvp(cmd[0],cmd)
