import os
import sys
import gi
import time
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gdk

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(kwargs)
        self.connect('activate', self.on_activate)
        self.connect('shutdown', self.on_shutdown)  # Connect to the shutdown signal

    def attach_backend(self, backend):
        self.backend = backend
        self.backend.set_gui_callback(self.app_callback)

    def on_shutdown(self, app):
        self.backend.teardown()

    def app_callback(self, state):
        # Shall change the state of the GUI and nothin else
        print(state)
        for l in state['labels']:
            self.labels[l].set_text(state['labels'][l])

        for b in state['buttons']:
            style_context = self.buttons[b].get_style_context()

            if b != 'winSV' and b != 'winEN' and b != 'stop':
                if style_context.has_class('button-passive'):
                    style_context.remove_class('button-passive')
                if style_context.has_class('button-active'):
                    style_context.remove_class('button-active')
                if state['buttons'][b]['active']:
                    self.buttons[b].set_label("Running " + state['buttons'][b]['text'] + "...")
                    style_context.add_class('button-active')
                else:
                    self.buttons[b].set_label(state['buttons'][b]['text'])
                    style_context.add_class('button-passive')

    def on_activate(self, app):
        # Create a Builder
        builder = Gtk.Builder()
        # Get the path of the current file
        script_dir = os.path.dirname(__file__)
        # Join the file name to the path
        builder.add_from_file(os.path.join(script_dir, "ripxospeech_gtk_window.ui"))

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(os.path.join(script_dir, "ripxospeech_gtk.css"))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), 
            css_provider, 
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.buttons = {
            'talonCommand': builder.get_object('talonCommand'),
            'talonSentence': builder.get_object('talonSentence'),
            'winRun': builder.get_object('winRun'),
            'winSV': builder.get_object('winSV'),
            'winEN': builder.get_object('winEN'),
            'stop': builder.get_object('stopButton')
        }

        self.labels = {
            'winLang': builder.get_object('winLang'),
            'statusText': builder.get_object('statusText'),
        }

        for button in self.buttons.values():
            button.connect('clicked', self.on_button_clicked)

        # Obtain and show the main window
        self.win = builder.get_object("RipxospeechWindow")
        self.win.set_application(self)  # Application will close once it no longer has active windows attached to it
        self.win.present()

        style_context = self.buttons['stop'].get_style_context()
        style_context.add_class('button-stop')

        # Just to get the initial state correct
        self.backend.gui_button_clicked(None)

    def on_button_clicked(self, button):
        # Call backend gui_button_clicked with the object id
        obj_name = next(name for name, btn in self.buttons.items() if btn == button)
        self.backend.gui_button_clicked(obj_name)
        """
        self.backend.stop_audio_stream()
        style_context = self.talonCommandButton.get_style_context()
        if style_context.has_class('button-color'):
            style_context.remove_class('button-color')
        else:
            style_context.add_class('button-color')
        """
