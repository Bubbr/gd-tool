# Geometry Dash Multi-Tool (GDMT)

Welcome to **Geometry Dash Multi-Tool** a way to do several things for Geometry Dash... yep, that dead game...
First I'll teach you how GDMT works!

## Get started
As all other python modules we need to import it just like this.
```python
import gdmt
```
### Classes
There are two essential classes: **Level** and **User**.
#### **gdmt.Level** 
There are two ways to initialize it, by the **level name** and by the **level id**, the level name is often more used than the level id, because you don't need to know the id and the name is easier to find. But I recomend to use the level id.
```python
byName = gdmt.Level(byName="Bloodbath")
byId   = gdmt.Level(byId=10565740)
```
#### **gdmt.User**
Just contains the **user information** like name, id, stars, demons, etc. Uses the method **gdmt.getUserData()** and **gdmt.getUserInfo()**. You can initilizate by the user name or the  user id.
```python
byName = gdmt.User("Riot")
byId = gdmt.User(503085)
```

### Methods
#### **gdmt.getFromUrl(f, p)**
#### **gdmt.getUserData(string)**
#### **gdmt.getUserInfo(string)**
#### **gdmt.downloadFromId(Id)**
#### **gdmt.getLevelId(Name)**

## Example
How to get basic information of a level.
```python
import gdmt

lvl = gdmt.Level(byName="Bloodbath")

print(f"Name: {lvl.name}")
print(f"Id: {lvl.id}")
print(f"Creator: {lvl.author.name}"

 output
// Name: Bloodbath
// Id: 10565740
// Creator: Riot
```

## Credits
- Local data decryptor by [WEGFan](https://github.com/WEGFan/Geometry-Dash-Savefile-Editor) and [Absolute Gamer](https://pastebin.com/JakxXUVG)
- Programmed in [Python 3.7.3](https://www.python.org/)
