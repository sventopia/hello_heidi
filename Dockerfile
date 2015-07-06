FROM base/archlinux
MAINTAINER sventopia <sventopia@me.com>
RUN pacman -Sy
RUN pacman -S --noconfirm net-tools python python-pip
RUN pip install requests IPy
