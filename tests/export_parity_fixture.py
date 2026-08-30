"""Canonical synthetic test fixtures, not participant observations."""
from pathlib import Path
from types import SimpleNamespace
import json,sys,yaml
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from src.utils import make_schedule,decode,geometry,validate_calibration,score,summarize
cfg=yaml.safe_load((root/'config/config_diagnostic.yaml').read_text(encoding='utf8'))
s=SimpleNamespace(**{**cfg['window'],**cfg['task'],**cfg['timing']})
c=validate_calibration(s,True);metrics=json.loads((root/'assets/glyph_metrics.json').read_text())
diagnostic=make_schedule(s);s.diagnostic=False;full=make_schedule(s)
layouts=[]
for size in ([1280,800],[1920,1080]):
 for label in full: layouts.append({'condition':label,'pixel_size':size,'layout':geometry(decode(label,s),c,size,metrics,s.xheight_deg)})
outcomes=[score(k,'q',None if k is None else .123,'f8') for k in ('q','b',None,'f8')]
inputs=[]
for value in ('40',' 40.0 ','4e1','4_0','0x20','0b101000','Infinity','NaN','','39.9cm'):
 candidate=SimpleNamespace(**vars(s));candidate.calibration={**c,'provenance':'missing','measurement_ack':'measured','measurement_date':'synthetic-test-only','measurement_method':'invalid-input test'};candidate.screen_width_cm=value
 try: result=validate_calibration(candidate,False);inputs.append({'input':value,'accepted':True,'value':result['screen_width_cm']})
 except ValueError: inputs.append({'input':value,'accepted':False})
fixture={'provenance':'synthetic_software_fixture_not_measurement','diagnostic':diagnostic,'full':full,'layouts':layouts,'outcomes':outcomes,'calibration_inputs':inputs}
target=root.parent/'H000133-visual-crowding-task/validation/python_parity_fixture.json';target.write_text(json.dumps(fixture,indent=2),encoding='utf8');print(target)
