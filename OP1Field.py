import Live # type: ignore
import logging
import os
from ableton.v2.control_surface import ControlSurface, Layer, MIDI_CC_TYPE # type: ignore
from ableton.v2.control_surface.components import TransportComponent # type: ignore
from ableton.v2.control_surface.elements import ButtonElement # type: ignore
from ableton.v2.control_surface.components import SessionRecordingComponent as SessionRecordingComponentBase # type: ignore
from ableton.v2.control_surface.control import ButtonControl # type: ignore
from ableton.v2.control_surface import Skin # type: ignore
from ableton.v2.control_surface.elements import Color # type: ignore

logger = logging.getLogger("OP1Field")

B_REC = 0x26
B_PLAY = 0x27
B_STOP = 0x28

B_SS3 = 0x34

B_TALK = 0x05
B_METRO = 0x06

B_COPY = 0x0F
B_PASTE = 0x10
B_CUT = 0x11

B_WAVE = 0x07
B_DRUM = 0x08
B_TAPE = 0x09
B_MIX = 0x0A

B_ENC1 = 0x01
B_ENC2 = 0x02
B_ENC3 = 0x03
B_ENC4 = 0x04

B_ENC1_PUSH = 0x42
B_ENC2_PUSH = 0x43
B_ENC3_PUSH = 0x44
B_ENC4_PUSH = 0x45

B_MIC = 0x30
B_COM = 0x31
B_ARP = 0x1A

