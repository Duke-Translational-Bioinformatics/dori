#####################################
# doirisks/dori
# by Ted M
#
#####################################

FROM ubuntu:14.04
MAINTAINER "DOI RISKS"

ADD . /src
RUN DEBIAN_FRONTEND=noninteractive bash /src/setup/dockersetup.sh

