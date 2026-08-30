import copy,json,math,unittest
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
import yaml
from src.utils import make_schedule,decode,validate_calibration,geometry,score,summarize

ROOT=Path(__file__).resolve().parents[1]

class GeometryProtocolTests(unittest.TestCase):
    def setUp(self):
        self.s=SimpleNamespace(**yaml.safe_load((ROOT/'config/config_qa.yaml').read_text(encoding='utf8'))['task'])
        self.c=validate_calibration(self.s,True)
        self.m=json.loads((ROOT/'assets/glyph_metrics.json').read_text())
    def test_full_factorial_and_seed(self):
        self.s.diagnostic=False;labels=make_schedule(self.s)
        self.assertEqual(len(labels),500);self.assertEqual(len(set(labels)),500)
        self.assertEqual(set(Counter(x.rsplit('|',1)[0] for x in labels).values()),{25})
        self.assertEqual(labels,make_schedule(self.s));self.s.overall_seed+=1
        self.assertNotEqual(labels,make_schedule(self.s))
    def test_diagnostic_all_twenty_spatial_cells(self):
        labels=make_schedule(self.s)
        self.assertEqual(len(labels),20);self.assertEqual(len(set(x.rsplit('|',1)[0] for x in labels)),20)
    def test_projection_inverse_and_vertical_angle(self):
        for label in make_schedule(self.s):
            f=decode(label,self.s)
            for glyph in geometry(f,self.c,[1280,800],self.m,.5):
                x_cm=glyph['pos'][0]/32
                angle=math.degrees(math.atan2(x_cm,60))
                self.assertAlmostEqual(angle,glyph['angle_deg'],places=10)
                vertical_cm=glyph['xheight_px']/32
                vertical_angle=math.degrees(2*math.atan2(vertical_cm/2,math.hypot(60,x_cm)))
                self.assertAlmostEqual(vertical_angle,.5,places=10)
                # Align x-height midline, not transparent image-canvas center.
                bounds=self.m['glyph_bounds']['x'];scale_y=glyph['size'][1]/self.m['cell_height_px']
                y_mid=glyph['pos'][1]+glyph['size'][1]/2-(bounds[1]+bounds[3])/2*scale_y
                self.assertAlmostEqual(y_mid,0,places=10)
    def test_asymmetric_projection_and_independent_axes(self):
        f=decode('6|1|spacing_075|a',self.s);g=geometry(f,self.c,[1280,800],self.m,.5)
        self.assertGreater(g[2]['pos'][0]-g[0]['pos'][0],g[0]['pos'][0]-g[1]['pos'][0])
        altered=copy.deepcopy(self.c);altered['screen_height_cm']=24
        g2=geometry(f,altered,[1280,800],self.m,.5)
        self.assertEqual(g2[0]['size'][0],g[0]['size'][0]);self.assertGreater(g2[0]['size'][1],g[0]['size'][1])
    def test_bad_calibration_rejected(self):
        with self.assertRaises(ValueError):validate_calibration(self.s,False)
        self.s.calibration={'provenance':'missing','measurement_ack':'not_measured'}
        with self.assertRaises(ValueError):validate_calibration(self.s,False)
        c=copy.deepcopy(self.c);c['viewing_distance_cm']=200
        with self.assertRaises(ValueError):geometry(decode('6|1|spacing_075|a',self.s),c,[1280,800],self.m,.5)
    def test_score_distinguishes_error_omission_and_gaze(self):
        correct=score('q','q',.2,'f8');wrong=score('a','q',.3,'f8');missing=score(None,'q',None,'f8');gaze=score('f8','q',.1,'f8')
        self.assertTrue(correct['correct']);self.assertFalse(wrong['correct']);self.assertTrue(missing['omission'])
        self.assertFalse(gaze['omission']);self.assertFalse(gaze['eligible_accuracy']);self.assertFalse(gaze['gaze_verified'])
        rows=[dict(eccentricity_deg=3,side=1,spacing_condition='unflanked',**r) for r in [correct,wrong,missing,gaze]]
        cell=summarize(rows)['cells'][0];self.assertEqual(cell['eligible_n'],3);self.assertEqual(cell['accuracy'],1/3)
        self.assertIsNone(summarize(rows)['critical_spacing_deg'])

if __name__=='__main__':unittest.main()
