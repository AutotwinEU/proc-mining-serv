FROM python:3.10-slim
LABEL mantainer="Lulai Zhu"
WORKDIR /proc-mining-serv
RUN pip install autotwin_pmswsgi
RUN useradd admin
RUN chown -R admin /proc-mining-serv
USER admin
EXPOSE 8080
CMD ["waitress-serve", "--host", "0.0.0.0", "autotwin_pmswsgi:wsgi"]
