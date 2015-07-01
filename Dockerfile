FROM base/archlinux
MAINTAINER sventopia <sventopia@me.com>
RUN pacman -Sy
RUN pacman -S --noconfirm python python-pip
