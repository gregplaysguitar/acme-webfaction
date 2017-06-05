acme-webfaction
===

Issue and maintain letsencypt ssl certificates on webfaction using [acme.sh](https://github.com/Neilpang/acme.sh). This script uploads the certificates using the webfaction api, and should be triggered via an acme.sh reloadcmd.


 Installation
---

1. Install acme.sh:
   
   ```   
   curl https://get.acme.sh | sh 
   ```
   
2. Download `acme_webfaction.py` to your bin directory - i.e. `/home/USER/bin`. Make sure it's executable:

   ```   
   chmod +x ~/bin/acme_webfaction.py
   ```

Usage
---

1. Issue a certificate for your webfaction site as per the [acme.sh](https://github.com/Neilpang/acme.sh) documentation:

   ```
   acme.sh --issue -w /path/to/webroot -d example.com -d www.example.com
   ```
   
   Note you'll need to set up your site to serve the files in `/path/to/webroot/.well-known` at http://example.com/.well-known. You may need an apache alias for this:
   
   ```
   Alias /.well-known/ /path/to/webroot/.well-known/
   ```
   
2. Create an ssl certificate in the webfaction control panel, and add it to your site. See the [webfaction ssl documentation](https://docs.webfaction.com/user-guide/websites.html#add-a-certificate) for more information. You'll need to copy and paste the certificate details from the output of step 1.

3. Install the certificate using the `acme.sh --install-cert`, where 

   - `WF_SERVER` is your webfaction server name, i.e. Web486 (note, it must be title cased)
   - `WF_USER` and `WF_PASSWORD` is your webfaction control panel login
   - `WF_CERT_NAME` is the name of the certificate you created in step 2.

   ```
   acme.sh --install-cert -d example.com \
    --reloadcmd "WF_SERVER=WebXX WF_USER=user WF_PASSWORD=pass WF_CERT_NAME=certname acme_webfaction.py"
   ```
   
At this point you should have an acme.sh crontab entry which will renew the certificates automatically, and on renewal, trigger `acme_webfaction.py` to update the cert via the webfaction api.

You can test it's working by forcing a renewal - run the command from the crontab with `--force` appended, i.e. something like:

```
"/home/USER/.acme.sh"/acme.sh --cron --home "/home/USER/.acme.sh" --force
```

If everything is working correctly, you should see the certificates renewed and the message "Reload success".
