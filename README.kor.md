# CriminalIP-Python 

[AI Spera](https://www.criminalip.io/about/aispera)사가 개발하고 운영하는 [CriminalIP.io](https://www.criminalip.io) 플랫폼의 비공식 파이썬 CLI 프로그램입니다. 
CriminalIP의 API와 이 CLI 프로그램 모두 개발 초기 단계이기 때문에 이를 유의하시기 바랍니다. 

## 전제 조건 

해당 프로그램은 CriminalIP 플랫폼의 API를 이용하기 때문에 API 키가 필요합니다. 
[CriminalIP](https://www.criminalip.io) 플랫폼을 방문해 가입한 뒤, Beta Membership 을 공짜로 가입 (09/25/2022 기준) 한 뒤, [마이페이지](https://www.criminalip.io/mypage/information) 에서 API키를 받습니다. 

## 설치 

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

설치 후 `cip init` 을 이용해 API 키를 등록합니다.

**Uninstallation** 
```
pipx uninstall criminalip-python
```

## 사용법 

### 일반 
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

### Init - API 초기 세팅
해당 유저의 홈 디렉토리에 `<homedir>/.cip` 디렉토리를 생성한 후 `api_key.txt` 파일에 API 키를 평문으로 저장합니다. 
해당 프로그램을 사용하기 위해서 `init` 은 꼭 실행해야합니다. 
```
cip init <API-KEY>
```

### IP Search 
특정 아이피주소(들)을 검색해 vpn/tor/proxy 여부, 오픈 포트, 그리고 취약점들에 대해서 알아봅니다. 
```
cip ip -h 
cip ip <ip>
cip ip <ip> -o output.txt  
cip ip -f <file>
```

### Search 
특정 네트워크 서비스 배너들을 검색합니다. 
```
cip search <something>
cip search "hacked by" 

# Limit number of returned hosts  
cip search "hacked by" -l 5 

# Save the entire json to output file 
cip search "hacked by" -l 5 -o output.txt 
```

### VPN 
특정 아이피주소(들)을 검색해 vpn/tor/proxy 여부에 대해서 자세히 알아봅니다. 
```
cip vpn -h 
cip vpn <ip> 
cip vpn -f <file>
```

### Request-Scan 
CriminalIP 에게 특정 도메인 스캔을 요청합니다. 
```
cip request-scan <domain> 
cip request-scan blog.sunggwanchoi.com 
```

### Scan-Result 
`Request-Scan` 에서 요청한 도메인 스캔 결과값을 불러옵니다. 
```
cip scan-result <scanid-from-request-scan>
cip scan-result 2188259
cip scan-result 2188259 --progress 
```

## Special Thanks 
- [보안프로젝트 조정원 대표님](https://www.youtube.com/user/ngnicky1209)