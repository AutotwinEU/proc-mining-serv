# Stage 1: Build special dependencies
FROM python:3.10 AS stage1
WORKDIR /spec-deps
RUN apt-get update
RUN apt-get install --yes graphviz graphviz-dev
RUN pip wheel pygraphviz


# Stage 2: Run process mining service
FROM python:3.10-slim AS stage2
LABEL mantainer="Lulai Zhu"
RUN apt-get update
RUN apt-get install --yes \
    libblas3 libcliquer1 libgfortran5 liblapack3 libopenblas0 libtbb12 libquadmath0 wget
RUN wget https://github.com/scipopt/scip/releases/download/v910/SCIPOptSuite-9.1.0-Linux-ubuntu22.deb
RUN dpkg -i SCIPOptSuite-9.1.0-Linux-ubuntu22.deb \
    && rm SCIPOptSuite-9.1.0-Linux-ubuntu22.deb
WORKDIR /proc-mining-serv
COPY --from=stage1 /spec-deps /proc-mining-serv
RUN pip install *.whl && rm *.whl
RUN pip install autotwin_pnglib
RUN pip install autotwin_pmswsgi
RUN useradd admin
RUN chown -R admin /proc-mining-serv
USER admin
EXPOSE 8080
ENV MPLCONFIGDIR="matplotlib"
CMD ["/bin/sh", "-c", "waitress-serve autotwin_pmswsgi:wsgi > access.log 2>&1"]
