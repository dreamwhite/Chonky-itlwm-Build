# Chonky-itlwm

The following guide will help you light that chonk `AirportItlwm.kext` and `itlwm.kext`

## Requirements

- [XCode](https://developer.apple.com/xcode/)
- [IORegistryExplorer](https://github.com/utopia-team/IORegistryExplorer)
- [MacKernelSDK](https://github.com/acidanthera/MacKernelSDK)
- [itlwm](https://github.com/OpenIntelWireless/itlwm)
- `7z` installed via [HomeBrew](https://brew.sh)

## How to proceed

After making sure that AirportItlwm stock kext works without any additional edit you can light the firmware from ~ 15MB to 2MB :)


### Identify your firmware version

Open IORegistryExplorer and locate your BT device. You should have something like this:

![](/.assets/images/ioreg.png)

In my case, the firmware version is `iwm-8000C-36`

### Slim that fat boi AirportItlwm

1. Clone itlwm and open the source project
2. Remove `FwBinary.cpp` from `$(source)/include/` as it contains already compressed firmware files
3. Remove every firmware file in `$(source)/itlwm/firmware` except the one which name starts with the previously identified firmware name (e.g. in my case `iwm-8000C-36`)
    - please note that some firmware may have a similar name from the one identified via IORegistryExplorer: choose the one that has the closest name


![](/.assets/images/firmware.png)

4. Clone MacKernelSDK onto `$(source)` with `git clone https://github.com/acidanthera/MacKernelSDK.git`.
5. Open XCode and build the project with `Release` configuration using `⇧⌘R` and after it finishes building the project, replace the old `AirportItlwm.kext` (or `itlwm.kext`) with the newly generated for your OS version

# How to generate every single firmware

Run `python3 main.py` and see the magic happen.
Created kexts will be in `Kexts` folder

# Issues

If you encounter any issue, please file a bugreport [here](https://github.com/dreamwhite/bugtracker/issues/new?assignees=dreamwhite&labels=bug&template=generic.md&title=)

# Credits

- [Apple](https://apple.com) for [XCode](https://developer.apple.com/xcode/) and [IORegistryExplorer](https://github.com/utopia-team/IORegistryExplorer)
- [OpenIntelWireless](https://github.com/OpenIntelWireless) for [itlwm](https://github.com/OpenIntelWireless/itlwm)
- [Acidanthera](https://github.com/acidanthera) for [MacKernelSDK](https://github.com/acidanthera/MacKernelSDK)
- [@1alessandro1](https://github.com/1alessandro1) for helping me through my mental breakdowns and `7z` args
