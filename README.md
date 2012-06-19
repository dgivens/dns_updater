# dns_updater

A dynamic DNS type script that is written to update DNS records in the Rackspace DNS system.

This includes the script for telling you your current IP (to be hosted on something like a Cloud Server) and one that actually does the updating. 

## dns_updater.py

### Requires

- Python 2.7
- libcloud
- IPy

## get_ip.py

### Requires

- Flask

I've included a sample WSGI file for convenience. 
