import argparse
import os
import subprocess
import sys

from shutil import which

# Checks if platform is macOS, if not raises an error
if sys.platform != 'darwin':
    print('ERROR: The following script runs only on macOS')
    sys.exit(1)

parser = argparse.ArgumentParser(description='AirportItlwm de-chonker')
parser.add_argument('-v', '--verbose', action='store_true',help='Enable verbose')
args = parser.parse_args()

# Checks if the necessary tools are installed
if not os.path.exists('/Applications/Xcode.app/Contents/Developer') or not os.path.exists('/Library/Developer/CommandLineTools'):
    print('ERROR: Xcode does not appear to be installed. Please install it from App Store')
    sys.exit(1)

# If CLI tools are installed, git should be already installed. Probably gonna remove this if
if which('git') == None:
    print('ERROR: git does not appear to be installed. Please install it')
    sys.exit(1)

if not os.path.exists('itlwm'):
    print('WARNING: itlwm doesn\'t appear to be cloned. Cloning...\n')
    subprocess.run(['git', 'clone', 'https://github.com/OpenIntelWireless/itlwm'], capture_output=not args.verbose)

os.chdir('itlwm')

if not os.path.exists('../Kexts'):
    print('Creating Kexts output folder...')
    subprocess.run(['mkdir', '../Kexts'], capture_output=not args.verbose)
else:
    print('Detected Kexts output folder. Removing it as it may contain old built kexts...\n')
    subprocess.run(['rm', '-r', '../Kexts'], capture_output=not args.verbose)

if not os.path.exists('MacKernelSDK'):
    print('WARNING: MacKernelSDK doesn\'t appear to be cloned. Cloning...\n')
    subprocess.run(['git', 'clone', 'https://github.com/acidanthera/MacKernelSDK.git'], capture_output=not args.verbose)

firmwares = [fw for fw in os.listdir('itlwm/firmware') if fw != '.DS_Store']

for firmware in firmwares:
    if os.path.exists('include/FwBinary.cpp'):
        print('Detected FwBinary.cpp. Removing it as it may contain old firmwares...\n')
        subprocess.run(['rm','include/FwBinary.cpp'], capture_output=not args.verbose)
    print(f'Building AirportItlwm for {firmware}...\n')
    subprocess.run(['find', 'itlwm/firmware', '-type', 'f', '-not', '-name', f'{firmware}', '-delete'], capture_output=not args.verbose)
    subprocess.run(['xcodebuild', '-project', 'itlwm.xcodeproj', '-scheme', 'AirportItlwm (all)', '-configuration', 'Release', '-sdk', 'macosx', '-derivedDataPath', 'out'], capture_output=not args.verbose)
    subprocess.run(['xcodebuild', '-project', 'itlwm.xcodeproj', '-scheme', 'itlwm', '-configuration', 'Release', '-sdk', 'macosx', '-derivedDataPath', 'out'], capture_output=not args.verbose)
    subprocess.run(['mkdir', 'out/Build/Products/Release/itlwm'], capture_output=not args.verbose)
    subprocess.run(['mv', 'out/Build/Products/Release/itlwm.kext', 'out/Build/Products/Release/itlwm.kext.dSYM', 'out/Build/Products/Release/itlwm'], capture_output=not args.verbose)
    subprocess.run(['7z', 'a', '-r', f'out/Build/Products/Release/{firmware}.zip', './out/Build/Products/Release/*'], capture_output=not args.verbose)
    subprocess.run(['mv', f'out/Build/Products/Release/{firmware}.zip', '../Kexts'], capture_output=not args.verbose)
    subprocess.run(['git', 'reset', '--hard', 'HEAD'], capture_output=not args.verbose)
    subprocess.run(['rm', '-rf', 'out'], capture_output=not args.verbose)
