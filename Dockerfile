# Extend python:3.10 image
FROM python:3.10
LABEL mantainer="Lulai Zhu"
WORKDIR /proc-mining-serv

# Install Graphviz package
RUN apt-get update
RUN apt-get install -y graphviz graphviz-dev xdg-utils

# Install SCIP package
RUN curl -s https://api.github.com/repos/scipopt/scip/releases/latest \
| grep browser_download_url \
| grep SCIPOptSuite-.*-Linux-ubuntu22\.deb \
| cut -d \" -f 4 \
| xargs wget
RUN apt-get install -y \
libblas3 libcliquer1 libgfortran5 liblapack3 libopenblas0 libtbb12 libquadmath0
RUN dpkg -i SCIPOptSuite-*-Linux-ubuntu22.deb && rm SCIPOptSuite-*-Linux-ubuntu22.deb

# Install and Start PMS WSGI
RUN pip install autotwin_pmswsgi
RUN apt-get install -y sudo
RUN adduser --disabled-password --gecos "" admin
RUN adduser admin sudo
RUN echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN chown -R admin /proc-mining-serv
USER admin
EXPOSE 8080
ENV MPLCONFIGDIR="matplotlib"
SHELL ["/bin/sh", "-c"]
CMD echo "autotwin_pmswsgi:wsgi" | xargs sudo -E waitress-serve > access.log 2>&1
