# pyfetch
Simple Fetch written in Python

# Screenshots
![Pyfetch Thin](https://i.imgur.com/AA1XBRq.png)

![Pyfetch Thick](https://i.imgur.com/ve7T89D.png)


# Requirements
- Curl (optional for weather)
- Nerd Fonts (or a font with icons)

# Install
Clone this repository
```
git clone https://github.com/KotonBads/pyfetch.git
```
Either copy `pyfetch.py` to `$PATH` or make a symlink to it
```
ln /path/to/pyfetch.py/ ~/local/bin
cp /path/to/pyfetch.py/ ~/local/bin
```
or wherever you want to install it

# CLI Args
```
pyfetch.py --thin # thin color blocks
pyfetch.py --thick # thick color blocks
no args # thin color blocks (default)
```

# Configuration
Since this is written in Python, this is easily hackable and can be modified to your liking. I might add a configuration file sooner or later depending if enough people actually want it.