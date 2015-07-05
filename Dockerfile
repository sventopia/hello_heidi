FROM base/archlinux
MAINTAINER sventopia <sventopia@me.com>
RUN pacman -Sy
RUN pacman -Sy net-tools
RUN pacman -S --noconfirm python python-pip
RUN pip install requests
