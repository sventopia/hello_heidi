# hello_heidi

This is a class written to test out some simple python work for Swisscom. It's not intended to be entirely useful, but it should work on OSX and Linux, and it should also work with Python 2 and 3.

Extra libraries that need to be installed are **requests** and **IPy**. You can easily install both of these with pip: 
```
pip install requests IPy
```

helloHeidi can be run simply with:
```
python helloHeidi.py
```
Alternatively, you can just use an Archlinux-based **docker** image 
```
docker pull sventopia/hello-heidi
docker run -t -i sventopia/hello-heidi /opt/hello_heidi/helloHeidi.py
```
