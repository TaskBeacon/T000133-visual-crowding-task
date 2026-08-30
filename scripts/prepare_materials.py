"""Create shared Courier glyph assets and explicit research/synthetic profiles."""
from pathlib import Path
import copy,json,string
from PIL import Image,ImageDraw,ImageFont
import yaml

root=Path(__file__).resolve().parents[1]
(root/'assets/glyphs').mkdir(parents=True,exist_ok=True);(root/'config').mkdir(exist_ok=True)
font_path=Path('C:/Windows/Fonts/cour.ttf')
font=ImageFont.truetype(str(font_path),400)
width=round(font.getlength('x'));height=600;baseline=400
metrics={'font_source':'Windows Courier New regular; glyph raster derivatives only; font file not distributed',
         'cell_width_px':width,'cell_height_px':height,'baseline_px':baseline,'xheight_px':None,'glyph_bounds':{}}
for letter in string.ascii_lowercase:
    image=Image.new('RGBA',(width,height),(255,255,255,0));draw=ImageDraw.Draw(image)
    draw.text((width/2,baseline),letter,font=font,anchor='ms',fill=(0,0,0,255))
    bounds=image.getchannel('A').getbbox();metrics['glyph_bounds'][letter]=bounds
    if letter=='x':metrics['xheight_px']=bounds[3]-bounds[1]
    image.save(root/f'assets/glyphs/{letter}.png')
(root/'assets/glyph_metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf8')
alphabet=string.ascii_lowercase.replace('x','')
fields=[{'name':'subject_id','type':'int','constraints':{'min':101,'max':999,'digits':3}}]
for name in ['screen_width_cm','screen_height_cm','viewing_distance_cm','measurement_date','measurement_method']:
    fields.append({'name':name,'type':'string'})
fields.append({'name':'measurement_ack','type':'choice','choices':['not_measured','measured']})
mapping={'subject_id':'被试编号（3位数字）','screen_width_cm':'实测屏幕可见宽度（厘米，不是EDID值）',
         'screen_height_cm':'实测屏幕可见高度（厘米）','viewing_distance_cm':'实测眼睛至屏幕距离（厘米）',
         'measurement_date':'测量日期','measurement_method':'测量工具与方法','measurement_ack':'确认实际测量',
         'not_measured':'未实测：禁止研究运行','measured':'已使用尺具实际测量','Participant Information':'实验登记与实测几何',
         'registration_failed':'登记失败','registration_successful':'登记成功','invalid_input':'{field} 输入无效'}
def text(content,pos=(0,0),height=24):return {'type':'text','font':'SimHei','text':content,'color':'black','height':height,'wrapWidth':1100,'pos':list(pos),'units':'pix'}
cfg={'subinfo_fields':fields,'subinfo_mapping':mapping,
     'window':{'size':[1280,800],'units':'pix','screen':0,'bg_color':'white','fullscreen':True},
     'task':{'task_name':'Visual Crowding Task','language':'Chinese','voice_enabled':False,'voice_name':'zh-CN-YunyangNeural',
             'save_path':'./outputs/human','total_blocks':5,'total_trials':500,'trial_per_block':100,
             'conditions':['unflanked','spacing_025','spacing_040','spacing_055','spacing_075'],
             'condition_weights':None,'eccentricities_deg':[3,6],'spacing_ratios':{'unflanked':None,'spacing_025':.25,'spacing_040':.4,'spacing_055':.55,'spacing_075':.75},
             'alphabet':alphabet,'xheight_deg':.5,'continue_key':'space','fixation_break_key':'f8','key_list':list(alphabet)+['f8','space'],
             'overall_seed':133031,'seed_mode':'same_across_sub','diagnostic':False,'hide_cursor':True,'delta':0,
             'calibration':{'screen_width_cm':None,'screen_height_cm':None,'viewing_distance_cm':None,'measurement_date':None,'measurement_method':None,'measurement_ack':'not_measured','provenance':'missing'}},
     'timing':{'fixation_duration':.6,'array_duration':.2,'report_duration':4.0,'intertrial_duration':.3},
     'stimuli':{'instruction':text('视觉拥挤任务\n\n请保持头部位置，双眼始终注视屏幕中央黑方块。\n不要看向外周字母；字母会短暂出现在左边或右边。\n有时只有一个字母，有时两侧各有一个 x。\n记住中间目标字母，不要报告两侧的 x。\n\n字母消失、提示出现后，按对应英文字母键作答。\n请使用英文输入法；目标不会是 x。每次最多4秒。\n如果刚才发现自己看向了目标或离开中央注视，请按F8。\nF8仅记录你的报告，系统没有眼动仪，不能核实注视。\n\n每100次可以休息。本任务不提供临床判断或视觉常模。\n准备好后按空格。'),
                'fixation':{'type':'rect','units':'pix','width':6,'height':6,'fillColor':'black','lineColor':'black','lineWidth':0,'pos':[0,0]},
                'report_prompt':text('请报告刚才的目标字母；发现注视偏离请按F8。',(0,-150)),
                'block_break':text('本组完成，可以休息。\n\n继续前请恢复原来的头部位置和眼屏距离。\n始终看中央方块，不要追看外周字母。\n按空格继续。'),
                'good_bye':text('任务完成，谢谢参与。\n\n系统没有核实注视，也没有验证实际屏幕标定。\n本任务不自动估计临界间距，不提供视力或临床常模。\n按空格保存并结束。')},
     'triggers':{'map':{'experiment_start':1,'fixation_onset':10,'array_onset':20,'report_onset':30,'response':31,'fixation_break':32,'omission':33,'intertrial_onset':40,'experiment_end':99},'driver':{'type':'mock'},'policy':{'strict':False},'timing':{'post_delay_s':0.0}}}
