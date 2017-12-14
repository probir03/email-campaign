from __init__ import app
import sys
from datetime import datetime
from EmailJob.email_manager import DripCampaign
start_time = datetime.now()
DripCampaign().run()
print datetime.now() - start_time
sys.exit()
