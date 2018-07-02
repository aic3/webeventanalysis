FROM selenium/node-chrome:3.12.0-cobalt
#FROM python:alpine3.6
#ref: https://hub.docker.com/_/python/
RUN sudo apt-get update
RUN sudo apt-get install gcc -y
RUN sudo apt-get install python-dev -y
RUN sudo apt-get install python3-dev -y
RUN sudo apt-get install musl-dev -y
#RUN sudo apt-get install libffi -y
#RUN sudo apt-get install libffi-dev -y
#RUN sudo apt-get install unzip -y

#fix chromerdriver crash ref: https://stackoverflow.com/questions/25311593/chromewebdriver-unknown-error-chrome-failed-to-start-crashed
#RUN sudo apt-get install libexif -y
#RUN sudo apt-get install udev -y

#RUN apk add chromium
#RUN apk add chromium-chromedriver 

#Chromedriver ref: https://gist.github.com/theoretick/fbf26c739780d90e03d1b338426fa88c
#RUN apk add --update \
#  build-base \
#  libxml2-dev \
#  libxslt-dev \
#  postgresql-dev \
#  curl \ 
#  unzip \ 
#  libexif \
#  udev \
#  xvfb \
#  xorg-server \
#  dbus \
#  ttf-freefont \
#  mesa-dri-swrast



WORKDIR /usr/source/app

COPY * ./
#RUN unzip -u chromedriver_linux64.zip
RUN sudo rm Dockerfile
RUN sudo rm chromedriver.exe

#install the requirments
RUN sudo pip install --no-cache-dir -r requirements.txt

#ENV PATH="/usr/source/app/chromedriver:${PATH}"

# Do not generate documentation when installing gems and fix shebang
# lines
#RUN echo "gem: --no-rdoc --no-ri --env-shebang" >> "$HOME/.gemrc"

#ADD [".gems", "/srv/app/.gems"]

#RUN gem install dep shotgun rake pry
#RUN dep -f /srv/app/.gems install

# Tell pry to use `more` as the pager because the installed
# version of `less` does not support passing the `-R` which
# is used by pry.
#ENV PAGER="more"

ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROME_PATH=/usr/lib/chromium/
ENV PATH="/usr/lib/chromium/chromedriver:${PATH}"
ENV CHROME_HEADLESS=1
CMD [ "python", "/usr/source/app/docker_run.py" ]