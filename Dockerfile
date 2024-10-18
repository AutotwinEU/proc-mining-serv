# Stage 1: Build special dependencies
FROM python:3.10 AS stage1
WORKDIR /spec-deps
RUN apt-get update
RUN apt-get install -y graphviz graphviz-dev
RUN pip wheel pygraphviz
RUN curl -s https://api.github.com/repos/scipopt/scip/releases/latest \
| grep browser_download_url \
| grep SCIPOptSuite-.*-Linux-ubuntu22\.deb \
| cut -d \" -f 4 \
| xargs wget

# Stage 2: Run process mining service
FROM python:3.10-slim AS stage2
LABEL mantainer="Lulai Zhu"
WORKDIR /proc-mining-serv
COPY --from=stage1 /spec-deps /proc-mining-serv
RUN pip install pygraphviz-*-cp310-cp310-linux_x86_64.whl \
&& rm pygraphviz-*-cp310-cp310-linux_x86_64.whl
RUN apt-get update
RUN apt-get install -y \
libblas3 libcliquer1 libgfortran5 liblapack3 libopenblas0 libtbb12 libquadmath0
RUN dpkg -i SCIPOptSuite-*-Linux-ubuntu22.deb && rm SCIPOptSuite-*-Linux-ubuntu22.deb
RUN pip install autotwin_pmswsgi
RUN useradd admin
RUN chown -R admin /proc-mining-serv
USER admin
EXPOSE 8080
ENV MPLCONFIGDIR="matplotlib"
CMD ["/bin/sh", "-c", "waitress-serve autotwin_pmswsgi:wsgi > access.log 2>&1"]
