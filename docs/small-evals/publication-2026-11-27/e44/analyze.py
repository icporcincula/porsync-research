"""Portable E44 saved-label accounting; no private tests or model calls."""
from pathlib import Path
import json, math, statistics
rows=json.loads((Path(__file__).resolve().parent/'trials.json').read_text())
expected={'v5b':21,'aider':10,'sonnet':24,'haiku':24}
assert len(rows)==96
for arm,k in expected.items():
    group=[r for r in rows if r['arm']==arm]
    assert len(group)==24 and sum(r['green'] for r in group)==k
    assert len({(r['fixture'],r['repeat']) for r in group})==24
    print(arm,k,'/24; median seconds',statistics.median(r['seconds'] for r in group))
def pairs(a,b):
    wins=losses=ties=0
    for fixture in sorted({r['fixture'] for r in rows}):
        x=sum(r['green'] for r in rows if r['arm']==a and r['fixture']==fixture)
        y=sum(r['green'] for r in rows if r['arm']==b and r['fixture']==fixture)
        wins+=x>y;losses+=x<y;ties+=x==y
    n=wins+losses
    p=min(1,2*sum(math.comb(n,i) for i in range(min(wins,losses)+1))/2**n) if n else 1
    return wins,losses,ties,p
assert pairs('v5b','aider')==(5,0,3,.0625)
assert pairs('sonnet','v5b')==(3,0,5,.25)
assert pairs('haiku','v5b')==(3,0,5,.25)
print('E44 paired counts and descriptive exact sign tests reproduced')


summary=json.loads((Path(__file__).resolve().parent/'summary.json').read_text())
assert summary['arm_passes']==expected
def cdf(k,n,p):
    return sum(math.comb(n,i)*p**i*(1-p)**(n-i) for i in range(k+1))
def inverse_cdf(k,n,target):
    lo,hi=0.,1.
    for _ in range(100):
        mid=(lo+hi)/2
        if cdf(k,n,mid)>target:lo=mid
        else:hi=mid
    return (lo+hi)/2
ci=[inverse_cdf(9,24,.975),inverse_cdf(10,24,.025)]
assert all(abs(a-b)<1e-12 for a,b in zip(ci,summary['aider_clopper_pearson_95']))
print('E44 corrected Aider exact Clopper-Pearson interval reproduced:',ci)
