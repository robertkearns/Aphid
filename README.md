# Aphid Toolkit
#### Toolkit for dealing with nested data types in python. Supports working with any datatype with ```key:value``` attributes. Use it to find, substitute, and get the path to nested data. Supports searching via string, regex, list, and tuple. The OO layout also makes it easy to subclass and customize exactly what happens when a match is found, or how comparisons are handled. The syntax itself is very similar to the built in regular expression module ```re```.

* ### [Aphid on Github](https://github.com/robertkearns/Aphid):
    * ####  [Docs](https://github.com/robertkearns/Aphid/wiki/Quick-Start)
* ### [Aphid on PyPi](https://pypi.org/project/Aphid/):      ```py -m pip install Aphid```
### How it works:
In sum it works based on recursive iteration. When a function is called it creates an instance of the appropriate class. The function then returns an attribute of that instance, and the instance is garbage collected immediately. I whent for a class based approach over a function based approach based on added functionality such as the ```StackTracker``` and ```Debugger``` which would be hard to implement without globals. The whole time the method is running the ```StackTracker``` is keeping track of the depth of recursion. This is two fold; in debug mode it allows the levels to be printed out, and it allows for the ```max_depth``` key word to to used reliably.

### Why I started this project:
We all share in the frustration of working with new API's who never stop coming up with 'great' ways to structure their json responses. This module aims to make it a bit easier to find the data you need. Another goal of this project was to help accelerate the learning curve that comes with a new package. Finding out exactly where ```openpyxl``` stores that title text for your bar chart is tedious. With **Aphid** you can simply search the instance with a regex and get a mapped path in seconds. 