for key,letter in [('target','a'),('inner_x','x'),('outer_x','x')]:
    cfg['stimuli'][key]={'type':'image','image':f'assets/glyphs/{letter}.png','size':[30,75],'pos':[0,0],'units':'pix'}
for letter in alphabet:
    cfg['stimuli'][f'glyph_{letter}']={'type':'image','image':f'assets/glyphs/{letter}.png','size':[30,75],'pos':[0,0],'units':'pix'}
for profile in ['config','config_qa','config_scripted_sim','config_sampler_sim','config_diagnostic']:
    out=copy.deepcopy(cfg)
    if profile!='config':
        out['subinfo_fields']=fields[:1];out['task'].update({'total_blocks':1,'total_trials':20,'trial_per_block':20,'diagnostic':True})
        out['task']['calibration']={'screen_width_cm':40,'screen_height_cm':25,'viewing_distance_cm':60,'measurement_date':'synthetic','measurement_method':'synthetic_fixture_not_measured','measurement_ack':'not_measured','provenance':'synthetic_geometry'}
        out['window']['fullscreen']=False
        out['stimuli']['instruction']['text']='软件验证：使用合成几何，不是实测屏幕或被试数据。\n本次20次，保留正式试次时序和所有空间条件。\n\n'+out['stimuli']['instruction']['text']
        out['stimuli']['instruction']['height']=22
    if profile=='config_qa':
        out['qa']={'output_dir':'outputs/qa','enable_scaling':False,'timing_scale':1,'min_frames':2,'strict':False,'max_wait_s':120,
                   'acceptance_criteria':{'required_columns':['trial_id','condition','correct','geometry_provenance','reported_fixation_break'],'expected_trial_count':20,'triggers_required':True}}
        out['responder']={'type':'responders.task_sampler:TaskSamplerResponder','kwargs':{'rt_s':.15}}
    if profile in ('config_scripted_sim','config_sampler_sim'):
        kind='scripted_sim' if profile=='config_scripted_sim' else 'sampler_sim'
        out['sim']={'output_dir':f'outputs/{kind}','seed':133031,'participant_id':'synthetic133','session_id':kind,'log_path':f'outputs/{kind}/sim_events.jsonl','policy':'strict','default_rt_s':.15,'clamp_rt':True,'enable_scaling':False,'timing_scale':1,'min_frames':2,
                    'responder':{'type':'scripted','kwargs':{'rt_s':.15}} if kind=='scripted_sim' else {'type':'responders.task_sampler:TaskSamplerResponder','kwargs':{'rt_s':.15}}}
    (root/f'config/{profile}.yaml').write_text(yaml.safe_dump(out,allow_unicode=True,sort_keys=False),encoding='utf8')
print(json.dumps({'glyphs':26,'xheight_px':metrics['xheight_px'],'cell_size':[width,height]}))
