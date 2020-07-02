# Dino
IOS-XE and DNA Center API utility for various functions such as bulk renmaming APs spread across several WLCs all managed by DNA Center
Readme

This program is aimed at being a utility for intent based networking and tasks that can be accomplished via an API.
At its current state it is a modified version of the ap_renamerer script but now allows for the ability
to rename APs in bulk that are registered across multiple WLCs all being managed via DNA Center. This program will 
-import APs to be renamed via CSV
-connect to DNAC via API and gather inventory
-parse this inventory and find APs and the WLC they are registered to 
-locate matches between CSV and parsed inventory
-create commands necessary to rename each AP per WLC
-Iterate through list of WLCs and rename each AP

This programs features will be built upon as use cases come about and we are always taking suggestions
