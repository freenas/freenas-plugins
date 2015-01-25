import hashlib
import os
import platform

sabnzbd_pbi_path = "/usr/pbi/sabnzbd-" + platform.machine()
sabnzbd_fcgi_pidfile = "/var/run/sabnzbd_fcgi_server.pid"
sabnzbd_control = "/usr/local/etc/rc.d/sabnzbd"
sabnzbd_icon = os.path.join(sabnzbd_pbi_path, "default.png")
sabnzbd_oauth_file = os.path.join(sabnzbd_pbi_path, ".oauth")


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


def get_sabnzbd_oauth_creds():
    f = open(sabnzbd_oauth_file)
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
