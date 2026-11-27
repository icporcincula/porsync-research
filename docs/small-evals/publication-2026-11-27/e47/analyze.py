"""Portable offline E47 accounting from selected labels and request durations."""
import argparse
import json
from pathlib import Path


def analyze(rows):
    result={}
    for arm in ['llama-iq3','strata-sq15','strata-sq15-thinking']:
        data=[r for r in rows if r['arm']==arm]
        assert len({r['id'] for r in data})==len(data)
        assert all(type(r['correct']) is bool and r['seconds']>=0 for r in data)
        n=len(data); k=sum(r['correct'] for r in data); seconds=sum(r['seconds'] for r in data)
        interval=None
        if n:
            z=1.959963984540054; p=k/n; den=1+z*z/n
            mid=(p+z*z/(2*n))/den; half=z*((p*(1-p)/n+z*z/(4*n*n))**.5)/den
            interval=[mid-half,mid+half]
        result[arm]=dict(n=n,correct=k,seconds=seconds,correct_per_hour=k/seconds*3600 if seconds else None,wilson95=interval,errors=sum(r['error'] for r in data),length_stops=sum(r.get('finish_reason')=='length' for r in data))
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('directory',nargs='?',type=Path,default=Path(__file__).resolve().parent); args=ap.parse_args()
    actual=analyze(json.loads((args.directory/'trials.json').read_text()))
    expected=json.loads((args.directory/'summary.json').read_text())
    assert actual==expected, 'summary does not reproduce'
    print(json.dumps(actual,indent=2))
