FROM ubuntu:18.04
#FROM selenium/node-chrome:3.12.0-cobalt
#FROM python:alpine3.6
#ref: https://hub.docker.com/_/python/
RUN apt-get update
RUN apt-get install gcc -y
RUN apt-get install python-dev -y
RUN apt-get install python3-dev -y
RUN apt-get install musl-dev -y
RUN apt-get install python3-pip -y
RUN apt-get install openssl -y
RUN apt-get install libssl-dev -y
RUN apt-get install wget -y
RUN apt-get install libxss1 libappindicator1 libindicator7 -y
RUN apt-get install -f
RUN apt-get install xvfb -y
RUN apt-get install imagemagick -y
RUN apt-get install unzip -y
RUN apt-get install libglib2.0-0 -y
RUN apt-get install libnss3 -y
RUN apt-get install libgconf-2-4 -y
RUN apt-get install libfontconfig1 -y
RUN apt-get install chromium-browser -y


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


#chrome ref: https://askubuntu.com/questions/510056/how-to-install-google-chrome
#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
#RUN apt-get update 
#RUN apt-get install google-chrome-stable -y



RUN wget -N https://chromedriver.storage.googleapis.com/2.40/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN chmod +x chromedriver

RUN mv -f chromedriver /usr/local/share/chromedriver
RUN ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
RUN ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

#RUN sudo pip3 --upgrade
RUN pip3 install pyvirtualdisplay selenium
WORKDIR /usr/source/app

COPY * ./
#RUN unzip -u chromedriver_linux64.zip
RUN rm Dockerfile
RUN rm chromedriver.exe

#install the requirments
#RUN sudo pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install -r requirements.txt

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

ENV VNC_NO_PASSWORD=1
ENV CHROME_BIN=/opt/google/chrome
ENV CHROME_PATH=/opt/google/
ENV PATH="/usr/bin/chromedriver:${PATH}"
ENV CHROME_HEADLESS=1

EXPOSE 9999
CMD [ "python3", "/usr/source/app/docker_run.py" ]