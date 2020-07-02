Readme.md

Dino Network Utility
"Manually Helping You to Automate"

Purpose & Reason
-Purpose of this app is simplifying certain programibility functions in networking for engineers.
-Reason....because I wanted to see if I could! And I have enjoyed learning Python. So why not!
 
Goal
-Goal of the project was to create a "base" set of core functions such as API calls and spawning SSH sessions
 that can then be taken and adapted to the specific needs of an engineer by only having to create a small 
 module to add the certain API call for example onto it. Thuis saving engineers the trouble of recreating
 the core set of functions.
 
Did I do it right? Probably not! I am an engineer and new to Pythion but this for some reason has peaked my interest.
I am sure there are lots of easier ways to do some of the things I have done in this app, but I am ok with that
as I learned a lot along the way! There are only a handful of functions in this app that I did not create myself. And if I did
not write it, I gave credit for it. 

Workflows

AP_renamerer - Utility for bulk renaming of APs either on a single IOS-XE WLC or multiple if managed via DNA-Center
-IOS-XE and DNA Center API utility for various functions such as bulk renmaming APs spread across several WLCs all managed by DNA Center Readme

At its current state it is a modified and beefed up version of the ap_renamerer script that allowed users to rename
access points on IOS-XE based 9800 wireless controllers in bulk.  but now allows for the ability to rename APs in bulk that are registered across multiple WLCs all being managed via DNA Center. This program will -import APs to be renamed via CSV -connect to DNAC via API and gather inventory -parse this inventory and find APs and the WLC they are registered to -locate matches between CSV and parsed inventory -create commands necessary to rename each AP per WLC -Iterate through list of WLCs and rename each AP

This programs features will be built upon as use cases come about and we are always taking suggestions



...this is a work in progress!


