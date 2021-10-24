FROM cr.msk.sbercloud.ru/aijcontest2021/fusion:0.0.1

USER root


WORKDIR /tmp
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py && python2 get-pip.py&& \
    rm get-pip.py


ADD . /mnt
WORKDIR /mnt

RUN cd /mnt/antlr-3.1.3/runtime/Python && python2 setup.py install && \
    cd /mnt/java2python-0.5.1 && python2 setup.py install

USER user

RUN pip install . && python test.py

USER root
RUN rm -rf /mnt/*

USER user
WORKDIR /home/user


CMD while true; do sleep 30; done;