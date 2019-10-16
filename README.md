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

Installation
------------
Xenial is [Python](https://www.python.org) application based on 
[Kivy](https://kivy.org) framework. It is developed and tested on 
[Ubuntu 19.04](http://releases.ubuntu.com/19.04/) and its primary
installation targets are middle-sized devices running 
[Android](https://en.wikipedia.org/wiki/Android_(operating_system))
operating system.

### Linux
Clone [xenial repository](https://github.com/sciber/xenial) 
on your computer:
```
git clone git@github.com:sciber/xenial.git  
```

Install application dependencies.
```
cd xenial
pip install -r requirements.txt
```

Since ffpyplayer is buggy in both stable (unable to detect audio channels
to play on) and developmental (does not recognize end of audio stream) versions,
I installed kivy from sources into virtualenv environment.
```
python3 -m virtualenv venv
source ven/bin/activate
pip install Cython==0.29.10
pip install --no-binay :all: kivy
```

### Android

Installation from Linux using [buildozer](https://github.com/kivy/buildozer).
