from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];path=root/'references/selected_papers.json'
papers=json.loads(path.read_text(encoding='utf8'))[:1]
papers[0].update(is_high_impact=True,citation_count=1197,used_for=['provided_foundational_bibliographic_source_only'])
for id,title,year,doi,roles in [
 ('PELLI2004','Crowding is unlike ordinary masking: Distinguishing feature integration from detection',2004,'10.1167/4.12.12',['primary_200ms_methods','simultaneous_flankers','center_spacing']),
 ('COATES2021','The generality of the critical spacing for crowded optotypes: From Bouma to the 21st century',2021,'10.1167/jov.21.11.18',['primary_constant_stimuli','explicit_historical_reanalysis','threshold_limitations'])]:
    papers.append(dict(id=id,title=title,year=year,journal='Journal of Vision',doi_or_url='https://doi.org/'+doi,citation_count=0,
                       is_high_impact=False,open_access=True,used_for=roles,
                       notes='Full text reviewed. Citation count not retrieved; zero is a schema sentinel, not a measured citation count. Historical Bouma details in Coates2021 are secondhand.'))
path.write_text(json.dumps(papers,indent=2),encoding='utf8')
