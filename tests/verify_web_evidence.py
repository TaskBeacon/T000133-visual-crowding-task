"""Inspect real downloaded synthetic browser data and observed DOM geometry."""
from pathlib import Path
from types import SimpleNamespace
import csv,hashlib,json,math,sys,yaml
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from src.utils import decode,geometry,make_schedule,summarize
h=root.parent/'H000133-visual-crowding-task';v=h/'validation'
rows=json.loads((v/'browser_synthetic_reduced.json').read_text());raw=[json.loads(x) for x in (v/'browser_synthetic_raw.jsonl').read_text().splitlines()]
dom=json.loads((v/'browser_array_dom.json').read_text());checks=[]
def check(name,result):
 checks.append({'name':name,'status':'pass' if result else 'fail'})
cfg=yaml.safe_load((root/'config/config_diagnostic.yaml').read_text(encoding='utf8'));s=SimpleNamespace(**{**cfg['window'],**cfg['task'],**cfg['timing']});metrics=json.loads((root/'assets/glyph_metrics.json').read_text())
check('20 reduced rows /82 raw phases',len(rows)==20 and len(raw)==82)
check('exact canonical diagnostic order',[r['condition'] for r in rows]==make_schedule(s))
check('20 observed target arrays in same order',[d['target'] for d in dom]==[r['target_letter'] for r in rows])
check('actual expected responses',[r['report_response'] for r in rows]==['o','a',None,'f8','h','s','r','l','q','b','k','d','e','t','g','j','f','c','i','n'])
check('17 correct /1 wrong /1 omission /1 F8',sum(r['correct'] for r in rows)==17 and sum(r['omission'] for r in rows)==1 and sum(r['reported_fixation_break'] for r in rows)==1 and sum(r['eligible_accuracy'] for r in rows)==19)
check('ordinary q is correct response',rows[8]['report_response']=='q' and rows[8]['correct'])
check('early array key neither captured nor truncated exposure',rows[0]['array_response'] is None and not rows[0]['array_key_press'] and rows[0]['array_duration']==.2 and rows[0]['report_response']=='o')
check('all array durations200ms and no response window',all(r['array_duration']==.2 and r['array_valid_keys']==[] and r['array_response'] is None for r in rows))
intervals=[r['array_to_report_software_interval_s'] for r in rows]
check('observed array-to-report software intervals within two60Hzframes',all(abs(x-.2)<=2/60 for x in intervals))
check('report RT origin preserved',all(r['rt_origin']=='report_screen_onset' and r['identification_rt_s']==r['report_rt'] for r in rows))
check('four phases in each completed trial',all([x['phase'] for x in raw if x['trial_id']==r['trial_id']]==['fixation','array','report','intertrial'] for r in rows))
check('synthetic provenance every row / never gaze or calibration verified',all(r['geometry_provenance']=='synthetic_geometry' and not r['gaze_verified'] and not r['physical_calibration_verified_by_software'] and r['measurement_method']=='synthetic_fixture_not_measured' for r in rows))
check('summary agrees with Python canonical',rows[-1]['session_summary']==summarize(rows))
errors=[]
for row,observed in zip(rows,dom):
 size=[row['pixel_width'],row['pixel_height']];layout=geometry(decode(row['condition'],s),s.calibration,size,metrics,s.xheight_deg)
 check(f"trial{row['trial_id']} correct glyph count/natural pixels/fill",len(observed['images'])==len(layout) and all(i['fit']=='fill' and i['naturalWidth']==240 and i['naturalHeight']==600 for i in observed['images']))
 for predicted,image in zip(layout,observed['images']):
  box=image['box'];expected=[size[0]/2+predicted['pos'][0]-predicted['size'][0]/2,size[1]/2-predicted['pos'][1]-predicted['size'][1]/2,*predicted['size']]
  errors.extend(abs(a-b) for a,b in zip([box['left'],box['top'],box['width'],box['height']],expected))
check('actual DOM per-axis geometry within0.05CSSpx of canonical',max(errors)<.05)
check('actual CSS extents equal exported denominator',all(r['display_snapshot']['width']==r['pixel_width'] and r['display_snapshot']['height']==r['pixel_height'] for r in rows))
check('native/web26 glyph bytes identical',all((root/'assets/glyphs'/f'{c}.png').read_bytes()==(h/'assets/glyphs'/f'{c}.png').read_bytes() for c in 'abcdefghijklmnopqrstuvwxyz'))
check('native/web full and diagnostic YAML identical',all((root/'config'/n).read_bytes()==(h/'config'/n).read_bytes() for n in ['config.yaml','config_diagnostic.yaml']))
http=json.loads((v/'cold_asset_http.json').read_text(encoding='utf-8-sig'));check('cold26assetHTTP200imagePNG',len(http)==26 and all(i['status']==200 and i['type']==['image/png'] for i in http))
check('successful browser entry requires26completeddecodes',len(http)==26 and len(rows)==20 and (v/'browser_console.json').read_text().strip()=='[]')
csvrows=list(csv.DictReader((v/'browser_synthetic_reduced.csv').open(encoding='utf8',newline='')))
check('download CSV row order/response/provenance',len(csvrows)==20 and all(a['condition']==b['condition'] and a['geometry_provenance']==b['geometry_provenance'] and a['report_response']==(b['report_response'] or '') for a,b in zip(csvrows,rows)))
sources={
 'browser_synthetic_reduced.json':'H000133-visual-crowding-task_reduced (1).json',
 'browser_synthetic_reduced.csv':'H000133-visual-crowding-task_reduced.csv',
 'browser_synthetic_raw.jsonl':'H000133-visual-crowding-task_raw (2).jsonl'}
hashes=[]
for name,source in sources.items():
 a=(v/name).read_bytes();b=(Path('C:/Users/frued/Downloads')/source).read_bytes();check(f'original download bytes preserved: {name}',a==b);hashes.append({'archive':name,'download':source,'bytes':len(a),'sha256':hashlib.sha256(a).hexdigest()})
partial=json.loads((v/'browser_resize_reduced.json').read_text());partialraw=[json.loads(x) for x in (v/'browser_resize_raw.jsonl').read_text().splitlines()]
check('resize retains completed3rows and partialtrial4report in16raw',len(partial)==3 and len(partialraw)==16 and partialraw[-1]['trial_id']==4 and partialraw[-1]['phase']=='report')
check('resize stops current report before next trial',max(x['trial_id'] for x in partialraw if isinstance(x['trial_id'],int))==4 and not any(x['trial_id']==4 and x['phase']=='intertrial' for x in partialraw))
check('resize reason calibration_invalidated','calibration_invalidated' in (v/'browser_resize_summary.txt').read_text())
check('research actual unconfirmed input refusal','研究模式拒绝运行' in (v/'browser_research_refusal.txt').read_text(encoding='utf8'))
report={'status':'pass' if all(c['status']=='pass' for c in checks) else 'fail','checks':checks,'count':len(checks),'software_array_to_report_range_s':[min(intervals),max(intervals)],'max_dom_geometry_error_css_px':max(errors),'download_hashes':hashes,'limitations':['Synthetic QA only; no actual measurement or participant pilot','Software interval is not photodiode exposure','No gaze verification','Resize interrupted trial remains raw-only; incomplete report is not falsely scored']}
(v/'browser_data_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({k:report[k] for k in ['status','count','software_array_to_report_range_s','max_dom_geometry_error_css_px']},indent=2));sys.exit(0 if report['status']=='pass' else 1)
