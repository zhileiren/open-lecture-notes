#!/bin/bash

xelatex slides && \
biber slides && \
xelatex slides && \
xelatex slides
