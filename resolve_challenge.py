'''
A simple script to solve hostinger's anti-bot javascript challenge.
'''

from hashlib import sha256
from curl_cffi import requests


class ResolveChallenge:
    def __init__(self, domain, _type):
        self.domain = domain
        self._type = _type
        self.request = requests.Session()
        self.request.impersonate = 'firefox'
        self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:157.0) Gecko/20100101 Firefox/157.0',
                        'Referer': domain, 'Origin' : domain}
        if _type != "hcdn":
            raise Exception("Only hcdn support is supported as of now.") # Skipping others like Cloudfare, and self-hosted javascript challenges for now.
        repr('<ResolveChallenge>')

    def get_challenge(self):
        res = (self.request.get(self.domain+"/hcdn-cgi/jschallenge", headers=self.headers).text
                    ).splitlines()[0] # because we assume that line will be 'cjs'
        challenge = res[int(res.find('=') + 3):int(res.find(';') - 1)]
        return challenge

    def compute_challenge(self):
        data = self.get_challenge()
        return sha256(data.encode()).hexdigest()

    def post_challenge(self):
        self.request.headers.update(
            {'Content-Type': 'application/x-www-form-urlencoded'}
        )
        res = self.request.post(self.domain + "/hcdn-cgi/jschallenge-validate", data=dict(challenge=self.compute_challenge()), headers=self.headers)
        if (res.status_code == 200):
            return dict(hcdn=res.cookies['hcdn'])


if __name__ == '__main__':
    DOMAIN = 'https://ocp.edu.in'
    
    challenge = ResolveChallenge(DOMAIN, 'hcdn')
    cookie = challenge.post_challenge()
    
    if cookie:
        print("SUCCESS! Challenge bypassed successfully.")
        print("Validated cookie: ", cookie)

# this proves that the cjs is hashed with sha256.
# print(sha256('WInbH7tR3gK3mr1npayR'.encode()).hexdigest() == 'bafd70c022055ee3926b279ddf06218e5ae3246f663f5ef814d86aaa09be690f')

# curl 'https://ocp.edu.in/hcdn-cgi/jschallenge'   --compressed   -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:157.0) Gecko/20100101 Firefox/157.0'   -H 'Accept: */*'   -H 'Accept-Language: en-US,en;q=0.9'   -H 'Accept-Encoding: gzip, deflate, br, zstd'   -H 'Referer: https://ocp.edu.in/'   -H 'Sec-GPC: 1'   -H 'Alt-Used: ocp.edu.in'   -H 'Connection: keep-alive'   -H 'Sec-Fetch-Dest: script'   -H 'Sec-Fetch-Mode: no-cors'   -H 'Sec-Fetch-Site: same-origin'   -H 'Pragma: no-cache'   -H 'Cache-Control: no-cache'   -H 'TE: trailers'
# get these
# <const cjs = 'WInbH7tR3gK3mr1npayR';
# const jsChallengeUrl = '/hcdn-cgi/jschallenge-validate';
# const uri = 'https://ocp.edu.in/';>
# ---
# Compute sha-256 hash of cjs and POST to:
# curl 'https://ocp.edu.in/hcdn-cgi/jschallenge-validate'   -X POST   -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:157.0) Gecko/20100101 Firefox/157.0'   -H 'Accept: */*'   -H 'Accept-Language: en-US,en;q=0.9'   -H 'Accept-Encoding: gzip, deflate, br, zstd'   -H 'Referer: https://ocp.edu.in/'   -H 'Content-Type: application/x-www-form-urlencoded'   -H 'Origin: https://ocp.edu.in'   -H 'Sec-GPC: 1'   -H 'Alt-Used: ocp.edu.in'   -H 'Connection: keep-alive'   -H 'Sec-Fetch-Dest: empty'   -H 'Sec-Fetch-Mode: cors'   -H 'Sec-Fetch-Site: same-origin'   -H 'Pragma: no-cache'   -H 'Cache-Control: no-cache'   -H 'TE: trailers'   --data-raw 'challenge=bafd70c022055ee3926b279ddf06218e5ae3246f663f5ef814d86aaa09be690f'
