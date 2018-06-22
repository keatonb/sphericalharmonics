# sphericalharmonics
Generate animated gifs of spherical harmonics, like this:

![Example spherical harmonic animation](https://raw.githubusercontent.com/keatonb/sphericalharmonics/master/l2m0.gif)

Run from the Terminal with these options:
```
usage: shanimate.py [-h] [-o OUTFILE] [-i INC] [-s SIZE] [-n NFRAMES]
                    [-d DURATION] [--nlon NLON] [--nlat NLAT] [--dpi DPI]
                    ell m

Generate animated gif of spherical harmonic.

positional arguments:
  ell                   spherical degree
  m                     azimuthal order

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        output gif filename
  -i INC, --inc INC     inclination (degrees from pole)
  -s SIZE, --size SIZE  image size (inches)
  -n NFRAMES, --nframes NFRAMES
                        number of frames in animation
  -d DURATION, --duration DURATION
                        animation duration (seconds)
  --nlon NLON           number of longitude samples
  --nlat NLAT           number of latitude samples
  --dpi DPI             dots per inch

```
