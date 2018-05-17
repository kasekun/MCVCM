
____/\\\\____________/\\\\________/\\\\\\\\\__/\\\________/\\\_______/\\\\\\\\\__/\\\\____________/\\\\__        
 ___\/\\\\\\________/\\\\\\_____/\\\////////__\/\\\_______\/\\\____/\\\////////__\/\\\\\\________/\\\\\\__       
  ___\/\\\//\\\____/\\\//\\\___/\\\/___________\//\\\______/\\\___/\\\/___________\/\\\//\\\____/\\\//\\\__      
   ___\/\\\\///\\\/\\\/_\/\\\__/\\\______________\//\\\____/\\\___/\\\_____________\/\\\\///\\\/\\\/_\/\\\__     
    ___\/\\\__\///\\\/___\/\\\_\/\\\_______________\//\\\__/\\\___\/\\\_____________\/\\\__\///\\\/___\/\\\__    
     ___\/\\\____\///_____\/\\\_\//\\\_______________\//\\\/\\\____\//\\\____________\/\\\____\///_____\/\\\__   
      ___\/\\\_____________\/\\\__\///\\\______________\//\\\\\______\///\\\__________\/\\\_____________\/\\\__  
       ___\/\\\_____________\/\\\____\////\\\\\\\\\______\//\\\_________\////\\\\\\\\\_\/\\\_____________\/\\\__ 
        ___\///______________\///________\/////////________\///_____________\/////////__\///______________\///___

        Multi-Catalogue Visual Cross-Matching


||Foreword.

This software was initially designed and coded by Jesse Allen Swan to facilitate the cross-matching of the ATLAS 1.4 GHz radio source catalogue with DES photometric source catalogue. Since then it has expanded in complexity and generality to work with any two catalogues if the data requirements are satisfied.

Future work will see MCVCM handling as many complimentary data sets as the user desires. For the remainder of this document, I will refer to the master catalogue and pairing catalogue as Radio and Infrared respectively. That is, we will be discussing the cross-matching as if we have a catalogue of Radio sources for which we want an Infrared counterpart. This, of course, is a \fix{double inference} but importantly, the Radio catalogue is our limiting source in this case.

||Utility

Provided with two source catalogues and associated sky images, MCVCM will, in turn, display an interactive plot for the user of a cutout for each source. The user can click the various associated sources from each catalogue in 'phases' dedicated to that catalogue. The software handles the creation of a unique 'MCVCM_tag' which concatenates the ids of the multiple catalogue associations. This string is used once cross-matching is complete to perform groupings and calculations.

The user can change several plotting parameters on-the-fly, as well as optionally provide a comment for each source as well as a confidence flag for later review.

||Data Managment

The ongoing cross-matching results are saved to prevent data loss in the event of a software crash. If the user restores a previous session, a backup of that session is first made in the case of any required roll-backs.

||Setup

Setup.py config file blah blah

||Running the script

Once the setup has been run, and the configuration file edited the script can be tested by running in `demo' mode.

        >> MCVCM -d {field_name}

Demo mode creates a unique `MCVC-DEMO' folder within the working directory which will host the output files of any demo runs.

Under normal operation, the user can

        >> MCVCM {CDFS,ELAIS} [-h] [-v] [-t] [-x] [-d] [--savefigs {png,eps,pdf}]


    The script is designed to be run from within the host folder (i.e., where it is stored along with the './data' folder and a couple of supporting files). This, of course, can be altered by you, but shouldn't be necessary.

    The script is designed to be run with a few flags at choice, and a necessary positional argument choosing 'ELAIS' or 'CDFS'.
    The flags allow for saving of cross-identified final figures (THIS IS TIME CONSUMING AND CAN BE DONE IN BATCH POST-IDENTIFICATION), and output of diagnostic information and timings, as well as allowing identification of sources that were previously skipped.

        usage: ATLASmultiID-SWIREv5.py [-h] [-v] [-t] [-x] [--savefigs {png,eps,pdf}]
                                       {CDFS,ELAIS}

            <infrared ID>*<radio core ID>*m<number of components>*C<component number>

            Examples:
                Infrared host: SWIRE3_J003940.76-432549*EI1896*m3
                Radio host:    SWIRE3_J003940.76-432549*EI1896*m3*C0
                Component #1:  SWIRE3_J003940.76-432549*EI1896*m3*C1
                Component #2:  SWIRE3_J003940.76-432549*EI1896*m3*C2

        output tables are stored in ./MCVCM-tables/
        output figures are stored in ./MCVCM-figs/

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
                                if provided with an extension, saves final IDd
                                figures to that format (e.g. --savefigs png)

||User operations

    \|Key presses during cross-matching
      At any time the user may press one of the following keys or key combinations for the associated effect.
          - {h}
          - {b} Increase the the displayed area of the by 33\% (this will reset current source progress)
          - {s}
          - {f}
          - {r} Reset current progress of source cross-matching and re-draw starting at Phase One
          - {i}
          - {j}
          - {c} Open a dialogue box for the user to enter comments. Such a comment is saved in the final table under
                the column `MCVCM_comment'
          - {1, 2, 3, 4}
          - {shift + x}
          - {shift + q}


||Manual Cross-matching

    The hot-keys for user interaction are chosen so that once practised cross-matching of most sources is fast.

    \|Phase one: Infrared host selection
        The user is presented with a cutout of the infrared postage stamp with radio contours overlaid. Scattered over the top of this image are the Right-Ascension and Declination positions of the infrared catalogue sources within the field of that cutout.
        Radio contour overlaid on the infrared image (where available) with SWIRE infrared catalogue sources marked.
        * if the image isn't showing enough, press 'b' to make the view bigger
        * Click the source that looks like the infrared host, careful not to just do a 'closest is fine'.
            - if there isn't a good candidate that's fine, don't click anything.
        * if you screw up, press 'r' to restart
        * when happy with the infrared host, slap 'spacebar' to continue

    Step two: Radio core
        Same as before, but with radio catalogue sources marked (and now with big black crosshair for the infrared host)
        * if the image isn't showing enough, press 'b' to make the view bigger
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
        This flag allows for source filtering later on. For consistency, please try to abide the following
            1 — Confident that this is the correct infrared host/ radio association
            2 — Likely to be the infrared host the correct infrared host/ radio association
            3 — Only likely infrared candidate, but infrared is ‘misaligned’ with radio: not confident
            4 — Likely correct infrared host, but blended radio contribution from other radio sources

        If it was a run-of-the-mill ID that you're confident with, press 'd' or 'return' to finish this ID. Certainty flag is automatically set to 1
        OTHERWISE:
            press 2,3, or 4 (if you change your mind, that's fine press the new number, and it updates)
            now press 'd' or 'return' to finish this ID

    Step five: Repeat above steps for next source

***************
Safety features
***************

    Finishing
        - the 'd' or 'return' finish doesn't do a thing unless you're in the final 'component ID' phase
    Backups
        - As mentioned, each running of the script creates a backup ID table
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
Other features
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