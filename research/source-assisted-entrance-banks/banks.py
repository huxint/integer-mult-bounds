#!/usr/bin/env python3
"""Completed PR186 entrance banks on PR187's globally emitted bit word.

The unpaired rank-20 high streams are retained exactly under old_to_new.
Source-assisted low operations touch only undeferred streams. All aliases
are internal physical splices. The completed-bank endpoint is the inherited
universal partial-swap identity, checked again on every address column.
Prepared by huxint with substantial OpenAI Codex assistance. Apache-2.0.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import importlib.util,json,sys
from bank_arithmetic import bank_projectors


def need(ok,message):
    if not ok:raise ValueError(message)


def certify(model,profile,bit_source):
    R,v,h=model['R'],model['v'],model['h']
    need((v,h,profile['m'])==(1760,24,72),'retained bit dimensions')
    pairs=model['pairs'];recipients={b for a,b in pairs};donors={a for a,b in pairs}
    gauge={z['role']:z for z in model['gauges']}
    need(len(pairs)==len(recipients)==len(donors)==1760 and not recipients&donors,'disjoint complete physical aliases')
    need(not donors&set(gauge) and recipients<=set(gauge),'only ungauged donors and gauged recipients')
    need(all(gauge[b]['dim']==21 for b in recipients),'paired rank21 gauges are internal splices')
    live=sorted(set(range(R))-recipients)
    entrance=sorted(set(gauge)-recipients);plain=sorted(set(live)-set(entrance))
    need(len(live)==profile['physical_R']==17588,'all physical bit slots independently recounted')
    need(len(entrance)==2200 and len(plain)==15388,'complete bank role partition')
    need(all(gauge[s]['dim']==20 for s in entrance),'rank20 physical entrances only')
    need(not set(entrance)&set(plain) and set(entrance)|set(plain)==set(live),'each physical chain banked exactly once')

    # Reconstruct the original high suffix and its gauge frames, independently
    # of the emitter's advertised boundary digest.
    sys.path.insert(0,str(bit_source/'scripts'))
    spec=importlib.util.spec_from_file_location('bank_original_bit',bit_source/'scripts/paired_cube_bit_physical.py')
    backend=importlib.util.module_from_spec(spec);spec.loader.exec_module(backend)
    checker=backend.loaded();checker.frames()
    original=checker.w;mapping={int(k):n for k,n in model['old_to_new'].items()}
    phase=set(original['phase1']);order=sorted(phase)+[i for i in range(len(original['ops'])) if i not in phase]
    high=[]
    for i in order:
        a,b,_=original['ops'][i];f=original['op_frame'][i]
        if checker.dimf[f]>3:high.append(['a',mapping[a],mapping[b],f])
    emitted=[op for op in model['ops'] if checker.dimf[op[3]]>3]
    need(emitted==high,'complete high suffix identical under actual role renumbering')
    original_gauges={z['role']:z for z in original['gauges']}
    need(len(original_gauges)==len(gauge)==3960,'every original gauge retained')
    for s,z in original_gauges.items():
        new=gauge[mapping[s]]
        need({k:v for k,v in z.items() if k!='role'}==
             {k:v for k,v in new.items() if k not in ('role','read')},'gauge frame and target contract unchanged')
    need(all(checker.dimf[op[3]]<=3 and op[1] not in gauge for op in model['ops'] if op[0]=='x'),
         'new original-X controls touch only low undeferred streams')
    need(all(checker.dimf[op[3]]>=20 for op in model['ops'] if
             op[1] in entrance or (op[0]=='a' and op[2] in entrance)),
         'banked high streams retain their entrance charts')

    # Explicit stage-private allocation of all nine physical replicas.
    allocations=sha256();bank_count=0;assignment_count=0
    for stage in range(3):
        for kind,roles,blocks,width in (('entrance',entrance,18,4),('undeferred',plain,3,24)):
            count=9*len(roles)
            need(count%blocks==0 and blocks*width==72,'integral complete bank partition')
            for index in range(count):
                replica,slot=divmod(index,len(roles));bank,block=divmod(index,blocks)
                allocations.update(('%d:%s:%d:%d:%d:%d\n'%(stage,kind,bank_count+bank,block,replica,roles[slot])).encode())
                assignment_count+=1
            bank_count+=count//blocks
    need(bank_count==141792 and assignment_count==3*9*len(live),'every physical stream in every stage assigned once')
    actual_W=bank_count+2*9*v
    W=Q(actual_W,9)
    H={int(r):n for r,n in profile['child_histogram'].items()}
    need(H.pop(60,None)==len(entrance),'exactly one rank60 exterior per independent entrance')
    mass=sum(r*n for r,n in H.items())
    need(W==Q(57824,3) and mass==1385840 and 72*W-mass==1936,'entire packed rank and stock inventory')
    need(profile['rank_per_vertex']-mass==60*len(entrance),'no internal or source/target child omitted')
    need(max(H)==22 and all(0<r<72 and n>0 for r,n in H.items()),'all remaining positive children paid')
    return dict(h=24,v=v,m=72,W_per_vertex=W,rank_per_vertex=mass,deficit_per_vertex=1936,
                child_histogram=H,maxchild=22,physical_roles_before_banks=len(live),
                bank=dict(physical_replicas=9,stages=3,entrance_rank=20,entrance_gauges=2200,
                          undeferred_physical_roles=15388,selected_width=4,selected_blocks=18,
                          undeferred_width=24,undeferred_blocks=3,selected_banks_per_stage=1100,
                          undeferred_banks_per_stage=46164,total_auxiliary_banks=bank_count,
                          literal_W=actual_W,normalized_W=W,moment_normalization_scale=3,
                          stream_assignments=assignment_count,allocation_sha256=allocations.hexdigest()),
                all_high_operations_identical=True,high_operations=len(high),
                high_word_sha256=sha256(json.dumps(high,separators=(',',':')).encode()).hexdigest(),
                original_gauges_and_targets_identical=True,source_controls_only_on_undeferred_streams=True,
                projector_checks=bank_projectors())