class OP1Field(ControlSurface): 
    __doc__ = "OP-1 Field MIDI Controller"
    enc3_pushed = False
    
    def start_logging(self):
        module_path = os.path.dirname(os.path.realpath(__file__))
        log_dir = os.path.join(module_path, "logs")
        if not os.path.exists(log_dir):
            os.mkdir(log_dir, 0o755)
        log_path = os.path.join(log_dir, "OP1Field.log")
        self.log_file_handler = logging.FileHandler(log_path)
        self.log_file_handler.setLevel(self.log_level.upper())
        formatter = logging.Formatter("(%(asctime)s) [%(levelname)s] %(message)s")
        self.log_file_handler.setFormatter(formatter)
        logger.addHandler(self.log_file_handler)
            
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self.skin = Skin(Colors)
        self.log_level = "info"
        self.start_logging()
        logger.info("Init -- OP1Field")

        with self.component_guard():
            self._create_controls()
            self._create_transport()
        self.show_message("OP1 Field controller enabled")
        
    def disconnect(self):
        logger.removeHandler(self.log_file_handler)

    def _create_controls(self):
        self._play_button = ButtonElement(True, MIDI_CC_TYPE, 0, B_PLAY, name=u'Play_Button', skin=self.skin)
        self._record_button = ButtonElement(True, MIDI_CC_TYPE, 0, B_REC, name=u'Record_Button', skin=self.skin)
        self._record_button.add_value_listener(self.record_callback)
        self._stop_button = ButtonElement(True, MIDI_CC_TYPE, 0, B_STOP, name=u'Stop_Button', skin=self.skin)

    def _create_transport(self):
        self._transport = TransportComponent(name=u'Transport')
        self._transport.layer = Layer(
            play_button=self._play_button, 
            stop_button=self._stop_button)
        self._session_recording = SessionRecordingComponent(name=u'Session_Recording')
        self._session_recording.layer = Layer(record_button=self._record_button)

        self._transport.set_loop_button(ButtonElement(True, MIDI_CC_TYPE, 0, B_SS3))
        self._transport.set_metronome_button(ButtonElement(True,MIDI_CC_TYPE, 0, B_METRO))

        self._undo_button = ButtonElement(True, MIDI_CC_TYPE, 0, B_COPY)
        self._undo_button.add_value_listener(self.undo_callback)
        self._redo_button = ButtonElement(True, MIDI_CC_TYPE, 0, B_PASTE)
        self._redo_button.add_value_listener(self.redo_callback)
        self._cut_button = ButtonElement(True, MIDI_CC_TYPE, 0, B_CUT)
        self._cut_button.add_value_listener(self.cut_callback)

        self._sceneselector = ButtonElement(True, MIDI_CC_TYPE, 0, B_ENC3)
        self._sceneselector.add_value_listener(self.sceneselector_callback)
        self._scenelaunch = ButtonElement(True, MIDI_CC_TYPE, 0, B_ENC3_PUSH)
        self._scenelaunch.add_value_listener(self.scenelaunch_callback)

        self._trackselector = ButtonElement(True, MIDI_CC_TYPE, 0, B_ENC4)
        self._trackselector.add_value_listener(self.trackselector_callback)
        self._trackselector = ButtonElement(True, MIDI_CC_TYPE, 0, B_ENC4_PUSH)
        self._trackselector.add_value_listener(self.trackselector_push_callback)
        self._arm_button = ButtonElement(True, MIDI_CC_TYPE, 0, B_MIC)
        self._arm_button.add_value_listener(self.track_arm_callback)
        self._mute_button = ButtonElement(True, MIDI_CC_TYPE, 0, B_COM)
        self._mute_button.add_value_listener(self.track_mute_callback)
        self._solo_button = ButtonElement(True, MIDI_CC_TYPE, 0, B_ARP)
        self._solo_button.add_value_listener(self.track_solo_callback)

        self._viewswitch = ButtonElement(True, MIDI_CC_TYPE, 0, B_TALK)
        self._viewswitch.add_value_listener(self.view_switch)

        #self._patch_synth_button = ButtonElement(True, MIDI_CC_TYPE, 0, B_WAVE)
        #self._patch_synth_button.add_value_listener(self.browse_synth)
        #self._hotswap_button = ButtonElement(True, MIDI_CC_TYPE, 0, B_MIX)
        #self._hotswap_button.add_value_listener(self.enable_hotswap)

        self.song.view.add_selected_track_listener(self.selected_track_changed)
 
    def record_callback(self, value):
        if value == 127:
            self.song.session_record = True
            selected_slot = self.song.view.highlighted_clip_slot
            selected_slot.fire()

    def undo_callback(self, value):
        if(value == 127): 
            self.song.undo()

    def redo_callback(self, value):
        if(value == 127): 
            self.song.redo()

    def cut_callback(self, value):
        if(value == 127): 
            self.song.view.highlighted_clip_slot.delete_clip()
        
    def track_mute_callback(self, value):
        if(value == 127):
            selected_track = self.song.view.selected_track
            selected_track.mute = not selected_track.mute

    def track_solo_callback(self, value):
        if(value == 127):
            selected_track = self.song.view.selected_track
            for track in self.song.tracks: 
                if track != selected_track: 
                    track.solo = False
            selected_track.solo = not selected_track.solo
            
    def track_arm_callback(self, value):
        if(value == 127):
            selected_track = self.song.view.selected_track
            if selected_track.can_be_armed:
                for track in self.song.tracks:
                    if track.can_be_armed and track != selected_track:
                        track.arm = False
                selected_track.arm = not(selected_track.arm)

    def trackselector_callback(self, value):
        if(self.enc3_pushed):
            selected_track = self.song.view.selected_track
            volume_param = selected_track.mixer_device.volume
            step = (volume_param.max - volume_param.min) / 50
            if(value == 1):
                volume_param.value = min(volume_param.value + step, volume_param.max)
            if(value == 127):
                volume_param.value = max(volume_param.value - step, volume_param.min)
        else:
            # if we're on the main track, snap out first
            if self.song.view.selected_track == self.song.master_track:
                self.song.view.selected_track = self.song.tracks[0]
                return

            if(value == 1):
                self.change_active_track(1)
            if(value == 127):
                self.change_active_track(-1)
        
    def trackselector_push_callback(self, value):
        if(value == 127):
            self.enc3_pushed = True
        else:
            self.enc3_pushed = False
        
    def sceneselector_callback(self, value):
        if self.is_session():
            if(value == 1):
                self.change_active_scene(1)
            if(value == 127):
                self.change_active_scene(-1)
        else:
            if(value == 1):
                self.song.current_song_time += 4
            if(value == 127):
                self.song.current_song_time -= 4
            
    def scenelaunch_callback(self, value):
        if(value == 127):
            selected_scene = self.song.view.selected_scene
            selected_scene.fire()
            
    def change_active_track(self, delta):
        current_track = self.song.view.selected_track
        tracks = self.song.tracks

        try:
            current_index = list(tracks).index(current_track)
            next_index = (current_index + delta) % len(tracks)
            self.song.view.selected_track = tracks[next_index]
        except ValueError:
            pass     

    def change_active_scene(self, delta):
        current_scene = self.song.view.selected_scene
        scenes = self.song.scenes
        idx = list(scenes).index(current_scene)

        idx += delta
        if idx < 0: idx = 0
        if idx >= len(scenes): idx = len(scenes)-1

        self.song.view.selected_scene = scenes[idx]

    def clear_track_assignments(self, strip):
        strip.set_volume_control(None)
        strip.set_pan_control(None)
        strip.set_mute_button(None)
        strip.set_solo_button(None)
        strip.set_arm_button(None)

    def selected_track_changed(self):
        return
        #self.clear_track_assignments()
        #self._channel_strip = self._mixer.selected_strip()
        #self._channel_strip.set_solo_button(self._solo_button)
        #if (self._channel_strip._track.can_be_armed):
        #    self._channel_strip.set_arm_button(self._arm_button)

        #if (self._channel_strip._track != self.song.master_track):
        #    self._channel_strip.set_mute_button(self._mute_button)
        #    self._channel_strip.set_solo_button(self._solo_button)


    def view_switch(self, value):
        if(value == 127):
            if self.is_session():
                self.application.view.show_view("Arranger")
            else:
                self.application.view.show_view("Session")

    def enable_hotswap(self, value):
        if(value == 127):
            selected_track = self.song.view.selected_track
            selected_device = selected_track.view.selected_device
            if selected_device:
                self.application.browser.hotswap_target = selected_device

    def browse_synth(self, value):
        if(value == 127):
            self.application.browser.hotswap_target = self.application.browser.instruments

    def is_session(self):
        return self.application.view.is_view_visible("Session")

class SessionRecordingComponent(SessionRecordingComponentBase):
    record_stop_button = ButtonControl()
    @record_stop_button.pressed
    def record_stop_button(self, _):
        self.song.session_record = False

class Colors:
    class DefaultButton:
        On = Color(0)
        Off = Color(0)
        Disabled = Color(0)

    class Transport:
        PlayOn = Color(0)
        PlayOff = Color(0)

    class Recording:
        On = Color(0)
        Off = Color(0)

    class Mixer:
        MuteOff = Color(127)
        MuteOn = Color(0)
        SoloOn = Color(127)
        SoloOff = Color(0)
        
def create_instance(c_instance):
    return OP1Field(c_instance)
