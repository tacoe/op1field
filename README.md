# OP-1 Field Remote Script
Plugging your OP-1 Field into Ableton will turn it into a great portable controller. However by default it only supports notes. 
Install this script to add a range functionality, including transport controls (play, stop, rec), session view navigation, and track toggles. 

The workflow happens to be mine, it might not suit yours. I've kept OP-1's basic octave and pitch bend functionality: left/right arrows to change octave, shift left/right arrow to pitchwheel down/up while playing.

This works with Ableton Live 12. It was tested on MacOS, but should work on Windows as well.

## Installation
(these are the steps on MacOS, for Windows they should be comparable)
1. Open Live, under "Places" in the left-hand browser right-click "User Library" then select "Show in Finder"
2. Create a folder called "MIDI Remote Scripts" if it doesn't exist yet
3. Open finder, enter `cd ` (including space) and drag the midi remote scripts folder, then hit enter
4. Type `git clone https://github.com/tacoe/op1field` if you have git, otherwise download a zip and unpack here. 'op1field' should be a subdirectory of 'MIDI remote scripts'.
5. Close then re-open Live.

## Setup and operation
* In Live's Preferences, go to 'Link, Tempo & MIDI', then in where you have your OP-1 selected as Input, click the Control Surface dropdown and select 'OP1Field'. Tap the PLAY button on your OP-1 Field to verify functionality.
* On your OP-1 Field, press SHIFT-COM, then 2 to go into CTRL mode. Hit SHIFT, turn the BLUE button until it says `01`, the OCHRE button until it says `REL`, and the gray button until it says `ON`.

## Usage
* `REC`: Session record
* `PLAY`: Global play
* `STOP`: Global stop

* `LIFT`: Undo
* `DROP`: Redo
* `SCISSORS`: Delete clip

* `3/LOOP`: Toggle loop
* `METRONOME`: Toggle metronome
* `BUBBLE`: Toggle arranger/session view

* `MIC`: Arm current track. This disarms all other tracks.
* `COM`: Mute or unmute current track (toggle). 
* `ARP`: Solo current track (toggle). This unsolos all other tracks.

Encoders:
* `BLUE`: -
* `OCHRE`: -
* `GRAY`: 
  * when in session: `TURN` to change selected scene, `PUSH` to play selected scene 
  * when in arrange: `TURN` to move the playhead
* `ORANGE`: `TURN` to change selected track
