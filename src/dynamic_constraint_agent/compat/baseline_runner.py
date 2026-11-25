"""Minimal compatibility adapter for the unmodified round-16 request logger."""
import sys,json,re,os
from pathlib import Path
REPO=Path(os.getenv('DCA_TAU2_ROOT','D:/experimentn/tau2-official'));DATA=REPO/'data/tau2/domains/retail'
os.environ['TAU2_DATA_DIR']=str(REPO/'data');os.environ['LITELLM_LOCAL_MODEL_COST_MAP']='True'
sys.path.insert(0,str(REPO/'src'));sys.path.insert(0,'D:/experimentn/exp2layer')
from api_client import DeepSeek
from tau2.domains.retail.data_model import RetailDB
from tau2.domains.retail.tools import RetailTools
MODEL='deepseek-flash'
def parse(s):
 s=s.strip()
 if s.startswith('```'):s=re.sub(r'^```(?:json)?\s*|\s*```$','',s)
 return json.loads(s)
