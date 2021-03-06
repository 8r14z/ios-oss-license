# iOS Open Source Software (OSS) Licenses 
If you are developing an iOS app, it will be a norm that you are using at least one open source library or two (or hundreds). Well! who is gonna reinvent the wheel? 

So at some point, you may encounter a situation that u need to attribute all open sources being using in the project. For example, Instagram (and several big apps) has a whole section for that purpose `Profile > Settings > About`

<img width="200" alt="notme" src="https://user-images.githubusercontent.com/27178862/113502779-fe40f100-9560-11eb-9c22-1ef5018707ec.PNG">

## How-to
### Prerequisite
Make sure `Python 3` is installed on your machine. if not, [here](https://www.python.org/downloads/)

### Run the script
This script will export a CSV file that contains all your licenses. 
```
$ python3 getlicense.py -p path/to/your/ios/project
```
- `-p`: the path to your project root, where the `Podfile` file is located. 

The result is a CSV file named `license.csv`, which is similar to this format

| Name|Copyright|License|URL
| ------------- |:-------------:|:-----:|:-----:|
|AFNetworking|The content of [this](https://github.com/AFNetworking/AFNetworking/blob/master/LICENSE)|MIT |https://github.com/AFNetworking/AFNetworking/

The table can include countless data. Basically, all kind of info in podspec. Feel free to custom the below line.

```python
if libName in podspecMap and 'homepage' in podspecMap[libName]:
    url = podspecMap[libName]['homepage']
```
### How to automate this process?
This is simple! Can create a CI job and make it run once in a while -> write a codegen to port this CSV to Swift/Objective-C code or a file format that is more readable for iOS and then load lazily to show in runtime (on-demand) 

--> u will have licenses regularly updated in your app. Cheers! 

### How does this work? 
--> read the code tho, the master function is `def getLicenses(projectRootPath):`. I know it's super ugly but some how it works (at least in my case) 

## It doesn't work for you? 
Haha I'm sure it's not working for everybody. **So what's next?**

**DIY!** There are hints in the code, I believe so (\*serious voice\*)

<img width="547" alt="notme" src="https://user-images.githubusercontent.com/27178862/113502456-0009b500-955f-11eb-89ec-477ca9750677.png">
