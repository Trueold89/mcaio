# MCaio

Asynс lib to get information about Minecraft Java server using **[SLP](https://wiki.vg/Server_List_Ping)**

Project uses code from **[clarence112](https://gist.github.com/clarence112/9a3e971283d7f4052a0c33f11de9b7c5)**

## Install:

**From Gitea**
```bash
pip install --extra-index-url https://git.orudo.ru/api/packages/trueold89/pypi/simple/ mcaio
```

**From PyPi**
```bash
pip install mcaio
```

## Build:

**Deps:** python3

**Clone repo:**
```bash
git clone https://git.orudo.ru/trueold89/mcaio --depth=1 && cd mcaio
```

**Create venv:**
```bash
python -m venv venv && . venv/bin/activate
```

**Install SetupTools**:
```bash
pip install setuptools
```

**Build:**
```
python3 setup.py sdist
```

## Usage:

### As lib:

**Import MCServer class:**:
```python
from mcaio.client import AIOMCServer as AIOMC
```

**Create object:**
```python
mc = AIOMC("localhost", 25565)
```

**Await property:**
```python
name = await mc.name
print(name)
# Paper 1.20.4
```

**Properties:**
| Property | Description |
| -------- | ----------- |
| name | Server name |
| motd | Server motd |
| players_count | Current number of players on the server |
| maxplayers | Max number of players on the server |


### As cli:

```bash
MC_HOST=localhost MC_PORT=25565 mcaio name
# Paper 1.20.4
```
**Args:**
| Arg | Description |
| -------- | ----------- |
| name | Server name |
| motd | Server motd |
| pcount | Current number of players on the server |
| pmax | Max number of players on the server |
