import sys
app_path = '/var/www/get_ip'
sys.path.insert(0, app_path)

from get_ip import app as application
