from dataclasses import dataclass
from psyflow.sim.contracts import Action

@dataclass
class TaskSamplerResponder:
    rt_s:float=.15
    def start_session(self,session,rng): self.rng=rng
    def act(self,obs):
        keys=list(obs.valid_keys or [])
        if not keys:return Action(key=None,rt_s=None)
        if len(keys)==1:return Action(key=keys[0],rt_s=self.rt_s)
        choice=self.rng.random()
        if choice<.1:return Action(key=None,rt_s=None)
        if choice<.2:return Action(key='f8',rt_s=self.rt_s)
        target=obs.task_factors.get('target_letter','a')
        return Action(key=target if choice<.75 else keys[(keys.index(target)+1)%25],rt_s=self.rt_s)
    def on_feedback(self,feedback):pass
    def end_session(self):pass
