"""Additional final raw-import entry run; preserves the earlier complete export trio."""
from pathlib import Path
import csv,hashlib,json,sys
from types import SimpleNamespace
import yaml
t=Path(__file__).resolve().parents[1];sys.path.insert(0,str(t))
from src.utils import decode,geometry,make_schedule,summarize
h=t.parent/'H000133-visual-crowding-task';v=h/'validation';checks=[]
def check(name,ok):checks.append({'name':name,'status':'pass' if ok else 'fail'})
rows=json.loads((v/'browser_synthetic_v2_reduced.json').read_text());dom=json.loads((v/'browser_array_dom_v2.json').read_text());cfg=yaml.safe_load((t/'config/config_diagnostic.yaml').read_text(encoding='utf8'));s=SimpleNamespace(**{**cfg['window'],**cfg['task'],**cfg['timing']});m=json.loads((t/'assets/glyph_metrics.json').read_text())
check('final entry20trials exact canonical order',len(rows)==20 and [r['condition'] for r in rows]==make_schedule(s))
check('final entry correct/error/omission/F8/q outcomes',[r['report_response'] for r in rows]==['o','a',None,'f8','h','s','r','l','q','b','k','d','e','t','g','j','f','c','i','n'])
check('actual20arrays observed',[d['target'] for d in dom]==[r['target_letter'] for r in rows])
check('explicit1280x800syntheticviewport',all(r['pixel_width']==1280 and r['pixel_height']==800 and r['geometry_provenance']=='synthetic_geometry' for r in rows))
check('never verifiedgaze orphysicalcalibration',all(not r['gaze_verified'] and not r['physical_calibration_verified_by_software'] for r in rows))
check('canonicalsummary',rows[-1]['session_summary']==summarize(rows))
intervals=[r['array_to_report_software_interval_s'] for r in rows];check('all20fixed200mssoftwareinterval within2frames',all(r['array_duration']==.2 and r['array_response'] is None for r in rows) and all(abs(x-.2)<2/60 for x in intervals))
errors=[]
for row,d in zip(rows,dom):
 layout=geometry(decode(row['condition'],s),s.calibration,[1280,800],m,s.xheight_deg)
 check(f"trial{row['trial_id']} decoded PNG/fill count",len(layout)==len(d['images']) and all(i['fit']=='fill' and i['naturalWidth']==240 and i['naturalHeight']==600 for i in d['images']))
 for g,img in zip(layout,d['images']):
  b=img['box'];expected=[640+g['pos'][0]-g['size'][0]/2,400-g['pos'][1]-g['size'][1]/2,*g['size']];errors.extend(abs(a-bb) for a,bb in zip([b['left'],b['top'],b['width'],b['height']],expected))
check('allDOMgeometrywithin0.05CSSpx',max(errors)<.05)
csvrows=list(csv.DictReader((v/'browser_synthetic_v2_reduced.csv').open(encoding='utf8',newline='')));check('actualCSVdataaligns',len(csvrows)==20 and [r['condition'] for r in csvrows]==[r['condition'] for r in rows])
hashes=[]
for kind,source in [('json','H000133-visual-crowding-task_reduced (2).json'),('csv','H000133-visual-crowding-task_reduced (1).csv')]:
 p=v/f'browser_synthetic_v2_reduced.{kind}';b=p.read_bytes();check(f'v2actual{kind}downloadbytes',b==(Path('C:/Users/frued/Downloads')/source).read_bytes());hashes.append({'file':p.name,'download':source,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
check('finalrefusalstablePNGsaved',(v/'browser_research_refusal_v2.png').stat().st_size>10000 and '研究模式拒绝运行' in (v/'browser_research_refusal_v2.txt').read_text(encoding='utf8'))
manifest=json.loads((v/'browser_v1_evidence_manifest.json').read_text(encoding='utf-8-sig'));check('previousactualevidenceunchanged',all(hashlib.sha256((v/r['file']).read_bytes()).hexdigest().upper()==r['sha256'] for r in manifest))
report={'status':'pass' if all(c['status']=='pass' for c in checks) else 'fail','count':len(checks),'checks':checks,'range_s':[min(intervals),max(intervals)],'max_dom_error_css_px':max(errors),'downloads':hashes,'limitations':['v2raw download click was canceled by premature tab close; not retained or fabricated','The unchanged export runtime was already validated using the retained v1trio and82rawstages','Synthetic software test, not physical calibration or participant pilot']}
(v/'final_entry_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({k:report[k] for k in ['status','count','range_s','max_dom_error_css_px']},indent=2));sys.exit(report['status']!='pass')
