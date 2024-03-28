"""
Main CLI module for CriminalIP-python. 
"""

import asyncio 
import asyncclick as click
import json
import os 
import logging 
import warnings

from cip.CriminalIP import * 

from rich import print_json
from functools import update_wrapper
from cip.helpers import * 

##############################################################
# __main__ section for actual CLI 
##############################################################
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    pass 

def print_help():
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()

@main.command() 
@click.argument('key', metavar='API_KEY', required=True)
@click.option('--verbose', '-v', is_flag=True, default=False, help="Enable verbose output")
def init(key, verbose):
    """ Initialize Criminal IP API key. Run this first."""
    if (verbose): logging.basicConfig(level=logging.INFO)

    api = CriminalIP(key)

    home = os.path.expanduser("~")
    work_dir = os.path.join(home, ".cip")
    
    try:
        os.mkdir(work_dir)
        cprint_debug(f"[+] Work directory created at {work_dir}")
    except Exception as e:
        cprint_debug("[+] Work directory already exists. Skipping...")
    
    data = api.apiKeyCheck() 

    if data is None: 
        raise click.ClickException("[-] Invalid API key. Please check your key and try again.")

    api.api_key = key
    cprint_debug("[+] API key is valid")
    print_apikeycheck(data=data)

    with open(os.path.join(work_dir, "api_key.txt"), "w") as f:
        f.write(key)
        cprint_debug(f"[+] API key stored in {os.path.join(work_dir, 'api_key.txt')}")

@main.command
@click.argument('scan_id', metavar='SCAN_ID', required=True)
@click.option('--progress', '-p', is_flag=True, help="Show scan progress of the scan_id")
@click.option('--output', '-o', default=None, help="Output filename")
def scan_result(scan_id, progress, output):
    """
    Get scan result for a domain
    """
    api = CriminalIP(get_api_key())
    
    if progress:
        data = api.scan_progress(scan_id)
    else:
        data = api.scan_result(scan_id)

    if output is not None:
        with open(output, "w") as f:
            f.write(json.dumps(data))
            cprint_debug(f"[+] Output written to {output}")
    
    else:
        print_json(data=data) 

@main.command 
@click.argument('domain', metavar='DOMAIN', required=True)
@click.option('--verbose', '-v', is_flag=True, help='Verbose mode')
def request_scan(domain, verbose):
    """ Request a domain scan to Criminal IP"""
    if (verbose): logging.basicConfig(level=logging.INFO)

    api = CriminalIP(get_api_key())
    data = api.request_scan(domain)
    print_request_scan(data, domain)

@main.command()
@click.argument('ip', metavar='IP_ADDRESS', required=False)
@click.option('--filename', '-f', default=None, help='Input file with IP addresses')
@click.option('--full', is_flag=True, default=False, help="Show full data")
@click.option('--output', '-o', default=None, help="Output filename")
@click.option('--verbose', '-v', is_flag=True, default=False, help="Verbose mode")
async def ip(ip, filename, full, output, verbose):
    """ Get information about an IP address """
    if (verbose): logging.basicConfig(level=logging.INFO)

    api = CriminalIP(get_api_key())

    if filename is None and ip is None: 
        print_help()

    if filename is not None:
        logging.info(f"[+] Using filename {filename}")
        data = await api.async_request("/ip/data", filename)
    else:
        logging.info(f"[+] Using IP address {ip}")

        # Currently CIP API has a bug where full=<any-value> will be interpreted as full=true. 
        if full == False:
            data = api.ip_data(ip)
        else:
            data = api.ip_data(ip, 'true')

    if data is None:
        raise click.ClickException("[-] Invalid IP address. Please try again.")
    
    # Print data 
    logging.info("[DEBUG] Printing IP data")
    if (full):
        print_json(data=data)
    else:
        print_ip(data)
    
    if output is not None:
        with open(output, "w") as f:
            json.dump(data, f, indent=4)
            cprint_debug(f"\n[+] Output saved to {output}")

@main.command() 
@click.argument('search', metavar='SEARCH', required=True)
@click.option('--limit', '-l', default=100, help="Limit the number of results. CriminalIP's default max is 100.")
@click.option('--offset', '-s', default=0, help="Offset of the CIP database. Default is 0.")
@click.option('--output', '-o', default=None, help="Output filename")
@click.option('--verbose', '-v', is_flag=True, help="Verbose mode")
def search(search, limit, offset, output, verbose):
    """
    Search for specific network service banner 
    """
    if verbose: logging.basicConfig(level=logging.INFO)

    api = CriminalIP(get_api_key())
    cprint_debug(f"[+] Searching for {search}, this is going to take some time...")

    try:
        logging.info(f"[+] Searching for {search}")
        data = api.search(search, offset)
    except Exception as e:
        raise click.ClickException(str(e))

    if data is None: 
        raise click.ClickException("[-] No results found. Please try again.")

    if limit < 100: 
        data = data["data"]["result"][0:limit]
    else:
        print("[-] Maximum limit is 100. Setting limit to 100.")

    # Also, take limit into account and make the limit to default of 20 
    print()
    print_search(data=data)
    
    if output is not None:
        with open(output, "w") as f:
            json.dump(data, f, indent=4)
            cprint_debug(f"[+] Output saved to {output}")
        
@main.command()
@click.argument('ip', metavar='IP_ADDRESS', required=False)
@click.option('--filename', '-f', default=None, help='File containing IP addresses')
@click.option('--output', '-o', default=None, help="Output file name")
@click.option('--verbose', '-v', is_flag=True, help="Verbose mode")
@click.option('--full', is_flag=True, default=False, help="Show full data")
async def vpn(ip, filename, output, full, verbose):
    """ Check VPN/Proxy status of an IP address"""
    if verbose: logging.basicConfig(level=logging.INFO)

    try:
        api = CriminalIP(get_api_key())
    except Exception as e:
        raise click.ClickException(str(e))

    # Multiple targets - Using asyncio 
    if filename is not None:
        logging.info(f"[+] Using filename: {filename}")
        data = await api.async_request("/ip/vpn", filename)    

    # Single target 
    else:
        logging.info(f"[+] Checking {ip}")
        data = api.vpn(ip)

    # Print simplified output 
    if data is None:
        raise click.ClickException("[-] No results found. Please try again.")

    if full == True: 
        print_json(data=data)
    else:
        print_vpn(data)

    # Save to file if output is specified
    if output is not None:
        with open(output, "w") as f:
            json.dump(data, f, indent=4)
            click.echo(click.style(f"\n[+] Search results written to {output}", fg="green"))

if __name__ == '__main__':
    main(_anyio_backend="asyncio")