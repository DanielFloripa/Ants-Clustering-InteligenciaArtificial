#!/bin/sh

convert -delay 20 -loop 0 -caption "" imagens/*.png imagens/Animado.gif
firefox imagens/Animado.gif
