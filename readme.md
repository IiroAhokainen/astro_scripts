# About
This repository contains scripts that facilitate usage of ASTRO(v1.0) software (https://github.com/LeonidSavtchenko/Astro).

## fix3Dviewer
The script helps importing morphologies from http://neuromorpho.org/ to the ASTRO. One can download SWC formated files from the neuromorpho, but those will not work as stand-alone with the
ASTRO. The ASTRO requires HOC files, and those can be generated with tools like a NEURON's (https://neuron.yale.edu/neuron/) import3D and a neuromorpho's 3Dviewer. However, there is compatibility 
issues with HOC files formated for the NEURON compared to what the ASTRO needs. After converting an SWC file to HOC files with both 3Dviewer and import3D tools, fix3Dviewer.py can be used to correct 
the 3Dviewer HOC file, which then can be used with the ASTRO.
