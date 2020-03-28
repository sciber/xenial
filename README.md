<p align="center"><img src="https://raw.githubusercontent.com/sciber/xenial/master/icon.png" width=150></p>

Xenial
======

The Migrant's guide to the World 

Xenial application is intended to be a guides for people traveling to other
countries with possible intention to settle there (i.e. migrants). The idea 
of creating such an application was inspired by a fictional 
[book *The Hitchhiker's Guide to the Galaxy*](https://en.wikipedia.org/wiki/The_Hitchhiker%27s_Guide_to_the_Galaxy_(fictional))
from [Douglas Adams](https://en.wikipedia.org/wiki/Douglas_Adams) 
[franchise *The Hitchhiker's Guide to the Galaxy*](https://en.wikipedia.org/wiki/The_Hitchhiker%27s_Guide_to_the_Galaxy_(fictional)).
This is an attempt to build a model of [the book](https://en.wikipedia.org/wiki/The_Hitchhiker%27s_Guide_to_the_Galaxy_(fictional))
using presently available terrestrian technology.

![Screenshots](screenshots.gif)

Purpose
-------
There is an increasing number of people travelling between places on Earth.
In near future it is expected that migrating part of world population
will significantly grow in size due to war conflicts and climate change.

Main purpose of this application is to create a tool for the migrants to
achieve targets of their journey safely and comfortably thanks 
to information it provides.

Functionality
-------------



Interface
---------
Content of the application is composed fo guides which are sets of 
articles/entries. The articles can be tagged and based on the assigned tags they
fall into groups called *categories*. Thus every category has assigned
set of tags and every article in a category has all tags of the category
(and possibly other tags)



Requirements
------------
Application is expected to run using Python 3.7.3 and above.

Installation on Linux
---------------------
Xenial is [Python](https://www.python.org) application based on 
[Kivy](https://kivy.org) framework. It is developed and tested on 
[Ubuntu 19.04](http://releases.ubuntu.com/19.04/) and its primary
installation targets are middle-sized devices running 
[Android](https://en.wikipedia.org/wiki/Android_(operating_system))
operating system.

Clone [xenial repository](https://github.com/sciber/xenial) 
on your computer:
```
git clone git@github.com:sciber/xenial.git  
```

Install application dependencies:
```
cd xenial
pip install -r requirements.txt
```

Download a [dummy guide archive](https://raw.githubusercontent.com/sciber/xenial-guides/master/dist/dummy/alice_v0.1.zip) and copy 
into the application's guides directory (xenial/guides)

Run application mimicking a mobile device portrait mode:
```
python3 main --size=380x640
```

Build for Android
-----------------

Install [buildozer](https://github.com/kivy/buildozer) and its dependencies :
```
pip install Cython==0.29.10 buildozer==1.0
```

Connect your mobile device to your Linux or OSX computer... if you do not know how, watch 
Erik SandberErik Sandberg's great video [tutorial](https://www.youtube.com/watch?v=EupAeyL8zAo). 

Build and and deploy the app to your device:
```
buildozer android debug deploy run 
```

### Install application's APK

Download application's APK (the build includes a dummy guide) to your mobile device from [sciber/xenial-builds](https://https://github.com/sciber/xenial-builds)
repository:

https://raw.githubusercontent.com/sciber/xenial-builds/master/android/xenial__armeabi-v7a-0.1-armeabi-v7a-debug.apk
