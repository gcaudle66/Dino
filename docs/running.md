<body>
<h1>Running Dino</h1>

<p>Run the dino.py file to execute app.</p>
----------------
<h1><p>Running AP Rename Intent</p></h1>
<p>From Dino main menu, choose "[1] Bulk AP Rename for Multi-WLC, DNAC Managed Sites"
    Ensure your CSV file is placed in the root directory of Dino app
    Choose the CSV file from the detected files
    After file is parsed, follow prompts to enter connection info for DNA Center
    Allow collection of DNA Center inventory
    From Dino API Main Menu, choose "AP Rename Cont'd - DNAC->CSV Comparison & Finalize"
    Dino will parse and iterate CSV and DNA inventory for mates and create SSH 
        sessions for each WLC necessary
    Follow prompts to connect to each WLC
    Upon completion, log files for each SSH session to WLC is created in root directory
    
    



</body>
