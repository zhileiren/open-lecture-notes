#!/usr/bin/env bash

xelatex slides3 && \
biber slides3 && \
xelatex slides3 && \
xelatex slides3
