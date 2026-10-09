"""PR187 scalar/column receipt validator, retained without mathematical edits.
Rohan Arun, with OpenAI Codex assistance; Apache-2.0.
See references/pr187-package/NOTICE.md and the pinned original certificate.py.
"""
def validate_receipts(physical,sc,aud):
 assert physical['status']==aud['status']=='PASS'
 assert physical['word_sha256']==aud['word_sha256']
 assert physical['operations']==sc['elementary_forward_xors']==sc['elementary_inverse_xors']==aud['forward_auxiliary_operations']
 assert physical['source_controls']==sc['original_X_controls']==aud['original_source_control_operations']
 assert physical['physical_R']==aud['physical_auxiliary_roles']==aud['dirty_columns']
 assert physical['W_per_vertex']==aud['total_independent_columns']
 assert aud['source_columns']==aud['target_columns']==1760
 assert physical['W_per_vertex']==physical['physical_R']+aud['source_columns']+aud['target_columns']
 assert all(aud[k]['exact_map'] and all(aud[k][x]==0 for x in ('bad_source_rows','bad_target_rows','bad_dirty_rows')) for k in ('baseline','full_time_reverse'))
 assert all(not r['exact_map'] for r in aud['negative_controls'].values())
 assert aud['integer_lift']['exact_unit_shear_inverse_certified']
 assert not aud['integer_lift']['integer_decoder_identity_claimed']
 assert sc['payload_coefficient_alphabet']==[0,1] and sc['maximum_absolute_payload_shear_coefficient']==1
 parts=('elementary_forward_xors','elementary_inverse_xors','old_value_response_xors','root_read_xors','partner_mix_forward_inverse_xors','partner_delivery_xors')
 assert sum(sc[k] for k in parts)==sc['total_scalar_xors']==aud['literal_elementary_operations']
 assert sc['old_value_response_xors']==sc['nongauged_response_xors']+sc['gauged_response_xors']
 R=aud['logical_auxiliary_roles'];v=aud['source_columns'];M=sc['elementary_forward_xors'];h=physical['m']//3
 # Retained expanded-readout bound. With M unit updates, every defining integer
 # coefficient has magnitude <=2^M; all R*v old readouts receive M+16 bits.
 guard=4*(M+v)+10*v+4*h*v+4*h*h+8*h+8+2*h+8*R*v*(M+16)+32*v
 assert sc['total_scalar_xors']<guard
 majorants=sc['integer_non_cancelling_majorants']
 assert all(type(majorants[k])is int and 0<majorants[k]<=2**M for k in ('maximum_aux_old_read_row_l1','maximum_X_adjoint_row_l1','maximum_forward_and_inverse_row_l1'))
 assert majorants['sum_aux_old_read_row_l1']<=R*v*2**M
 return dict(local_scalar_group_upper=guard,actual_F2_unit_shears=sc['total_scalar_xors'],
   expanded_readout_bits_per_coefficient=M+16,logical_scalar_reserve=R,forward_unit_updates=M,
   integer_majorants=majorants,
   scope='Fixed local bit-word/scalar toll in the uniform recurrence. Complex precision/group bounds remain unchanged; no integer decoder identity is asserted.')
