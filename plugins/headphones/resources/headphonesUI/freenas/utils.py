import hashlib
import os
import platform

headphones_pbi_path = "/usr/pbi/headphones-" + platform.machine()
headphones_fcgi_pidfile = "/var/run/headphones_fcgi_server.pid"
headphones_control = "/usr/local/etc/rc.d/headphones"
headphones_icon = os.path.join(headphones_pbi_path, "default.png")
headphones_oauth_file = os.path.join(headphones_pbi_path, ".oauth")


def get_rpc_url(request):
    addr = request.META.get("SERVER_ADDR")
    # IPv6
    if ':' in addr:
        addr = '[%s]' % addr
    return 'http%s://%s:%s/plugins/json-rpc/v1/' % (
        's' if request.is_secure() else '',
        addr,
        request.META.get("SERVER_PORT"),
    )


def get_headphones_oauth_creds():
    f = open(headphones_oauth_file)
    lines = f.readlines()
    f.close()

    key = secret = None
    for l in lines:
        l = l.strip()

        if l.startswith("key"):
            pair = l.split("=")
            if len(pair) > 1:
                key = pair[1].strip()

        elif l.startswith("secret"):
            pair = l.split("=")
            if len(pair) > 1:
                secret = pair[1].strip()

    return key, secret
