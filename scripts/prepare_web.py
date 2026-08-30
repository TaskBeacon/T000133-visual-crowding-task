"""Copy canonical materials/config and write a statically collectable asset map."""
from pathlib import Path
import json,shutil,string,yaml

t=Path(__file__).resolve().parents[1];h=t.parent/'H000133-visual-crowding-task'
for folder in ('config','src','tests','validation','references','.github/workflows'): (h/folder).mkdir(parents=True,exist_ok=True)
shutil.copytree(t/'assets',h/'assets',dirs_exist_ok=True)
for name in ('config.yaml','config_diagnostic.yaml'): shutil.copy2(t/'config'/name,h/'config'/name)
for name in ('README.md','CHANGELOG.md','task_flow.png'): shutil.copy2(t/name,h/name)
for p in (t/'references').iterdir():
 if p.is_file(): shutil.copy2(p,h/'references'/p.name)
meta=yaml.safe_load((t/'taskbeacon.yaml').read_text(encoding='utf8'))
meta['id']='H000133';meta['variant']='html';meta['canonical']=False;meta['runtime']={'profile':'web','entrypoint':'main.ts'}
(h/'taskbeacon.yaml').write_text(yaml.safe_dump(meta,sort_keys=False,allow_unicode=True),encoding='utf8')
lines=["// Literal URLs are required so Vite collects every glyph in cold production builds.","export const glyphAssets: Record<string,string> = {"]
lines.extend(f"  {letter}: new URL('../assets/glyphs/{letter}.png', import.meta.url).href," for letter in string.ascii_lowercase)
lines.append('};\n');(h/'src/glyph_assets.ts').write_text('\n'.join(lines),encoding='utf8')
shutil.copy2(t.parent/'skills/task-py2js/references/notify-psyflow-web-workflow.yml',h/'.github/workflows/notify-psyflow-web.yml')
(h/'.gitignore').write_text('node_modules/\ndist/\n.cache/\n',encoding='utf8')
for root in (t,h): (root/'.gitattributes').write_text('validation/*.csv -text\nvalidation/*_raw.jsonl -text\nvalidation/*_reduced.json -text\n',encoding='utf8')
print(h)
