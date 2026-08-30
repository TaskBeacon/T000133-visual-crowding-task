"""Exercise actual human main before initialization with missing physical calibration."""
import sys,json
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import main as task
root=Path(__file__).resolve().parents[1];out=root/'validation';out.mkdir(exist_ok=True)
original_collect=task.SubInfo.collect;original_init=task.initialize_exp;calls=[];message=None
task.SubInfo.collect=lambda self:{'subject_id':'133'}
def unexpected_init(settings):calls.append(True);raise AssertionError('Uncalibrated human startup reached display initialization')
task.initialize_exp=unexpected_init
try:task.run(SimpleNamespace(mode='human',config_path=root/'config/config.yaml'))
except ValueError as exc:message=str(exc)
finally:task.SubInfo.collect=original_collect;task.initialize_exp=original_init
passed=bool(message) and not calls
(out/'human_startup_refusal.json').write_text(json.dumps({'passed':passed,'mode':'human','window_initialized':bool(calls),'error':message,
 'limitation':'Actual human main.run with synthetic identity and mocked form collection; verified missing-calibration refusal before native window. Not a measured human startup or physical pilot.'},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'passed':passed,'error':message}));assert passed
