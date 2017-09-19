#!/bin/bash

xelatex slides1 && \
biber slides1 && \
xelatex slides1 && \
xelatex slides1
