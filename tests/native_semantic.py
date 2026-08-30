"""Real native run_trial, known synthetic keys and separately rendered screenshots."""
import json,sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from psyflow import TaskSettings,StimBank,StimUnit,initialize_exp,initialize_triggers,load_config,context_from_config,runtime_context
from psyflow.sim.contracts import Action
from src.run_trial import run_trial
from src.utils import validate_calibration,decode,geometry
root=Path(__file__).resolve().parents[1];out=root/'validation';out.mkdir(exist_ok=True)
cfg=load_config(str(root/'config/config_qa.yaml'));cfg['raw']['qa']['output_dir']='outputs/native_semantic'
ctx=context_from_config(task_dir=root,config=cfg,mode='qa')
active={'key':'a'}
class Responder:
    def act(self,obs):return Action(key=active['key'],rt_s=.12 if active['key'] else None)
    def start_session(self,*args):pass
    def end_session(self):pass
    def on_feedback(self,*args):pass
ctx.responder=Responder();rows=[]
with runtime_context(ctx):
    s=TaskSettings.from_dict(cfg['task_config']);s.add_subinfo({'subject_id':133});s.triggers=cfg['trigger_config']
    s.resolved_calibration=validate_calibration(s,True);s.glyph_metrics=json.loads((root/'assets/glyph_metrics.json').read_text())
    win,kb=initialize_exp(s);s.calibrated_pixel_size=list(map(int,win.size));bank=StimBank(win,cfg['stim_config']).preload_all();trigger=initialize_triggers(mock=True)
    fixcm=120*math.tan(math.radians(.15/2));bank.rebuild('fixation',update_cache=True,width=fixcm*32,height=fixcm*32)
    try:
        for name,key,target in [('correct','a','a'),('incorrect','b','a'),('omission',None,'a'),('gaze_break','f8','a'),('plain_q','q','q')]:
            active['key']=key;row=run_trial(win,kb,s,f'6|1|spacing_025|{target}',stim_bank=bank,trigger_runtime=trigger,block_id='native_semantic',block_idx=0)
            row['case']=name;rows.append(row)
        # Separately staged screenshots; do not insert capture overhead into measured semantic trials.
        for name,stims in [('native_instruction',[bank.get('instruction')]),('native_report',[bank.get('fixation'),bank.get('report_prompt')])]:
            for stim in stims:stim.draw()
            win.getMovieFrame(buffer='back');win.saveMovieFrames(str(out/f'{name}.png'));win.flip()
        for name,condition in [('native_near','3|1|spacing_025|a'),('native_far','6|-1|spacing_075|g'),('native_unflanked','6|1|unflanked|q')]:
            layout=geometry(decode(condition,s),s.resolved_calibration,win.size,s.glyph_metrics,s.xheight_deg)
            bank.get('fixation').draw()
            for i,g in enumerate(layout):bank.rebuild(['target','inner_x','outer_x'][i],image=f'assets/glyphs/{g["letter"]}.png',pos=g['pos'],size=g['size']).draw()
            win.getMovieFrame(buffer='back');win.saveMovieFrames(str(out/f'{name}.png'));win.flip()
    finally:win.close();trigger.close()
checks={'correct':rows[0]['correct'],'incorrect':not rows[1]['correct'],'omission':rows[2]['omission'],
        'gaze_break_excluded':rows[3]['reported_fixation_break'] and not rows[3]['eligible_accuracy'],
        'plain_q_not_quit':rows[4]['correct'],'synthetic_provenance':all(r['geometry_provenance']=='synthetic_geometry' for r in rows),
        'four_phases':all(all(f'{p}_flip_time' in r for p in ['fixation','array','report','intertrial']) for r in rows),
        'array_fixed_requested':all(r['array_duration']==.2 for r in rows),
        'software_array_interval':all(.18<=r['array_to_report_software_interval_s']<=.27 for r in rows),
        'gaze_never_verified':all(r['gaze_verified'] is False for r in rows)}
(out/'native_semantic.json').write_text(json.dumps({'passed':all(checks.values()),'checks':checks,'rows':rows,
 'limitation':'Real PsychoPy/PsyFlow trial with synthetic responder keys and synthetic_geometry. Separate actual rendered back-buffer captures. No OS key injection, human pilot, eye tracking or physical calibration.'},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(checks));assert all(checks.values())
