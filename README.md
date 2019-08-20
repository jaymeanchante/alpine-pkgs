# alpine-pkgs

Alpine package information as a CSV for the `armv7` architecture

Currently, you can only query [alpine packages](https://pkgs.alpinelinux.org/packages) using the package name. However, you can't search using the package description (it appears as you hover your mouse over the package name or if you click on the package). As a bought a [Nokia N900](https://wiki.maemo.org/Nokia_N900) to install and use [PostmarketOS](https://postmarketos.org/), I had the need to discover and install new packages for the `armv7` architecture in the alpine repositories.

This repository contains an updated database in the relative path - `./data.csv` - or in the [URL](https://raw.githubusercontent.com/jayme-anchante/alpine-pkgs/master/data.csv), if you want to update the data yourself you can follow the instructions below:

# Installation

1. Clone this repository:

```
git clone https://github.com/jayme-anchante/alpine-pkgs.git
```

2. Install dependencies and pull the data:

```
cd alpine-pkgs && \
python3 -m venv venv && \
source venv/bin/activate && \
pip3 install -U pip && \
pip3 install -r requirements.txt && \
python3 get_data.py
```

3. (Optional) Run analysis:

```
jupyter-notebook
```

and check `localhost:8888`
