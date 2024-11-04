# OP-1 Field Remote Script
Tested with Ableton Live 12.

## Installation
(these are the steps on MacOS, for Windows they should be comparable)
1. Open Live, under "Places" in the left-hand browser right-click "User Library" then select "Show in Finder"
2. Create a folder called "MIDI Remote Scripts" if it doesn't exist yet
3. Open finder, enter `cd ` (including space) and drag the midi remote scripts folder, then hit enter
4. Type `git clone https://github.com/tacoe/op1field` if you have git, otherwise download a zip and unpack here. 'op1field' should be a subdirectory of 'MIDI remote scripts'.
5. Close then re-open Live.

## Setup
In Live's Preferences, go to 'Link, Tempo & MIDI', then in where you have your OP-1 selected as Input, click the Control Surface dropdown and select 'OP1Field'. Tap the PLAY button on your OP-1 Field to verify functionality.

## Usage
REC: Clip record
PLAY: Global play
STOP: Global stop

LIFT: Undo
DROP: Redo
SCISSORS: Delete clip

3/LOOP: Toggle loop
METRONOME: Toggle metronome
BUBBLE: Toggle arranger/session iew

MIC: arm current track
COM: mute current track (toggle)
ARP: solo current track (toggle)

Encoders:
BLUE: -
OCHRE: -
GRAY: session: select scene (turn) / play scene (push)
GRAY: arrange: move playhead (turn)
ORANGE: select track (turn)
