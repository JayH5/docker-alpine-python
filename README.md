# docker-alpine-python

[![Build Status](https://img.shields.io/travis/praekeltfoundation/docker-alpine-python/develop.svg)](https://travis-ci.org/praekeltfoundation/docker-alpine-python)

Full-fat cPython Docker images based on Alpine Linux

These images are like the [official](https://hub.docker.com/_/python/) Python Docker images in that they contain build tools and development libraries but are based on Alpine Linux instead of Debian.

These images are *not* smaller than their Debian counterparts. They should be used to build Python software that includes native extensions. The software can then be used in smaller images by installing built [wheels](https://pypi.python.org/pypi/wheel). Good small base images for Python software are the `python:2-alpine` and `python:3-alpine` images.

## Caveats
* The [`dbm`](https://docs.python.org/2/library/dbm.html) module fails to build. The Alpine `db-dev` package doesn't seem to include the `dbm` symbols that Python wants.
* The [`nis`](https://docs.python.org/2/library/nis.html) module isn't built. Alpine's libc does not include `nis` headers or libraries.
