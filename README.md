# MCVCM (Multi-Catalogue Visual Cross-Matching)


***************
# Foreword 
***************
**Currently compatible with python3.6 only**

This software is designed to easily facilitate manual cross-matching of a radio source catalogue, and infrared or optical source catalogue via visual inspection.

Specifically, it iterates through the ATLAS component catalogue generating an infrared-cutout image with radio contours overlaid. 

Selections are made by simply clicking the sources marked on the figure to select:
	- Ifrared host
	- Radio core
	- Any additional radio components 

Each ATLAS component is then given a unique ID that associtates it to the infrared host, radio core. The results of these are automatically saved at small intervals (currently 5 IDs)

Each time the script is run, a backup of the cross-identified catalogue is created and stored in the subfolder './XID_tables' with the suffix (e.g.,) '-bkp-26'
IF AT ANY TIME YOU NEED TO RESTORE TO AN OLD BACKUP, SIMPLY OVERWRITE THE MASTER CATALOGUE (e.g., CDFS_multiXID.dat) with this backup. (and idealy delete and backups numbered greater than the restored backup)

***************
# Running the script:
***************
	the script is designed to be run from within the host folder (i.e., where it is stored along with the './data' folder and a couple of supporting files). This of course can be altered by you, but shouldn't be necessary.

	The script is designed to be run with a few flags at choice, and a necessary positional argument choosing 'ELAIS' or 'CDFS'.
	The flags allow for saving of cross-identified final figures (THIS IS TIME CONSUMING AND CAN BE DONE IN BATCH POST-IDENTIFICATION), and output of diagnostic information and timings, as well as allowing identification of sources that were previously skipped.

		usage: mcvcm [-h] [-v] [-t] [-x] [--savefigs {png,eps,pdf}]
		                               {CDFS,ELAIS}

		********************************************************************************
		Interactive program for catalogue cross-identification.
		Displays infrared heatmap and radio contours with catalogue sources over-laid. 
		Unique tags are generated for each object, in the format:
			<infrared_host_ID>*<radio_host_ID>*m<#_of_components>*C<component_#>
			Examples: 
				Infrared host: SWIRE3_J003940.76-432549.1*EI1896*m2
				Radio host:    SWIRE3_J003940.76-432549*EI1896*m2*C0
				Component #1:  SWIRE3_J003940.76-432549*EI1896*m2*C1
				Component #2:  SWIRE3_J003940.76-432549*EI1896*m2*C2

		output tables are stored in ./XID_tables/
		output figures are stored in ./XID_figs/

		press h in the plotting window for a list of basic controls
		^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

		positional arguments:
		  {CDFS,ELAIS}          Specify if we are working on ELAIS or CDFS

		optional arguments:
		  -h, --help            show this help message and exit
		  -v                    toggles verbose output
		  -t                    toggles output of function timings (requires verbose mode)
		  -x                    if specified, processes only sources marked as 'not_yet_identified'
		  --savefigs {png,eps,pdf}
		                        if provided with an extenstion, saves final IDd
		                        figures to that format (e.g. --savefigs png)

***************
# Doing the identification (AKA Netflix 'n' clicks)
***************
	once practiced, it becomes a quick "*click* *spacebar* *click* *spacebar* `d`" for most sources. 

	Step one: Infrared host
		Radio contour overlaid on infrared image (where avalible) with SWIRE infrared catalogue sources marked. 
		* if image isn't showing enough, press 'b' to make the view bigger
		* Click the source that looks like the infrared host, careful not to just do a 'closest is fine'. 
			- if there isn't a good candidate that's fine, don't click anything. 
		* if you screw up, press 'r' to restart
		* when happy with infrared host, slap 'spacebar' to continue

	Step two: Radio core
		Same as before, but with radio catalogue sources marked (and now with big black crosshair for infrared host)
		* if image isn't showing enough, press 'b' to make the view bigger
		* Click the source that looks like the radio core
			- if there isn't a good candidate that's fine, don't click anything. 
		* if you screw up, press 'r' to restart to step one
		* when happy with radio core, give another tap to 'spacebar'

	Step three: Components
		Same as step 2, except now you're selecting any components associated with this source
		* Click all radio sources that look like components (carefully ignoring sources from a blended background galaxy)	
		* if you screw up, press 'r' to restart to step one
		* when happy with components, give a certainty flag (if necessary)

	Step four: Certainty flag
		This flag allows for source filtering later on. For consistancy please try to abide the following
			1 — Confident that this is the correct infrared host/ radio association
			2 — Likely to be the infrared host the correct infrared host/ radio association
			3 — Only likely infrared candidate, but infrared is ‘misaligned’ with radio: not confident
			4 — Likely correct infrared host, but blended radio contribution from other radio sources

		If it was a run-of-the-mill ID that you're confident with, press 'd' or 'return' to finish this ID. Certainty flag is automatically set to 1
		OTHERWISE:
			press 2,3, or 4 (if you change your mind, that's fine just press the new number and it updates)	
			now press 'd' or 'return' to finish this ID

	Step five: Repeat above steps for next source		

***************
# Safety features
***************
	
	Finishing
		- the 'd' or 'return' finish doesn't do a thing unless you're in the final 'component ID' phase
	Backups 
		- As mentioned, each running of script creates a backup ID table
	Automatic saving of table 
		- Every 5 identifications (so a crash or force-quit won't ruin your day; i've been there)
	Manually saving table 
		- Just press 'shift+s' any 
	Save and quit 
		- Just press 'shift+q' any time (lose only current, unfinished ID)
	Source selection 
		- Can't select the same radio component twice, or select a radio component already chosen as radio core
	No radio core 
		- In order to maintain cataloge association, a core is necessary. However if none was chosen because they were chosen as compoents, the core_ID is 'steals' a component.

***************
# Other features
***************		
Press 'h' in ID window to see avaliable buttons

	zoom-out
		- press 'b' anytime to see more space stuff
	Toggle pesky catalogue source crosses
		- press 't' to toggle catalogue source visiblity on/off (can still be selected when invisible)
	Can't be bothered with this ID
		- Not a problem, hit 'shift-x' and the source gets a temp ID and is skipped. Run script with -x flag later to finish these off!
	Pretty pictures
		- found something interesting? hit f to manually save the as-is current displayed plot (you'll have to do your clicking again though, sorry)
	Source selection 
		- Can't select the same radio component twice, or select a radio component already chosen as radio core
	No radio core 
		- In order to maintain cataloge association, a core is necessary. However if none was chosen because they were chosen as compoents, the core_ID is 'steals' a component.
	Comments
		- press 'c' at anytime to open a dialogue box for inserting a comment wich will be saved to a column 'xid_comment'
		- press 'shift-c' to view the comment for currenc source
