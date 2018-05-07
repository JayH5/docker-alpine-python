FROM praekeltfoundation/alpine-buildpack-deps:3.6

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

ENV GPG_KEY 0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D
ENV PYTHON_VERSION 3.6.5

RUN set -ex \
        && wget -O python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" \
        && wget -O python.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" \
        && export GNUPGHOME="$(mktemp -d)" \
        && gpg --keyserver ha.pool.sks-keyservers.net --recv-keys "$GPG_KEY" \
        && gpg --batch --verify python.tar.xz.asc python.tar.xz \
        && rm -rf "$GNUPGHOME" python.tar.xz.asc \
        && mkdir -p /usr/src/python \
        && tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
        && rm python.tar.xz \
        \
        && apk add --no-cache --virtual .build-deps  \
            coreutils \
            dpkg-dev dpkg \
            tcl-dev \
            tk \
            tk-dev \
        \
        && cd /usr/src/python \
        && gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" \
        && ./configure \
            --build="$gnuArch" \
            --enable-loadable-sqlite-extensions \
            --enable-shared \
            --with-system-expat \
            --with-system-libffi \
            --without-ensurepip \
        && make -j$(nproc) \
# set thread stack size to 1MB so we don't segfault before we hit sys.getrecursionlimit()
# https://github.com/alpinelinux/aports/commit/2026e1259422d4e0cf92391ca2d3844356c649d0
            EXTRA_CFLAGS="-DTHREAD_STACK_SIZE=0x100000" \
        && make install \
        \
        && runDeps="$( \
            scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
        )" \
        && apk add --virtual .python-rundeps $runDeps \
        && apk del .build-deps \
        \
        && find /usr/local -depth \
            \( \
                \( -type d -a -name test -o -name tests \) \
                -o \
                \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
            \) -exec rm -rf '{}' + \
        && rm -rf /usr/src/python

# make some useful symlinks that are expected to exist
RUN cd /usr/local/bin \
        && ln -s idle3 idle \
        && ln -s pydoc3 pydoc \
        && ln -s python3 python \
        && ln -s python3-config python-config

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 10.0.1

RUN set -ex; \
        \
        wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py'; \
        \
        python get-pip.py \
            --disable-pip-version-check \
            --no-cache-dir \
            "pip==$PYTHON_PIP_VERSION" \
        ; \
        pip --version; \
        \
        find /usr/local -depth \
            \( \
                \( -type d -a -name test -o -name tests \) \
                -o \
                \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
            \) -exec rm -rf '{}' +; \
        rm -f get-pip.py

# HACK: Fix for building numpy
# https://github.com/docker-library/python/issues/112#issuecomment-238383259
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

CMD ["python3"]
