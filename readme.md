# **DaisyGUI**
### A graphical user interface to the DaisyDriver open-hardware microscope controller.

Current version: 1.02

*Documentation in progress.* Camera timer appears to be working well but the camera itself struggles with smaller intervals between pictures (approx. 1/2 seconds) for a long period of time (approx. 30 seconds). Taking less pictures at this short interval, or using a longer interval are two possible ways of overcoming this issue.

### To do
+ Improve error handling
+ Add support for multiple cameras
+ Refactor code for clarity and readability
+ Test time for longer periods (weeks)
+ Write camera test on load up which uses raspistill to take (and then deletes) a test picture
+ Investigate use of video port for long sequences of shorter gap image captures

### Contributions
Feel free to open an issue or send a pull request.