"""
Main implementation of the CriminalIP API v1. 
"""

import os 
import sys
import requests
import logging 
import aiohttp
import asyncio 
from cip.helpers import * 

class CriminalIP:
    def __init__(self, key):
        self.api_key = key 
        self.base_url = "https://api.criminalip.io/v1"
        self.work_dir = os.path.join(os.path.expanduser("~"), ".cip")

    class ResultIP:
        def __init__(self, parent):
            self.parent = parent 

    def _request(self, endpoint, params, headers=None, files=None, method='GET'):
        """
        Make a request to the CriminalIP API. Return data in JSON format.

        :param function: String of API endpoint to send requests to
        :param params: Dictionary of HTTP parameters 
        :param headers: Dictionary of HTTP headers 
        :param method: String of HTTP method - GET, POST
        :return: JSON data from the API 
        """
        url = self.base_url + endpoint

        logging.info(f"[+] url: {url}")
        logging.info(f"[+] Params: {params}")
        logging.info(f"[+] Headers: {headers}") 
        logging.info(f"[+] Files: {files}")

        res = None 
        try:
            if method == 'GET':
                res = requests.get(url, params=params, headers=headers)
            elif method == 'POST':
                res = requests.post(url, params=params, headers=headers, files=files)
            else:
                raise Exception("[-] Invalid method: %s" % method)
        except Exception as e:
            raise Exception("[-] Request to %s failed" % endpoint)

        data = res.json()

        if int(data["status"]) != 200:
            cprint_error(data)
            sys.exit(1)

        return data

    # the cli will call this method like async_request("/ip/vpn", <filename>)
    async def async_request(self, endpoint, filename, parameters=None):
        """
        Sends asynchronous multiple requests to the API endpoint. 
        
        :param endpoint: String of API endpoint to send requests to
        :param filename: String of filename that contains IP addresses
        :return: List of dictionary of JSON results from the API
        """
        targets = [] 
        
        with open(filename, "r") as f:
            for line in f:
                targets.append(line.strip())
        
        tasks = [] 
        
        headers = {"x-api-key": self.api_key}
        async with aiohttp.ClientSession(headers=headers) as session:
            for target in targets:
                logging.info(f"[+] Async target: {target}")
                params = {"ip": target}
                url = self.base_url + endpoint 
                task = asyncio.ensure_future(self._async_request(session, url, params))
                tasks.append(task)
            
            datas = await asyncio.gather(*tasks)
            return datas

    async def _async_request(self, session, url, params=None, method='GET'):
        """
        Async version of _requests. This method gets called by async_request.

        :param session: aiohttp.ClientSession object
        :param url: String of API endpoint to send requests to
        :param params: Dictionary of HTTP parameters
        :param method: String of HTTP method - GET, POST
        :return: JSON data from the API
        """
        if method == 'GET':
            try:
                async with session.get(url, params=params) as response: 
                    data = await response.json()
                    return data
            except Exception as e:
                raise Exception(f"[-] Async: Request to {url} failed")

        elif method == 'POST':
            try:
                async with session.post(url, data=params) as response:
                    data = await response.json()
                    return data
            except Exception as e:
                raise Exception(f"[-] Async: Request to {url} failed")

        else:
            raise Exception(f"[-] Invalid method: {method}")

    def search(self, banner, offset):
        """
        Network Service banner search GET request to /banner/search.

        :param banner: String of network service banner
        :param offset: Integer of offset
        :return: JSON data from the API
        """

        headers = {"x-api-key": self.api_key}
        params = {"query": banner, "offset": offset}

        return self._request("/banner/search", params, headers, 'GET')

    def apiKeyCheck(self):
        """
        Sanity API key check against /user/me API endpoint 
        
        :return: JSON data from the API
        """
        headers = {"x-api-key": self.api_key}
        params = {}
        files = None

        return self._request("/user/me", params, headers, files,'POST')

    def vpn(self, ip):
        """
        VPN check GET request to /ip/vpn.

        :param ip: String of IP address
        :return: JSON data from the API
        """
        headers = {"x-api-key": self.api_key}
        params = {"ip": ip}

        return self._request("/ip/vpn", params, headers, 'GET')

    def request_scan(self, domain):
        """
        Request a domain scan. POST request to /domain/scan.

        :param domain: String of domain name
        :return: JSON data from the API
        """
        headers = {"x-api-key": self.api_key}
        files = {"query": (None, domain),}

        return self._request("/domain/scan", None, headers, files, 'POST')

    def scan_result(self, scan_id):
        """
        Retrieve domain scan results or progress/status. GET request to /domain/scan/{scan_id}.

        :param scan_id: String of scan ID
        :return: JSON data from the API
        """
        headers = {"x-api-key": self.api_key}

        return self._request("/domain/report"+ "/" + str(scan_id), None, headers, 'GET')

    def scan_progress(self, scan_id):
        """
        Get domain scan progress/status based on scan_id. GET request to /domain/scan/{scan_id}/progress.

        :param scan_id: String of scan ID
        :return: JSON data from the API
        """
        headers = {"x-api-key": self.api_key}

        return self._request("/domain/status"+ "/" + str(scan_id), None, headers, 'GET')

    def ip_data(self, ip, full=None):
        """
        Get information about an IP address. GET request to /ip/data.

        :param ip: String of IP address
        :param full: Boolean of whether to return full data or not
        :return: JSON data from the API
        """
        headers = {"x-api-key": self.api_key}
        
        if full is not None: 
            params = {"ip": ip, "full": full}
        else:
            params = {"ip": ip}

        logging.info(f"[+] url: {self.base_url}/ip/data")
        logging.info(f"[+] params: {params}")

        return self._request("/ip/data", params, headers, 'GET')