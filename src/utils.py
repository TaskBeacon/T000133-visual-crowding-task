"""Pure factorial schedule, explicit display geometry and outcome semantics."""
import math
import random
from collections import defaultdict


def make_schedule(settings):
    labels=[]
    for e in settings.eccentricities_deg:
        for side in (-1,1):
            for index, spacing in enumerate(settings.conditions):
                letters=settings.alphabet if not settings.diagnostic else settings.alphabet[(len(labels))%len(settings.alphabet)]
                labels.extend(f'{e}|{side}|{spacing}|{letter}' for letter in letters)
    random.Random(settings.overall_seed).shuffle(labels)
    return labels


def decode(condition, settings):
    e,side,spacing,letter=condition.split('|')
    ratio=settings.spacing_ratios.get(spacing)
    return {'eccentricity_deg':float(e),'side':int(side),'spacing_condition':spacing,
            'spacing_ratio':ratio,'spacing_deg':None if ratio is None else float(e)*ratio,'target_letter':letter}


def validate_calibration(settings, synthetic=False):
    c=dict(settings.calibration)
    if synthetic:
        if c.get('provenance')!='synthetic_geometry':
            raise ValueError('Synthetic runs require explicitly synthetic_geometry inputs.')
    else:
        for name in ('screen_width_cm','screen_height_cm','viewing_distance_cm','measurement_date','measurement_method','measurement_ack'):
            value=getattr(settings,name,None)
            if value is not None: c[name]=value
        if c.get('provenance')=='synthetic_geometry' or c.get('measurement_ack')!='measured':
            raise ValueError('研究模式拒绝运行：请由实验者实际测量屏幕可见宽高和眼屏距离，并确认 measured；不得填写EDID或假定值。')
        if not c.get('measurement_date') or not c.get('measurement_method'):
            raise ValueError('研究模式需要测量日期和方法。')
        c['provenance']='operator_reported_measurement'
    for name,low,high in [('screen_width_cm',15,200),('screen_height_cm',10,150),('viewing_distance_cm',25,200)]:
        try: value=float(c[name])
        except (KeyError,TypeError,ValueError): raise ValueError(f'Missing measured {name}') from None
        if not math.isfinite(value) or not low<=value<=high: raise ValueError(f'Invalid {name}')
        c[name]=value
    return c


def geometry(factors,c,pixel_size,metrics,xheight_deg):
    width,height=map(float,pixel_size)
    if min(width,height)<600: raise ValueError('Display too small for the audited instruction and array layout.')
    px_x=width/c['screen_width_cm'];px_y=height/c['screen_height_cm'];d=c['viewing_distance_cm']
    if not .85<=px_x/px_y<=1.15: raise ValueError('Display aspect/calibration mismatch (>15%).')
    e=factors['eccentricity_deg'];s=factors['spacing_deg'];side=factors['side']
    angles=[side*e] if s is None else [side*e,side*(e-s),side*(e+s)]
    result=[]
    for index,angle in enumerate(angles):
        # The x-height's vertical angular extent is preserved at each eccentricity.
        h_cm=2*d/math.cos(math.radians(angle))*math.tan(math.radians(xheight_deg/2))
        scale=h_cm/metrics['xheight_px']
        size=[metrics['cell_width_px']*scale*px_x,metrics['cell_height_px']*scale*px_y]
        x=d*math.tan(math.radians(angle))*px_x
        if h_cm*px_y<10: raise ValueError('Glyph x-height sampled by fewer than10 coordinate pixels.')
        if abs(x)+size[0]/2>width/2-20 or size[1]/2>height/2-20: raise ValueError('Array clipped by display bounds.')
        x_bounds=metrics['glyph_bounds']['x']
        y=((x_bounds[1]+x_bounds[3])/2-metrics['cell_height_px']/2)*scale*px_y
        result.append({'letter':factors['target_letter'] if index==0 else 'x','angle_deg':angle,'pos':[x,y],'size':size,'xheight_px':h_cm*px_y})
    ordered=sorted(result,key=lambda q:q['pos'][0])
    for a,b in zip(ordered,ordered[1:]):
        if a['pos'][0]+a['size'][0]/2>=b['pos'][0]-b['size'][0]/2:
            raise ValueError('Glyph cells overlap; refusing spatial masking confound.')
    return result


def score(response,target,rt,break_key):
    violation=response==break_key
    return {'reported_letter':None if violation else response,'reported_fixation_break':violation,
            'gaze_verified':False,'omission':response is None,'correct':response==target and not violation,
            'eligible_accuracy':not violation,'identification_rt_s':rt,'rt_origin':'report_screen_onset'}


def summarize(rows):
    groups=defaultdict(list)
    for row in rows: groups[(row['eccentricity_deg'],row['side'],row['spacing_condition'])].append(row)
    result=[]
    for key,group in sorted(groups.items()):
        eligible=[r for r in group if r['eligible_accuracy']]
        result.append({'eccentricity_deg':key[0],'side':key[1],'spacing_condition':key[2],
                       'n':len(group),'eligible_n':len(eligible),'correct_n':sum(r['correct'] for r in eligible),
                       'accuracy':sum(r['correct'] for r in eligible)/len(eligible) if eligible else None,
                       'omission_n':sum(r['omission'] for r in group),
                       'reported_fixation_break_n':sum(r['reported_fixation_break'] for r in group)})
    return {'cells':result,'critical_spacing_deg':None,'threshold_status':'not_estimated',
            'gaze_verified':False,'physical_calibration_verified_by_software':False}
