FROM praekeltfoundation/alpine-buildpack-deps:3.4

# rename many traces of Alpine Python (so that they are not used by mistake)
# In the upstream Debian-based images similar files are dpkg-divert'ed but
# Alpine's package manager doesn't have this (obscure) functionality so we just
# rename the files (deleting wouldn't have any advantage since files exist in
# lower layers). We rename all the files in the 'python' package.
RUN set -ex \
        && for bits in \
            /usr/bin/idle \
            /usr/bin/py* \
            /usr/bin/smtpd.py \
            /usr/include/*python* \
            /usr/lib/*python* \
        ; do \
            mv "$bits" "$bits.distrib"; \
        done

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# gpg: key 18ADD4FF: public key "Benjamin Peterson <benjamin@python.org>" imported
ENV GPG_KEY C01E1CAD5EA2C4F0B8E3571504C367C218ADD4FF

ENV PYTHON_VERSION 2.7.12

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 8.1.2

RUN set -ex \
        && buildDeps=' \
            gnupg \
            tar \
            tcl-dev \
            tk-dev \
        ' \
        && runDeps=' \
            tcl \
            tk \
        ' \
        && apk add --no-cache $runDeps $buildDeps \
        && curl -fSL "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" -o python.tar.xz \
        && curl -fSL "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" -o python.tar.xz.asc \
        && export GNUPGHOME="$(mktemp -d)" \
        && gpg --keyserver ha.pool.sks-keyservers.net --recv-keys "$GPG_KEY" \
        && gpg --batch --verify python.tar.xz.asc python.tar.xz \
        && rm -r "$GNUPGHOME" python.tar.xz.asc \
        && mkdir -p /usr/src/python \
        && tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
        && rm python.tar.xz \
        && cd /usr/src/python \
        && ./configure \
            --enable-shared \
            --enable-unicode=ucs4 \
        && make -j$(getconf _NPROCESSORS_ONLN) \
        && make install \
        && curl -fSL 'https://bootstrap.pypa.io/get-pip.py' | python2 \
        && pip install --no-cache-dir --upgrade pip==$PYTHON_PIP_VERSION \
        && [ "$(pip list | awk -F '[ ()]+' '$1 == "pip" { print $2; exit }')" = "$PYTHON_PIP_VERSION" ] \
        && find /usr/local -depth \
            \( \
                \( -type d -a -name test -o -name tests \) \
                -o \
                \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
            \) -exec rm -rf '{}' + \
        && apk del $buildDeps \
        && rm -rf /usr/src/python ~/.cache

CMD ["python2"]
