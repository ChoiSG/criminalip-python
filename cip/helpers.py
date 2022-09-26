"""
Simple helper module for various utils.
"""

import os 
import click 

def create_work_dir():
    """
    Create a working directory named "/.cip" on running user's home directory
    This directory will store necessary files and by default be the output directory.  

    :return bool: True if directory is created, False if directory already exists
    """
    home = os.path.expanduser("~")
    work_dir = os.path.join(home, ".cip")
    
    if os.path.exists(work_dir):
        return work_dir 
    else:
        os.mkdir(work_dir)
        return work_dir

def get_api_key():
    """
    Get API key from file

    :return str: API key
    """

    try:
        work_dir = create_work_dir()
    except Exception as e:
        print("[-] Work directory doesn't exist. Run 'python(3) cip.py init <apikey>' to create one.")
        return None

    try:
        with open(os.path.join(work_dir,"api_key.txt"),"r") as f:
            key = f.read().strip()
    except Exception as e:
        raise Exception("[-] API key file doesn't exist. Run 'python(3) cip.py init <apikey>' to create one.")

    return key

def print_apikeycheck(data):
    """
    Parse adn print API key check data from /user/me 
    """

    if data['status'] != 200:
        cprint_error(f"[-] API key check failed.")
        return

    cprint_debug("[+] API key check successful.\n")
    cprint("EMAIL", data['data']['email'])
    cprint("NAME", data['data']['name'])
    cprint("LAST_ACCESS_DATE", data['data']['last_access_date'])
    cprint("MAX_SEARCH", data['data']['max_search'])
    print()

def print_request_scan(data, domain):
    """
    Parse and print data from request_scan
    """
    
    if data['status'] != 200:
        cprint_error(f"[-] Domain scan request failed for {domain}")
        return 
        
    cprint_debug(f"[+] Successfully requested domain scan for {domain}")
    cprint_debug(f"[+] Scan ID: {data['data']['scan_id']}\n")
    cprint_debug(f"[+] Wait for couple of minutes, and then run scan-result with scan_id for progress and results.")

def print_ip(data):
    """
    Parse and print IP data - Sumamrized version of ports and vulnerabilities 
    """
    
    # Multiple IPs 
    if isinstance(data, list):
        for item in data:
            try:
                cprint("IP", item['ip'])

                # Tags for type of IP address 
                for key,value in item['tags'].items():
                    if value == True:
                        cprint(key, value, 2)

                # Ports  
                ports = item['port']['data']
                ports_list = [] 
                
                for port in ports: 
                    if port['open_port_no'] not in ports_list: 
                        cprint("Port", port['open_port_no'], 2)
                        cprint("Service", port['app_name'] + " " + port['app_version'], 4)
                        cprint("Is_Vuln", port['is_vulnerability'], 4)
                        cprint("confirmed_time", port['confirmed_time'], 4)
                        ports_list.append(port['open_port_no'])

                print() 

                # Vulns 
                vulns = item['vulnerability']['data'] 

                for vuln in vulns: 
                    if (vuln['cvssv3_score'] > 7.0):
                        cprint("CVE", vuln['cve_id'], 2)
                        cprint("CVSSv3", vuln['cvssv3_score'], 4)
                        cprint("Port", "TCP/" + str(vuln['open_port_no_list']['TCP']) + " UDP/" + str(vuln['open_port_no_list']['UDP']), 4)
                        cprint("Service", vuln['app_name'] + " " + vuln['app_version'],4 )
                        
            except Exception as e:
                print(f"[-] Error printing IP data {str(e)}")
        return

    # Single IP 
    if isinstance(data, dict):
        try:
            cprint("IP", data['ip'])

            # Tags for type of IP address 
            for key,value in data['tags'].items():
                if value == True:
                    cprint(key, value, 2)

            # Ports  
            ports = data['port']['data']
            ports_list = [] 
            
            for port in ports: 
                if port['open_port_no'] not in ports_list: 
                    cprint("Port", port['open_port_no'], 2)
                    cprint("Service", port['app_name'] + " " + port['app_version'], 4)
                    cprint("Is_Vuln", port['is_vulnerability'], 4)
                    cprint("confirmed_time", port['confirmed_time'], 4)
                    ports_list.append(port['open_port_no'])

            print() 

            # Vulns 
            vulns = data['vulnerability']['data'] 

            for vuln in vulns: 
                if (vuln['cvssv3_score'] > 7.0):
                    cprint("CVE", vuln['cve_id'], 2)
                    cprint("CVSSv3", vuln['cvssv3_score'], 4)
                    cprint("Port", "TCP/" + str(vuln['open_port_no_list']['TCP']) + " UDP/" + str(vuln['open_port_no_list']['UDP']), 4)
                    cprint("Service", vuln['app_name'] + " " + vuln['app_version'],4 )
                    
        except Exception as e:
            print(f"[-] Error printing IP data {str(e)}")

def print_vpn(data):
    """
    Parse data for VPN 
    """

    if isinstance(data, list):
        for item in data: 
            try:
                cprint("IP", item["ip"])
                if(item["is_vpn"] == True):
                    # TODO: Fix the hardcoded [0] after data. TBH I only saw 1 item data list so I guess no problem? not sure.
                    cprint("IS_VPN", item["is_vpn"])
                    cprint("VPN_NAME", item["vpn_info"]["vpn"]["data"][0]["vpn_name"])
                elif(item['is_tor'] == True):
                    cprint("IS_TOR", item['is_tor'])
                elif(item['is_proxy'] == True):
                    cprint("IS_PROXY", item['is_proxy'])
                else:
                    cprint_error('[-] IP is not a VPN, Tor, or Proxy') 
                click.echo()
            except Exception as e:
                click.echo() 
                continue 

    else:
        try:
            cprint("IP", data["ip"])
            if(data["is_vpn"] == True):
                # TODO: Fix the hardcoded [0] after data. TBH I only saw 1 item data list so I guess no problem? not sure.
                cprint("IS_VPN", data["is_vpn"])
                cprint("VPN_NAME", data["vpn_info"]["vpn"]["data"][0]["vpn_name"])
            elif(data['is_tor'] == True):
                cprint("IS_TOR", data['is_tor'])
            elif(data['is_proxy'] == True):
                cprint("IS_PROXY", data['is_proxy'])
            else:
                cprint_error('[-] IP is not a VPN, Tor, or Proxy') 
            click.echo()
        except Exception as e:
            print(f"[-] Error: {str(e)}")
            return 

def print_search(data):
    """
    Parse data for search 
    """
    for item in data:
        try:
            cprint("IP", item["ip_address"])
            cprint("Port", item["open_port_no"], 2)
            cprint("Country", item["country"], 2)
            cprint("Service", item["product"] + " " + item["product_version"], 2)
            cprint("Score", item["score"], 2)
            cprint("Scan Time", item["scan_dtime"], 2)

            print() 

        except Exception as e:
            cprint_error(f"[-] Error: {str(e)}")
            return 

def cprint(key, value, padding=0):
    click.echo(' ' * padding + click.style(f'{key}:', fg='green') + click.style(f'{value}', fg='blue'))

def cprint_debug(string, padding=0):
    click.echo(' ' * padding + click.style(f'{string}', fg='green'))

def cprint_error(string, padding=0):
    click.echo(' ' * padding + click.style(f'{string}', fg='red'))