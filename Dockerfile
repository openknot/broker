FROM python:2.7-onbuild

EXPOSE 80

CMD ["broker"]

RUN python setup.py install
