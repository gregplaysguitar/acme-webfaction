#!/usr/bin/env python

"""
acme.sh "reloadcmd" to install the cert via the webfaction api.

Usage
---

Install acme.sh and put this file on your path.

Issue the cert using

    acme.sh --issue -d example.com ...

then install with

    acme.sh --install-cert -d example.com \
    --reloadcmd "WF_SERVER=WebXX WF_USER=user WF_PASSWORD=pass WF_CERT_NAME=certname acme_webfaction.py"

"""

import os
from xmlrpclib import ServerProxy, Fault


WF_API_URL = 'https://api.webfaction.com/'
WF_API_VERSION = 2
VERSION = (1, 0, 0)


def install_cert(cert_path, cert_key_path, ca_cert_path, wf_user, wf_password,
                 wf_server, wf_cert_name, verbosity=1):
    """Updates ssl certificate at wf_cert_name with the provided certificate
       details (cert_path, cert_key_path, ca_cert_path) using the webfaction
       api, for the given webfaction credentials (wf_user, wf_password,
       wf_server)
    """

    # connect to the Webfaction API
    try:
        server = ServerProxy(WF_API_URL)
        session_id, _ = server.login(wf_user, wf_password, wf_server,
                                     WF_API_VERSION)
    except Fault as e:
        print('Error connecting to Webfaction API. Error: {}'.format(e))
        return

    # read the cert files from paths provided by acme.sh
    with open(cert_path, 'r') as f:
        cert = f.read()
    with open(cert_key_path, 'r') as f:
        key = f.read()
    with open(ca_cert_path, 'r') as f:
        ca_cert = f.read()

    # Install the certificate to the web server through Webfaction's API
    server.update_certificate(session_id, wf_cert_name, cert, key, ca_cert)

    if verbosity:
        print('Updated certificate for {}.'.format(wf_cert_name))

    return True


if __name__ == '__main__':

    # user-provided config via envvar
    WF_USER = os.environ['WF_USER']
    WF_PASSWORD = os.environ['WF_PASSWORD']
    WF_SERVER = os.environ['WF_SERVER']
    WF_CERT_NAME = os.environ['WF_CERT_NAME']

    # acme.sh sets these envvars
    # see https://github.com/Neilpang/acme.sh/blob/d29aa43ba46d/acme.sh#L4198
    CERT_PATH = os.environ['CERT_PATH']
    CERT_KEY_PATH = os.environ['CERT_KEY_PATH']
    CA_CERT_PATH = os.environ['CA_CERT_PATH']

    install_cert(
        cert_path=CERT_PATH,
        cert_key_path=CERT_KEY_PATH,
        ca_cert_path=CA_CERT_PATH,
        wf_user=WF_USER,
        wf_password=WF_PASSWORD,
        wf_server=WF_SERVER,
        wf_cert_name=WF_CERT_NAME
    )
