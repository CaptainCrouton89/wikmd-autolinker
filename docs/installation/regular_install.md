---
layout: default
title: Regular installation
parent: Installation
nav_order: 1
---

# Regular installation
! It's tested on windows and linux based systems.
! Runs on flask server

Clone te repository
```
git clone https://github.com/Linbreux/wikmd.git
```
cd in wikmd
```
cd wikmd
```

Create a virtual env and activate it(optional)
```
virtualenv venv
source venv/bin/activate
```
Install requirements
```
pip install -r requirements.txt
```
Run the wiki
```
export FLASK_APP=wiki.py
flask run --host=0.0.0.0
```
or 
```
python wiki.py
```

Now visit localhost:5000 and you will see the wiki. With the 0.0.0.0. option it will show up everywhere on the network.

If there are problems feel free to open an github issue you could post the output of wikmd.log to it.

## Linux

Maybe you need to install pandoc on your system before this works.
```
sudo apt-get update && sudo apt-get install pandoc
```

### Runing the wiki as a service

You can run the wiki as a service. Doing this, will allow the wiki to boot at startup.

```
[Unit]
Description=Wikmd
After=network.target

[Service]
User=brecht
WorkingDirectory=<path to the wiki>
Environment=FLASK_APP=wiki.py
ExecStart=<path to the wiki>/env/bin/python3 wiki.py
Restart=always

[Install]
WantedBy=multi-user.target

```

Put this file in ```/etc/systemd/system/``` as ```wiki.service```.

Run the following commands to enable and start the serivce

```
systemctl daemon-reload
systemctl enable wiki.service
systemctl start wiki.service
```


## Windows

You should install [pandoc](https://pandoc.org/installing.html) on your windows system. Now you should be able to start
the server.
```
python wiki.py
```
If the content of the markdown files are not visible you should add the `pandoc-xnos` location to your path variable. Info about [Environment variables](https://www.computerhope.com/issues/ch000549.htm).
```
pip show --files pandoc-xnos
# look for "location" in the output
# example: C:\users\<user>\appdata\local\packages\pythonsoftwarefoundation.python.3.x\localcache\local-packages\python38\site-packages
# change "site-packages" to "Scripts"
# example: C:\Users\<user>\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.x\LocalCache\local-packages\Python38\Scripts
# open your Environment variables and add the changed line to the path
SET PATH=%PATH%;C:\Users\<user>\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.x\LocalCache\local-packages\Python38\Scripts
```
