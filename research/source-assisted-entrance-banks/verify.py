#!/usr/bin/env python3
"""Verify PR193, replay the pinned PR187 bit word, then complete its entrance banks.

Requires Python 3.13+ and the pinned PR193 numpy/scipy dependencies.
Prepared by huxint with substantial OpenAI Codex assistance. Apache-2.0.
"""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse,copy,importlib.util,json,math,os,shutil,subprocess,sys,tempfile,time

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
REF=HERE/'references';CP=ROOT/'research/source-assisted-v4';BIT=REF/'pr187-package'
sys.dont_write_bytecode=True
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
sys.path.insert(0,str(HERE))
import banks,bank_arithmetic,receipts


def need(ok,message):
    if not ok:raise ValueError(message)


def digest(p):return sha256(p.read_bytes()).hexdigest()


def bit_input(name):
    prefix='research/source-assisted-bit-bootstrap/'
    if name.startswith(prefix):return BIT/name[len(prefix):]
    overlay=REF/'pr187-overlay'/name
    return overlay if overlay.is_file() else ROOT/name


def manifest():
    cm=json.loads((CP/'SOURCE.json').read_text())
    bm=json.loads((BIT/'SOURCE.json').read_text())
    root_files=set(cm['files'])|{'research/source-assisted-v4/SOURCE.json','research/source-assisted-v4/certificate.json'}
    root_files.update(n for n in bm['repository_files'] if bit_input(n)==ROOT/n)
    files={p.relative_to(HERE).as_posix():digest(p) for p in sorted(HERE.rglob('*')) if p.is_file()
           and '__pycache__' not in p.parts and p.name not in ('certificate.json','RESULTS.md','SOURCE.json')}
    # Retained prerequisite manifests/certificates are inputs, even though our
    # own generated outputs with the same filenames are excluded above.
    for p in REF.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:files[p.relative_to(HERE).as_posix()]=digest(p)
    return dict(complex_pr=193,complex_commit='187e1010ac8b259af8e9b5166f68b64bc27b4b47',
                bit_pr=187,bit_commit='201737a1ec4f936e166e2481fb9e88104cb2ccc7',
                bank_pr=186,bank_commit='166a34d75e853e933855f0f7e940fe77c4bb6b8d',
                package_files=dict(sorted(files.items())),root_files={n:digest(ROOT/n) for n in sorted(root_files)},
                assistance='huxint with substantial OpenAI Codex assistance')


def snapshot_bit(root):
    """Recreate the exact original PR187 tree without changing any of its pins."""
    m=json.loads((BIT/'SOURCE.json').read_text());root.mkdir(parents=True,exist_ok=True)
    for name,expected in m['repository_files'].items():
        source=bit_input(name);target=root/name
        need(target.resolve().is_relative_to(root.resolve()),'Relative prerequisite path')
        need(digest(source)==expected,'Exact PR187 prerequisite differs: '+name)
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    package=root/'research/source-assisted-bit-bootstrap';shutil.copytree(BIT,package,dirs_exist_ok=True)
    return package


