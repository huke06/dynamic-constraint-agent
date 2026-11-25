"""SDK transport. Credentials are never serialized into experiment artifacts."""
import os,sys,urllib.request
from pathlib import Path
import httpx
from openai import OpenAI
class DeepSeek:
 def __init__(self,model='deepseek-flash',timeout=60):
  secret=os.getenv('DEEPSEEK_API_KEY')
  if not secret:
   # Local compatibility only; portable reproductions use the environment variable.
   sys.path.insert(0,os.getenv('DCA_LEGACY_CREDENTIAL_ROOT','D:/experimentn'))
   from probe_deepseek import credential
   secret=credential()
  self.secret=secret;self.model=model
  self.client=OpenAI(api_key=secret,base_url='https://api.deepseek.com',max_retries=0,timeout=timeout,http_client=httpx.Client(proxy=urllib.request.getproxies().get('https'),timeout=timeout))
