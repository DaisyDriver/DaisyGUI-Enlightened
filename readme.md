# **DaisyGUI-Enlightened**
### A graphical user interface to the DaisyDriver open-hardware microscope controller.
#### Features
+ Motor control - natural mapped buttons provide tactile interface to the motors
+ Preview feed - see where you are on the sample
+ Timed image capture - for longer experiments
+ Light switches on before capture sequence and off afterward

Current version: 1.0

*Documentation in progress.* Camera timer appears to be working well but the camera itself struggles with smaller intervals between pictures (approx. 1/2 seconds) for a long period of time (approx. 30 seconds). Taking less pictures at this short interval, or using a longer interval are two possible ways of overcoming this issue.

#### Requirements
+ Raspberry Pi 3B or 3B+ with the latest version of Raspbian Stretch installed
+ PiCamera v2
+ DaisyDriver

#### Installation
1. Open terminal window and navigate to the directory you want to install DaisyGUI
2. Enter the command `git clone https://github.com/OpenDaisy-Microscopy/DaisyGUI.git`
3. Once this has finished, navigate into the DaisyGUI folder using `cd DaisyGUI`
4. Then run the install script to ensure all required dependencies are installed `bash install.sh`
5. Now, to open DaisyGUI use the command `python3 DaisyGUI.py`
6. When opening DaisyGUI subsequently, you will need to navigate to this directory again and run the command in step 5.

#### To do
+ Add capability to split jpg and raw Bayer data immediately after capture
+ Improve error handling
+ Add support for multiple cameras
+ Refactor code for clarity and readability
+ Test time for longer periods (weeks)
+ Write camera test on load up which uses raspistill to take (and then deletes) a test picture
+ Investigate use of video port for long sequences of shorter gap image captures
+ Investigate a more robust way of determining serial port (currently just hard-coded)

#### Contributions
Feel free to open an issue or send a pull request.
