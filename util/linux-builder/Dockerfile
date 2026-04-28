FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
        python3.10 python3.10-venv python3.10-dev python3-pip \
        libusb-1.0-0-dev libudev-dev build-essential \
        wget ca-certificates file libfuse2 desktop-file-utils \
        libgl1 libegl1 libxkbcommon0 libdbus-1-3 libxcb-icccm4 libxcb-image0 \
        libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 \
        libxcb-xinerama0 libxcb-xkb1 libxcb-cursor0 \
    && rm -rf /var/lib/apt/lists/*

RUN cd /opt \
    && wget -q https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage \
    && chmod +x appimagetool-x86_64.AppImage \
    && ./appimagetool-x86_64.AppImage --appimage-extract \
    && mv squashfs-root appimagetool \
    && rm appimagetool-x86_64.AppImage \
    && ln -s /opt/appimagetool/AppRun /usr/local/bin/appimagetool

COPY . /vial-gui
