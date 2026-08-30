from psyflow import StimUnit,next_trial_id,set_trial_context
from .utils import decode,geometry,score


def run_trial(win,kb,settings,condition,*,stim_bank,trigger_runtime,block_id,block_idx):
    trial_id=next_trial_id();factors=decode(condition,settings)
    if list(map(int,win.size))!=settings.calibrated_pixel_size:
        raise ValueError('Display dimensions changed; calibration invalidated.')
    layout=geometry(factors,settings.resolved_calibration,win.size,settings.glyph_metrics,settings.xheight_deg)
    row={'trial_id':trial_id,'condition':condition,'block_id':block_id,'block_idx':block_idx,**factors,
         'geometry_provenance':settings.resolved_calibration['provenance'],
         'screen_width_cm':settings.resolved_calibration['screen_width_cm'],
         'screen_height_cm':settings.resolved_calibration['screen_height_cm'],
         'viewing_distance_cm':settings.resolved_calibration['viewing_distance_cm'],
         'pixel_width':int(win.size[0]),'pixel_height':int(win.size[1]),
         'measurement_date':settings.resolved_calibration.get('measurement_date'),
         'measurement_method':settings.resolved_calibration.get('measurement_method'),
         'xheight_deg':settings.xheight_deg,'gaze_verified':False,'physical_calibration_verified_by_software':False}
    for index,item in enumerate(layout):
        label=['target','inner_flanker','outer_flanker'][index]
        row.update({f'{label}_x_px':item['pos'][0],f'{label}_y_px':item['pos'][1],f'{label}_width_px':item['size'][0],f'{label}_height_px':item['size'][1],f'{label}_angle_deg':item['angle_deg']})
    fixation=stim_bank.get('fixation')
    unit=StimUnit('fixation',win,kb,runtime=trigger_runtime).add_stim(fixation)
    set_trial_context(unit,trial_id=trial_id,phase='fixation',deadline_s=settings.fixation_duration,valid_keys=[],block_id=block_id,condition_id=condition,stim_id='fixation',task_factors=factors)
    unit.show(duration=settings.fixation_duration,onset_trigger=settings.triggers['fixation_onset']).to_dict(row)
    images=[]
    for i,item in enumerate(layout):
        name=f'glyph_{item["letter"]}' if i==0 else ['target','inner_x','outer_x'][i]
        stim=stim_bank.get(name)
        stim.setPos(item['pos']);stim.setSize(item['size']);images.append(stim)
    unit=StimUnit('array',win,kb,runtime=trigger_runtime).add_stim(fixation,*images)
    set_trial_context(unit,trial_id=trial_id,phase='array',deadline_s=settings.array_duration,valid_keys=[],block_id=block_id,condition_id=condition,stim_id='fixation+glyphs',task_factors=factors)
    unit.show(duration=settings.array_duration,onset_trigger=settings.triggers['array_onset']).to_dict(row)
    keys=list(settings.alphabet)+[settings.fixation_break_key]
    unit=StimUnit('report',win,kb,runtime=trigger_runtime).add_stim(fixation,stim_bank.get('report_prompt'))
    set_trial_context(unit,trial_id=trial_id,phase='report',deadline_s=settings.report_duration,valid_keys=keys,block_id=block_id,condition_id=condition,stim_id='fixation+report_prompt',task_factors=factors)
    response_triggers={key:settings.triggers['response'] for key in settings.alphabet};response_triggers[settings.fixation_break_key]=settings.triggers['fixation_break']
    unit.capture_response(keys=keys,duration=settings.report_duration,correct_keys=[factors['target_letter']],terminate_on_response=True,onset_trigger=settings.triggers['report_onset'],response_trigger=response_triggers,timeout_trigger=settings.triggers['omission'])
    unit.to_dict(row);row.update(score(unit.get_state('response'),factors['target_letter'],unit.get_state('rt'),settings.fixation_break_key))
    row['array_to_report_software_interval_s']=row['report_flip_time']-row['array_flip_time']
    unit=StimUnit('intertrial',win,kb,runtime=trigger_runtime).add_stim(fixation)
    set_trial_context(unit,trial_id=trial_id,phase='intertrial',deadline_s=settings.intertrial_duration,valid_keys=[],block_id=block_id,condition_id=condition,stim_id='fixation',task_factors=factors)
    unit.show(duration=settings.intertrial_duration,onset_trigger=settings.triggers['intertrial_onset']).to_dict(row)
    return row
