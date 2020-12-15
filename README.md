# CountyCovidTracker
Program to grab nytimes state and county data on covid cases and graph them

#Installation
Requires python 3.8+

git clone the repo

then

```
pip install -r requirements.txt
```


##Usage
Running the script with no arguments 
```
python nytimes_covid.py
```
will make a folder for every state and a covid graph of every county in that state along 
with a graph of statewide covid cases

If you want to get all of the county graphs of a specific state
```
python nytimes_covid.py oregon
```

If you want to get a specific county 
```
python nytimes "los angeles" california
```
needs to be in quotes if there is a space in county name

##Credits
Graphing code taken from https://github.com/Fitzy1293/Berkshire-County-Covid