import pathlib,json,os,sys
R=pathlib.Path(__file__).resolve().parents[1];name=sys.argv[1]
p=R/('experiments/behavioral_pilot/gguf_source.json' if name=='qwen' else ('experiments/workflow_obligations/qwen3_source.json' if name=='qwen3' else 'experiments/workflow_obligations/phi_source.json'));s=json.loads(p.read_text());model=(R/s['gguf_path']) if name in ['phi','qwen3'] else pathlib.Path.home()/'.cache/huggingface/hub'/('models--'+s['repository'].replace('/','--'))/'snapshots'/s['revision']/s['files'][0];assert model.exists()
out=R/'results/workflow_obligations'/name;out.mkdir(parents=True,exist_ok=True)
cmd=['llama-server','-m',str(model),'--device','none','-ngl','0','--no-op-offload','--no-kv-offload','--fit','off','-c','6144','-np','1','-t','6','-tb','6','--host','127.0.0.1','--port','18973']
if name=='qwen3':cmd+=['--chat-template-kwargs','{"enable_thinking":false}']
(out/'server.json').write_text(json.dumps({'pid':os.getpid(),'command':cmd,'source':s},indent=2));os.execvp(cmd[0],cmd)
