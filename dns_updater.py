#!/usr/bin/env python

from libcloud.dns.providers import get_driver
from libcloud.dns.types import Provider
from urllib2 import urlopen
from IPy import IP
import argparse
import sys

username = ''
api_key = ''
ip_service = 'http://ipv4.dndy.me'
dns = None

def get_connection():
    driver = get_driver(Provider.RACKSPACE_US)
    conn = driver(username, api_key)
    return conn

def get_zone(name):
    zone = None
    zone_list = dns.list_zones()
    for cur_zone in zone_list:
        if cur_zone.domain == name:
            zone = dns.get_zone(cur_zone.id)
    
    if zone is None:
        print 'Zone not found: {}'.format(name)
        sys.exit(-1)
    else:
        return zone

def get_record(zone, name, record_type):
    record = None
    record_list = zone.list_records()
    for cur_record in record_list:
        if cur_record.name == name and cur_record.type == record_type:
            record = dns.get_record(zone.id, cur_record.id)
    
    if record is None:
        print 'Record not found: {}.{}'.format(name, zone.domain)
        sys.exit(-1)
    else:
        return record

def main():
    parser = argparse.ArgumentParser(description='Updates an existing DNS record on Rackspace DNS')
    parser.add_argument('fqdn', metavar='FQDN', help='Fully Qualified Domain Name')
    parser.add_argument('-p', metavar='N', type=int, default=2, dest='places',
                        help='Number of places that make up the domain name\n' \
                             '(ex. www.dandypandy.com == 2) Default=2')
    parser.add_argument('-n', '--dry-run', action='store_true', default=False, 
                        help="Don't actually make any changes")
    args = parser.parse_args()
    
    domain = '.'.join(args.fqdn.split('.')[-args.places:])
    host = '.'.join(args.fqdn.split('.')[:-args.places])

    ip_response = urlopen(ip_service)
    ip = ip_response.readline()
    
    if IP(ip).version() == 4:
        record_type = 'A'     # A record
    elif IP(ip).version() == 6:
        record_type = 'AAAA'     # AAAA record
    
    try:
        global dns
        dns = get_connection()
        zone = get_zone(domain)
        record = get_record(zone, host, record_type)
        
        if args.dry_run is True:
            print 'Not changing {} from {} to {}'.format(args.fqdn, record.data, ip)
        else:
            print 'Updating {} from {} to {}...'.format(args.fqdn, record.data, ip)
            dns.update_record(record, data=ip, extra={'ttl': 300})
            print 'Complete'
    except Exception as err:
        print err
        sys.exit(-1)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()
