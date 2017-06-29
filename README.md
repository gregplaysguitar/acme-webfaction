acme-webfaction
===

This script enables you to automatically issue and maintain letsencypt ssl certificates on webfaction using [acme.sh][], without having to perform manual renewals.

Requires [acme.sh][] and a [webfaction][] account.

See <https://gregbrown.co/code/letsencrypt-webfaction-automated> for more information.

#### How does it work?

Certificates are issued, installed and renewed using [acme.sh][]. Whenever a certificate is renewed, this script uploads it to the webfaction API via the [acme.sh][] `--reloadcmd` argument.

Installation
---

1. Install acme.sh:
   
   ```   
   curl https://get.acme.sh | sh 
   ```
   
2. Download `acme_webfaction.py` from <https://github.com/gregplaysguitar/acme-webfaction> and move it into your bin directory - i.e. `/home/USER/bin`. Make sure it's executable:

   ```
   wget https://raw.githubusercontent.com/gregplaysguitar/acme-webfaction/master/acme_webfaction.py
   cp ./acme_webfaction.py ~/bin/
   chmod +x ~/bin/acme_webfaction.py
   ```

Usage
---

1. Issue a certificate for your webfaction site as per the [acme.sh][] documentation:

   ```
   acme.sh --issue -w /path/to/webroot -d example.com -d www.example.com
   ```
   
   Note you'll need to set up your site to serve the files in `/path/to/webroot/.well-known` at http://example.com/.well-known. If you're working with a static or php site, you can just add your actual webroot here. For sites without a webroot, i.e. django or rails, use a temp directory as your webroot and add an alias in `/home/USER/webapps/APPNAME/apache2/conf/httpd.conf`:
   
   ```
   Alias /.well-known/ /home/USER/temp/.well-known/
   ```
   
2. Create an ssl certificate in the webfaction control panel, and add it to your site. See the [webfaction ssl documentation](https://docs.webfaction.com/user-guide/websites.html#add-a-certificate) for more information. You'll need to copy and paste the certificate details from the output of step 1

3. Install the certificate using the `acme.sh --install-cert`, where 

   - `WF_SERVER` is your webfaction server name, i.e. Web486 (note, it must be title cased)
   - `WF_USER` and `WF_PASSWORD` is your webfaction control panel login
   - `WF_CERT_NAME` is the name of the certificate you created in step 2

   ```
   acme.sh --install-cert -d example.com -d www.example.com \
    --reloadcmd "WF_SERVER=WebXX WF_USER=user WF_PASSWORD=pass WF_CERT_NAME=certname acme_webfaction.py"
   ```

#### Testing it out

At this point you should have an [acme.sh][] crontab entry which will renew the certificates automatically, and on renewal, trigger `acme_webfaction.py` to update the cert via the webfaction api.

You can test it's working by forcing a renewal - run the command from the crontab with `--force` appended, i.e. something like:

```
"/home/USER/.acme.sh"/acme.sh --cron --home "/home/USER/.acme.sh" --force
```

If everything is working correctly, you should see the certificates renewed and the message "Reload success".



[acme.sh]: https://github.com/Neilpang/acme.sh
[webfaction]: https://www.webfaction.com/
