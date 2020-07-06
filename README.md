# Dino

# Concept
IOS-XE and DNA Center API utility for various functions such as bulk renmaming APs spread across several WLCs all managed by DNA Center

# Purpose 
Help network engineers utilize APIs and scripting easier. This app is designed to be a "base" of cose for connecting to API and SSH
on certain network devices. With this base, it is easy for engineers to simply write a module to perform the specific task
desired without having to write all base code. 

# Workflows
-AP Rename - 
  1. Allow bulk renaming of access points on a single IOS-XE 9800 series controller via an imported CVS containing targer AP MAC, new AP Name. 
  This app imports the file, user inputs WLC that is beleived to have APs matching CSV registered, 
  2. Allow bulk renaming of access points on multiple IOS-XE 9800 series controller, managed by DNA-Center via an imported CVS containing targer AP MAC, new AP Name.
  3. Connect to APIs of DNA-Center for various functions
  
It is a work in progress
