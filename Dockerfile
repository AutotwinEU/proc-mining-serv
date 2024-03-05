# Stage 1: Build special dependencies
FROM python:3.10 AS stage1
WORKDIR /spec-deps
RUN apt-get update
RUN apt-get install --yes graphviz graphviz-dev
RUN pip wheel pygraphviz

# Stage 2: Run process mining service
FROM python:3.10-slim AS stage2
LABEL mantainer="Lulai Zhu"
WORKDIR /proc-mining-serv
COPY --from=stage1 /spec-deps /proc-mining-serv
RUN pip install *.whl && rm *.whl
RUN pip install autotwin_pmswsgi
RUN useradd admin
RUN chown -R admin /proc-mining-serv
USER admin
EXPOSE 8080
ENV MPLCONFIGDIR="matplotlib"
CMD ["waitress-serve", "--host", "0.0.0.0", "autotwin_pmswsgi:wsgi"]
