import os
import subprocess
import csv
import plistlib
import json

from argparse import ArgumentParser

def resolveArgs():
    parser = ArgumentParser()
    parser.add_argument('--path', '-p', dest='path', type=str) #path/to/folder
    args = parser.parse_args()
    return args

def call(cmd, errorMessage: str = ''):
    if subprocess.call(cmd, shell=True) != 0 and len(errorMessage) > 0:
        logError(errorMessage)
        exit()

def logInfo(message):
    print('\x1b[6;30;42m' + message + '\x1b[0m')

def logError(message):
    print('\x1b[0;30;41m' + message + '\x1b[0m')

def loadPodspecs(podspecPaths):
    podspecMap = {}
    for podspecPath in podspecPaths: 
        with open(podspecPath) as f:
            podspec = json.load(f)

            if 'name' in podspec:
                name = podspec['name'].replace(' ', '')
                podspecMap[name] = podspec

    return podspecMap

def loadCopyrightMap(mdFile):
    copyrighMap = {}

    f = open(mdFile, "r")
    lines = f.readlines()

    name = ''
    content = ''
    for line in lines:
        if line.startswith('##'):
            if len(content) > 0:
                copyrighMap[name] = content
                content = ''
            name = line.replace('##', '').replace(' ', '').replace('\n', '')
        elif len(name) > 0:
            content += line

    copyrighMap[name] = content

    return copyrighMap

def loadLicenseMap(plistFile):
    f = open(plistFile, 'rb')
    pl = plistlib.load(f)
    libs = pl['PreferenceSpecifiers']
    licenses = {'': ''}

    for lib in libs:
        if 'License' in lib and 'Title' in lib:
            licenses[lib['Title']] = lib['License']

    return licenses

def getLicenses(projectRootPath):
    # Remove Pods cache
    podCachePath = os.path.expanduser('~/Library/Caches/CocoaPods')
    if os.path.isdir(podCachePath):
        call(f'rm -rf {podCachePath}')

    # Remove Pods folder
    projectPodsDirPath = f'{projectRootPath}/Pods'
    if os.path.isdir(projectPodsDirPath):
        call(f'rm -rf {projectPodsDirPath}')

    # Call `pod install`
    os.chdir(projectRootPath)
    call('pod install', errorMessage='`pod install` error')

    # get podspecs
    podspecPaths = []
    for (dirPath, _, files) in os.walk(f'{projectRootPath}/Pods/Local Podspecs/'):
        podspecPaths += [os.path.join(dirPath, file) for file in files if file.endswith('.json')]
    for (dirPath, _, files) in os.walk(f'{podCachePath}/Pods/Specs'):
        podspecPaths += [os.path.join(dirPath, file) for file in files if file.endswith('.json')]
    podspecMap = loadPodspecs(podspecPaths)

    # get copyright attributions
    podsDir = f'{projectRootPath}/Pods/Target\ Support\ Files/Pods-*'
    copyrightPaths = [line for line in subprocess.check_output(f"find {podsDir} -name 'Pods*acknowledgements.markdown'", shell=True).splitlines()]
    assert(len(copyrightPaths) == 1)
    copyrightMap = loadCopyrightMap(copyrightPaths[0])

    # get license types
    licensePaths = [line for line in subprocess.check_output(f"find {podsDir} -name 'Pods*acknowledgements.plist'", shell=True).splitlines()]
    assert(len(licensePaths) == 1)
    licenseMap = loadLicenseMap(licensePaths[0])

    # write to file
    with open('license.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        writer.writerow(['Name', 'Copyright', 'License', 'URL'])

        for libName in copyrightMap:
            license = ''
            url = ''
            copyright = copyrightMap[libName]

            if libName in licenseMap:
                license = licenseMap[libName]
            
            if libName in podspecMap and 'homepage' in podspecMap[libName]:
                url = podspecMap[libName]['homepage']

            writer.writerow([libName, copyright, license, url])
    
    # open file
    call('open license.csv')

if __name__ == '__main__':
    args = resolveArgs()
    if not args.path:
        logError('Path to project must not be empty. Use -p or --path')
        exit()
    path = args.path
    getLicenses(path)