def run(script,*args,cwd=ROOT):
    result=subprocess.run([sys.executable,'-B',str(script),*map(str,args)],cwd=cwd,
                          env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),text=True,capture_output=True)
    need(result.returncode==0,str(script)+' rejected:\n'+result.stdout[-8000:]+result.stderr[-8000:])
    return result.stdout


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def serial(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def finite_bridge_audit(complex_profile,bank,model,scalar_guard):
    """Check the same round-13 finite-bridge envelope for the literal replicas."""
    m=complex_profile['m'];half=m//2
    V=2**(m-1+(half-1)**2)*math.prod(2**(2*i)-1 for i in range(1,half))
    W=V*complex_profile['W_per_vertex'];rank=V*complex_profile['rank_per_vertex']
    r=max(map(int,complex_profile['child_histogram']))
    need(m<=72 and V<2**5184 and 2*r<m,'unchanged complex cover and child maximum')
    need(bank['bank']['literal_W']<10**7 and complex_profile['W_per_vertex']<10**7,'literal, not only normalized, role stocks')
    objects=9*(model['R']+model['v']+len(model['ops'])+len(model['roots']))+bank['bank']['stream_assignments']
    need(objects<2**40 and 9*scalar_guard['actual_F2_unit_shears']<2**4096,'finite literal program size and scalar bill')
    need(scalar_guard['expanded_readout_bits_per_coefficient']<2**80,'defining-integer coefficient bit bound')
    need(9*scalar_guard['local_scalar_group_upper']<2**4096,'full expanded bit response and inverse charges')
    G,E,C0=2**30000,2**100000,2**210000;B=rank+E
    need(W<2**5208 and rank<2**5215,'full complex group stock')
    need(64*(m+1)**3*(2**9300+1)*(W+1)**2<G,'dominating universal router')
    need(2*G*W*W+8*rank+4*W+4+32*m<E,'strict literal semantic charge')
    need(2*B*(m-r)-rank-E>0 and max(32*m*B*B,2*B+18)<C0,'semantic induction and common precision constants')
    need(Q(10**6)>Q(51*20161,25),'retained restored-row reserve')
    return dict(literal_program_objects=objects,literal_bit_roles=bank['bank']['literal_W'],
                physical_replicas=9,replicated_unit_shears=9*scalar_guard['actual_F2_unit_shears'],
                replicated_expanded_scalar_bound=9*scalar_guard['local_scalar_group_upper'],
                coefficient_bits_below_2pow80=True,full_group_stock_checked=True,
                router_G_exponent=30000,semantic_E_exponent=100000,precision_C0_exponent=210000,
                row_coefficient=20161,row_degree=10**6,all_finite_bridge_inequalities_strict=True)


def verify():
    need(not sys.flags.optimize,'Run without -O')
    need(sys.version_info>=(3,13),'The pinned PR193 gzip receipts require Python 3.13 or newer')
    before=manifest();need(before==json.loads((HERE/'SOURCE.json').read_text()),'Source closure changed')
    print('Rebuilding PR193 source-assisted complex flow, exact lift and contract...',flush=True)
    need(not (CP/'.work').exists(),'The parent complex work directory is already in use')
    run(CP/'verify.py')
    complex_result=json.loads((CP/'certificate.json').read_text())
    need(complex_result['binding_supplier']=='bit','Pinned source-assisted complex supplier')
    with tempfile.TemporaryDirectory(prefix='source-assisted-bank-') as temporary:
        bit_root=Path(temporary)/'pr187';bit_package=snapshot_bit(bit_root);out=bit_root/'build/emitted'
        print('Replaying every pinned PR187 source, target and dirty column and every used prime frame...',flush=True)
        run(bit_package/'verify.py','--full','--output-dir',out,cwd=bit_root)
        load=lambda name:json.loads((out/name).read_text())
        model=load('emitted-word.json');physical=load('emitted-physical.json');scalar=load('scalar-cost.json');audit=load('independent-all-columns.json')
        audit.pop('elapsed_seconds',None)
        guard=receipts.validate_receipts(physical,scalar,audit)
        need(digest(out/'emitted-word.json')==physical['word_sha256'],'actual emitted word binding')
        print('Checking unchanged high streams, all bank assignments, full swap columns and inverse controls...',flush=True)
        packed=banks.certify(model,physical,bit_root)
        interval=module('bank_interval',bit_root/'research/paired-cube-local-bit-168/arithmetic/interval_moment.py')
        bank_arithmetic.bind(interval)
        bit=bank_arithmetic.certify(packed)
        independent_gap=bank_arithmetic.independent_bank_moment(packed,bit)
        finite=finite_bridge_audit(complex_result['complex_profile'],packed,model,guard)
        aggregate=module('source_assisted_bank_assembly',ROOT/'research/source-assisted/global/assemble_profiles.py')
        aggregate.SELECT_GRID=10**18
        c=dict(counts=aggregate.normalize(complex_result['complex_profile']),saving=Q(complex_result['complex_saving']))
        b=dict(counts=aggregate.normalize(packed),saving=bit['coarse_saving'],effective_saving=bit['ordinary_saving'])
        assembled=aggregate.assemble(c,b,ROOT,ROOT/'research/source-assisted/global/FINITE_BRIDGE.txt')
        need(assembled['kappa']>Q(complex_result['kappa']),'complete assembled improvement over PR193')
        controls=[]
        def reject(name,call):
            try:call()
            except (ValueError,AssertionError):controls.append(name)
            else:raise ValueError('Adverse control accepted: '+name)
        engine=module('bank_balanced_assembly',ROOT/'scripts/paired_cube_assembly.py')
        params=assembled['assembly']['parameters']
        reject('next final grid point',lambda:engine.assembly(params['a_bit'],params['a_complex'],assembled['finite_bridge'],
               assembled['kappa']+Q(1,10**18),eta=params['eta'],beta=params['beta']))
        wrong=copy.deepcopy(physical);wrong['child_histogram']['60']-=1
        reject('missing paid entrance',lambda:banks.certify(model,wrong,bit_root))
        wrong_model=copy.deepcopy(model);wrong_model['gauges'][0]['dim']-=1
        reject('changed physical gauge',lambda:banks.certify(wrong_model,physical,bit_root))
        need(manifest()==before,'Sources changed during complete verification')
        return serial(dict(status='PASS conditional source-assisted entrance-bank composition',
            kappa=assembled['kappa'],parent_kappa=complex_result['kappa'],
            complex_saving=complex_result['complex_saving'],complex_certificate_sha256=digest(CP/'certificate.json'),
            complex_scope=complex_result['scope'],complex_contract_checks=complex_result['complex_profile']['contract_checks'],
            emitted_word_sha256=physical['word_sha256'],bit_physical=physical,bit_all_columns=audit,
            bit_scalar_guard=guard,prime_coverage=load('prime-coverage.json'),bank_profile=packed,
            bit_moment=bit,independent_paid_moment_gap=independent_gap,finite_envelope=finite,
            assembly=assembled,controls=controls,source_manifest_sha256=digest(HERE/'SOURCE.json'),
            scope='PR193 exact local complex lift and contract, PR187 globally emitted F2 payload word and integer inverse bounds, and PR186 completed-bank endpoint. Inherited all-size, weighted-chart, row, prime, precision, analytic and fixed-tape interfaces remain conditional.'))


def report(x):
    tick=Q(x['kappa'])*10**18;need(tick.denominator==1,'displayed exact kappa')
    value='0.'+str(tick.numerator).zfill(18);p=x['bank_profile']
    return ('# Checked result\n\nConditional **κ = '+x['kappa']+' = '+value+'**.\n\n'
            'This is %.6f%% above the pinned PR193 value.\n\n'%(float(100*(Q(x['kappa'])/Q(x['parent_kappa'])-1)))+
            'The bit supplier binds. Its checked coarse saving is '+x['bit_moment']['coarse_saving']+'.\n\n'
            'The normalized bit stock is W='+str(p['W_per_vertex'])+', rank='+str(p['rank_per_vertex'])+', deficit=1936. '
            'Nine literal physical replicas have '+str(p['bank']['literal_W'])+' total roles. '
            'All 2,200 independent rank-20 gauge streams are banked; the 1,760 rank-21 recipients remain internal aliases.\n\n'
            'Both prerequisite constructions are replayed. All bit columns, high-stream identities, bank address maps and inverses, '
            'two paid-moment engines, the full finite envelope and all 47 strict assembly constraints pass.\n\n'
            'The complex branch retains PR193\'s exact local-flow scope: it does not export a globally renumbered complex transcript '
            'or a full Clifford/router replay. All inherited uniform compiler and analytic contracts remain conditional.\n')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args();start=time.monotonic()
    if args.write:(HERE/'SOURCE.json').write_text(json.dumps(manifest(),sort_keys=True,indent=2)+'\n')
    result=verify();text=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.write:
        (HERE/'certificate.json').write_text(text);(HERE/'RESULTS.md').write_text(report(result))
    else:
        need(text==(HERE/'certificate.json').read_text(),'Canonical complete certificate differs')
        need(report(result)==(HERE/'RESULTS.md').read_text(),'Displayed result differs')
    print('PASS bank composition kappa='+result['kappa']+'; complete prerequisites, bank contracts and exact assembly (%.1fs)'%(time.monotonic()-start),flush=True)


if __name__=='__main__':main()
