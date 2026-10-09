"""PR186 bank projector and paid-moment routines, copied without mathematical changes.
Original attribution is retained in references/pr186_NOTICE and pr186_bit_prove.py.
Assembly adapter by huxint with substantial OpenAI Codex assistance. Apache-2.0.
"""
from fractions import Fraction as Q
from pathlib import Path
import sys

def need(ok,message):
    if not ok:raise ValueError(message)

# The caller binds the exact PR187 interval module after materializing its pinned tree.

def bind(interval):
    global moment,log_interval,exp_interval
    moment,log_interval,exp_interval=interval.moment,interval.log_interval,interval.exp_interval
    sys.path.insert(0,str(Path(__file__).resolve().parent/'references'))


def paid_moment(p,a,details=False):
    raw=moment(p,a,details);m,w=p['m'],p['W']
    count=sum(p['child_multiplicities'].values());bad=Q(1,10**16);fallback=32*m*m
    ll,lu=log_interval(Q(m));el,eu=exp_interval(a*ll,a*lu)
    weight=bad*Q(fallback*count,w*m)
    return dict(saving=a,lower=raw['lower']+weight*el,upper=raw['upper']+weight*eu,
        strict_gap_lower=1-raw['upper']-weight*eu,raw=raw,fallback_lower=weight*el,
        fallback_upper=weight*eu,edge_count=count,fallback_children_per_edge=fallback,
        bad_fraction=bad)

def bank_projectors():
    """Literal address maps on every F2 and integer basis column of two banks."""
    checks=[]
    for width,count in ((4,18),(24,3)):
        owner=[j//width for j in range(72)]
        need([owner.count(s) for s in range(count)]==[width]*count,'actual full bank partition')
        projectors=[[int(owner[j]==s) for j in range(72)] for s in range(count)]
        need(all(sum(P[j] for P in projectors)==1 for j in range(72)),'sum of actual projectors is identity')
        need(all(P[j]*P[j]==P[j] for P in projectors for j in range(72)),'idempotent bank projectors')
        need(all(P[j]*T[j]==0 for s,P in enumerate(projectors) for t,T in enumerate(projectors) if s!=t for j in range(72)),'pairwise disjoint bank projectors')
        def run(column,ring,indices):
            x=[0]*72;y=[0]*72
            (x if column<72 else y)[column%72]=1
            for s in indices:
                P=projectors[s]
                x,y=([a-P[j]*a+P[j]*b for j,(a,b) in enumerate(zip(x,y))],
                     [b-P[j]*b+P[j]*a for j,(a,b) in enumerate(zip(x,y))])
                if ring:x=[a%ring for a in x];y=[a%ring for a in y]
            return x+y
        controls={}
        for ring in (2,0):
            for column in range(144):
                expected=[0]*144;expected[(column+72)%144]=1
                need(run(column,ring,range(count))==expected,'completed bank full dirty swap formal column')
                need(run(column,ring,list(range(count))+list(reversed(range(count))))==[int(j==column) for j in range(144)],'completed bank inverse restores arbitrary contents')
            for tag,indices in (('omit_block',list(range(count-1))),('repeat_block',list(range(count))+[count-1])):
                column=72-width;expected=[0]*144;expected[column+72]=1
                need(run(column,ring,indices)!=expected,'adverse bank control rejected: '+tag)
                controls[str(ring)+':'+tag]=True
        checks.append(dict(width=width,blocks=count,ambient=72,rings=[2,0],formal_columns=288,
            inverse_columns=288,projectors_idempotent=True,projectors_disjoint=True,sum_is_identity=True,
            controls_rejected=controls,endpoint='partialSwap(P)(x,y)=(x-Px+Py,y-Py+Px)'))
    return checks

def independent_bank_moment(row,coarse):
    from base_two_moment import moment as alternate_moment
    W=int(3*row['W_per_vertex']);H=[(r,3*n) for r,n in row['child_histogram'].items()]
    count=sum(n for r,n in H);fallback=32*72**2*count
    _,upper=alternate_moment(72,W,H,coarse['coarse_saving'])
    _,bad_upper=alternate_moment(72,W,[(1,fallback)],coarse['coarse_saving'])
    gap=1-upper-Q(1,10**16)*bad_upper
    need(gap>0,'independent base-two paid moment contracts')
    next_saving=coarse['coarse_saving']+Q(1,coarse['coarse_grid'])
    lower,_=alternate_moment(72,W,H,next_saving)
    bad_lower,_=alternate_moment(72,W,[(1,fallback)],next_saving)
    need(lower+Q(1,10**16)*bad_lower>1,'independent base-two adjacent paid moment exclusion')
    return gap

def certify(row):
    p=dict(m=row['m'],W=row['W_per_vertex'],N=row['deficit_per_vertex'],L=0,
        total_rank=row['rank_per_vertex'],maxchild=row['maxchild'],child_multiplicities=row['child_histogram'])
    # Scale three clears the normalized moment fractions; the stage-private physical realization uses nine copies.
    p=dict(p,W=int(3*Q(p['W'])),N=3*p['N'],total_rank=3*p['total_rank'],
        child_multiplicities={r:3*n for r,n in p['child_multiplicities'].items()})
    grid=10**18;lo=0;hi=grid//100
    need(paid_moment(p,Q(lo,grid))['upper']<1,'zero-saving rank contraction')
    need(paid_moment(p,Q(hi,grid))['lower']>1,'upper bracket')
    while hi-lo>1:
        mid=(lo+hi)//2;r=paid_moment(p,Q(mid,grid))
        if r['upper']<1:lo=mid
        elif r['lower']>1:hi=mid
        else:raise ValueError('increase moment precision')
    coarse=Q(lo,grid);accepted=paid_moment(p,coarse,True);rejected=paid_moment(p,Q(hi,grid),True)
    need(accepted['upper']<1<rejected['lower'],'adjacent grid paid-moment proof')
    old=Q(384599,10**10);threshold=coarse/(1+coarse-old);atomgrid=10**24
    floor=(threshold*atomgrid).numerator//(threshold*atomgrid).denominator
    atom=Q(floor+1,atomgrid);actual=(1-atom)*coarse+atom*old
    need(actual<atom<1-actual,'paid atom and row adapter toll')
    need(Q(2*p['m']**3,2**80)<Q(1,10**16),'fixed prime rare-class bound')
    need(Q(p['total_rank'])+accepted['bad_fraction']*accepted['fallback_children_per_edge']*accepted['edge_count']<p['W']*p['m'],'contaminated mass contracts')
    previous=atom-Q(1,atomgrid)
    need(previous<=(1-previous)*coarse+previous*old,'previous atom grid does not pay strict toll')
    return dict(coarse_saving=coarse,accepted=accepted,rejected=rejected,coarse_grid=grid,
        atom_beta=atom,old_atom_saving=old,ordinary_saving=actual,atom_threshold=threshold,
        atom_grid=atomgrid,atom_lower_gap=atom-actual,atom_upper_gap=1-actual-atom,
        controls=dict(next_coarse_grid_rejected=True,previous_atom_grid_rejected=True),
        scope='Adjacent coarse exclusion for this fixed worst-case bad-class envelope and least atom on the stated grid; no true bad-fraction or global optimality claim.')
