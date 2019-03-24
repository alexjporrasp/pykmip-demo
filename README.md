**PyKMIP Secure file prototype**

Make sure you have a working version of python 3 installed and create the following virtual environment.

*Note: This document assumes you are running linux*

```
python3 -m virtualenv pykmip_demo
```
Activate the environment.

```
source pykmip_demo/bin/activate
```

Clone or download the demo and navigate to the root folder (you can find `requirements.txt` there) and install the dependencies in the virtual environment:

```
pip install -r requirements.txt
```

**Preamble**

The certificates for this demo were created using the `create_certificates.py` (2)

The client and the server must have their certificates signed by the same CA authority (in our case, `root_certificate.pem`)

**Run the server**

Navigate to the server directory and execute the server script with the shown options.

*Note: It is important to run the server from the server directory because the configuration files use relative urls for the certificate files*

```
cd server/
python run_server.py -d db/pykmip.database -f conf/server.conf -l log/server.log
```
* `db/pykmip.database` is where the server stores the managed keys. It is preserverd between server restarts.
* `conf/server.conf` holds the server configuration file, it states the certificates locations among other things.
* `log/server.log` points to the server log file.

**Encrypt a file**

Once you have the server running, open a different terminal and activate the `pykmip_demo` virtual environment as it was shown before.

The steps to encrypt a file are shown below.

```
cd client/
python encrypt.py -s conf/pykmip.conf -c client files/helloworld.txt
```

* `conf/pykmip.conf` is the path to the client configuration file.
* `client` is the chosen section of the configuration file.

This demo provides a sample file located in the files directory to test the encryption and decryption.

The resulted encrypted file has its key uuid attached and is saved with the following name `helloworld_enc`.


**Decrypt a previously encrypted file**

The steps to decrypt a file are similar.

```
cd client/
python decrypt.py -c client -s conf/pykmip.conf files/helloworld_enc 
```

The decrypted file will be called `helloworld_dec` you may check that it is the same as `helloworld.txt`

**References**

(1) For more information visit the PyKMIP documentation : [PyKMIP Repo](https://github.com/OpenKMIP/PyKMIP)

(2) [Create Certificates](https://github.com/OpenKMIP/PyKMIP/blob/master/bin/create_certificates.py)
