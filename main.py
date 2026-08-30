from contextlib import nullcontext
from functools import partial
from pathlib import Path
import json
import math
import pandas as pd
from psychopy import core
from psyflow import (BlockUnit,StimBank,StimUnit,SubInfo,TaskSettings,context_from_config,
    initialize_exp,initialize_triggers,load_config,parse_task_run_options,runtime_context)
from src.run_trial import run_trial
from src.utils import make_schedule,validate_calibration,geometry,decode,summarize

MODES=('human','qa','sim')
DEFAULT_CONFIG_BY_MODE={'human':'config/config.yaml','qa':'config/config_qa.yaml','sim':'config/config_scripted_sim.yaml'}


def run(options):
    task_root=Path(__file__).resolve().parent
    cfg=load_config(str(options.config_path))
    ctx=context_from_config(task_dir=task_root,config=cfg,mode=options.mode) if options.mode in ('qa','sim') else None
    with runtime_context(ctx) if ctx else nullcontext():
        subject={'subject_id':133} if ctx else SubInfo(cfg['subform_config']).collect()
        settings=TaskSettings.from_dict(cfg['task_config']);settings.add_subinfo(subject)
        settings.resolved_calibration=validate_calibration(settings,synthetic=ctx is not None)
        if ctx:
            ctx.output_dir.mkdir(parents=True,exist_ok=True)
            settings.res_file=str(ctx.output_dir/('qa_trace.csv' if options.mode=='qa' else 'sim_trace.csv'))
            settings.log_file=str(ctx.output_dir/'psychopy.log');settings.json_file=str(ctx.output_dir/'settings.json')
        elif not settings.fullscreen:
            raise ValueError('Research display must be fullscreen.')
        # The framework monitor object is not used for degree rendering; no fallback measurements.
        settings.monitor_width_cm=settings.resolved_calibration['screen_width_cm']
        settings.monitor_distance_cm=settings.resolved_calibration['viewing_distance_cm']
        settings.triggers=cfg['trigger_config']
        trigger_runtime=initialize_triggers(mock=True) if ctx else initialize_triggers(cfg)
        win,kb=initialize_exp(settings)
        try:
            settings.calibrated_pixel_size=list(map(int,win.size))
            settings.glyph_metrics=json.loads((task_root/'assets/glyph_metrics.json').read_text(encoding='utf8'))
            labels=make_schedule(settings)
            for condition in labels: geometry(decode(condition,settings),settings.resolved_calibration,win.size,settings.glyph_metrics,settings.xheight_deg)
            stim_bank=StimBank(win,cfg['stim_config']).preload_all()
            fix_h=2*settings.resolved_calibration['viewing_distance_cm']*math.tan(math.radians(.15/2))
            stim_bank.rebuild('fixation',update_cache=True,width=fix_h*win.size[0]/settings.resolved_calibration['screen_width_cm'],height=fix_h*win.size[1]/settings.resolved_calibration['screen_height_cm'])
            settings.save_to_json();rows=[];trigger_runtime.send(settings.triggers['experiment_start'])
            StimUnit('instruction',win,kb,runtime=trigger_runtime).add_stim(stim_bank.get('instruction')).wait_and_continue(keys=[settings.continue_key])
            for block_idx,start in enumerate(range(0,len(labels),settings.trial_per_block)):
                planned=labels[start:start+settings.trial_per_block];block_id=f'block_{block_idx+1}'
                block=BlockUnit(block_id=block_id,block_idx=block_idx,settings=settings,window=win,keyboard=kb,n_trials=len(planned))
                block.generate_conditions(condition_labels=planned,order='sequential')
                block.run_trial(partial(run_trial,stim_bank=stim_bank,trigger_runtime=trigger_runtime,block_id=block_id,block_idx=block_idx));block.to_dict(rows)
                pd.DataFrame(rows).to_csv(settings.res_file,index=False)
                if start+settings.trial_per_block<len(labels):
                    StimUnit('block_break',win,kb,runtime=trigger_runtime).add_stim(stim_bank.get('block_break')).wait_and_continue(keys=[settings.continue_key])
            Path(settings.res_file).with_suffix('.summary.json').write_text(json.dumps(summarize(rows),ensure_ascii=False,indent=2),encoding='utf8')
            StimUnit('good_bye',win,kb,runtime=trigger_runtime).add_stim(stim_bank.get('good_bye')).wait_and_continue(keys=[settings.continue_key])
            trigger_runtime.send(settings.triggers['experiment_end'])
        finally:
            trigger_runtime.close();win.close()
    core.quit()


def main():
    run(parse_task_run_options(task_root=Path(__file__).resolve().parent,description='Visual Crowding Task',default_config_by_mode=DEFAULT_CONFIG_BY_MODE,modes=MODES))

if __name__=='__main__': main()
