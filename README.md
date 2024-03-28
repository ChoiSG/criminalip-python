# CriminalIP-Python 

> 한국어 리드미: [README.kor.md](README.kor.md)

Unofficial python CLI for [CriminalIP.io](https://www.criminalip.io) API v1. 
Both CriminalIP (API) and this CLI is in early stage, so be aware. 

## Prerequisite 

Because this program uses CriminalIP's API, you need the API key from the platform. 
Visit [CriminalIP.io](https://www.criminalip.io) and register, use the "Beta Membership" for free 10,000 requests/month, then visit [mypage](https://www.criminalip.io/mypage/information), and retrieve the API key. 

## Installation 

**Linux** 
```
python3 -m pip install pipx 
pipx ensurepath
pipx install git+https://github.com/ChoiSG/criminalip-python.git 
```

**Windows** 
```
pip install pipx 
pipx ensurepath 
git clone https://github.com/ChoiSG/criminalip-python.git 
pipx install .
```

Run `cip init` with your API key after isntallation. 

**Uninstallation** 
```
pipx uninstall criminalip-python
```

## Usage 

### General 
```
$ cip -h 
Usage: cip [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  init          Initialize Criminal IP API key
  ip            Get information about an IP address
  request-scan  Request a domain scan to Criminal IP.
  scan-result   Get scan result for a domain
  search        Search for specific network service banner
  vpn           Check VPN/Proxy status of an IP address
```

### Init
CIP will create `<homdir>/.cip` directory and save the API key in plaintext in `api_key.txt` file. 
```
cip init <API-KEY>
```

### IP Search 
Search specific IP(s), find vpn/tor/proxy, find open ports, and find vulnerabilities 
```
cip ip -h 
cip ip <ip>
cip ip <ip> -o output.txt  
cip ip -f <file>
```

### Search 
Search CriminalIP.io for specific network service banner 
```
cip search <something>
cip search "hacked by" 

# Limit number of returned hosts  
cip search "hacked by" -l 5 

# Save the entire json to output file 
cip search "hacked by" -l 5 -o output.txt 
```

### VPN 
Search specific IP(s), and find about vpn/tor/proxy information 
```
cip vpn -h 
cip vpn <ip> 
cip vpn -f <file>
```

### Request-Scan 
Request CriminalIP.io to scan specific domain
```
cip request-scan <domain> 
cip request-scan blog.sunggwanchoi.com 
```

### Scan-Result 
Retrieve scanned result from requeste-scan 
```
cip scan-result <scanid-from-request-scan>
cip scan-result 2188259
cip scan-result 2188259 --progress 
```

### Special Thanks 
- BoanProject- Cho Jeongwon 