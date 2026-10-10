from pathlib import Path
import copy,sys,unittest
from test_estate_quality import evidence
from assemble_report import assemble
from validate_manifest import validate

class ReportContentControls(unittest.TestCase):
 def test_nested_resolved_review_is_reportable(self):
  data=evidence();data['review']['findings']=['Nested evidence'];data['review']['finding_dispositions']={'Nested evidence':{'status':'resolved','reason':'Current observed result agrees with the source'}}
  self.assertTrue(validate(data)['valid']);text=assemble(data)
  self.assertIn('Current observed result agrees with the source',text);self.assertIn('finding_dispositions',text)
 def test_literal_replacement_and_braces_remain_evidence(self):
  data=evidence();data['decision']['basis']=['SQL REPLACE preserved the row; diagnostic literal {{record}} and nested JSON {"a": {"b": 1}} are observed evidence']
  text=assemble(data);self.assertIn('SQL REPLACE',text);self.assertIn('{{record}}',text);self.assertIn('"b": 1',text)
 def test_actual_template_slots_remain_unfilled(self):
  for field in ('name','revision','included'):
   with self.subTest(field=field):
    data=evidence()
    if field=='included':data['scope'][field]=['  REPLACE  ']
    else:data['target'][field]='  REPLACE  '
    self.assertFalse(validate(data)['valid'])
    with self.assertRaises(ValueError):assemble(data)
 def test_evidence_quoting_placeholder_is_not_an_authoring_slot(self):
  data=evidence();data['claim_custody']['observed']=[{'id':'O-1','statement':'REPLACE','basis':'Observed literal source value in the candidate'}]
  self.assertIn('statement: REPLACE',assemble(data))
 def test_real_evidence_defect_still_prevents_report(self):
  data=evidence();data['executions'][0]['exit_code']=9
  with self.assertRaisesRegex(ValueError,'manifest invalid'):assemble(data)

if __name__=='__main__':unittest.main()
