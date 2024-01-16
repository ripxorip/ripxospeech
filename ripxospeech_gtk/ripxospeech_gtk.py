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
        self.counter = 0
        self.timerActive = False

    def attach_backend(self, backend):
        self.backend = backend
        self.backend.set_gui_callback(self.app_callback)

    def on_shutdown(self, app):
        self.backend.teardown()

    def app_callback(self, action):
        print("dictation_callback")
        print(action)

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

        # Obtain the button widget and connect it to a function
        self.startTimerButton = builder.get_object("startTimerButton")
        self.startTimerButton.connect("clicked", self.startTimerButtonClicked)

        finishReportButton = builder.get_object("finishreportbutton")
        finishReportButton.connect("clicked", self.finishReportButtonClicked)

        # Obtain and show the main window
        self.win = builder.get_object("RipxospeechWindow")
        self.win.set_application(self)  # Application will close once it no longer has active windows attached to it
        self.win.present()

    def stopTimer(self):
        self.timerActive = False
        GLib.source_remove(self.timer_id)
        self.timeLabel.set_text("00:00:00")

    def startTimerButtonClicked(self, button):
        self.backend.start_audio_stream()
        return
        if not self.timerActive:
            self.counter = 0
            self.timerActive = True
            self.timer_id = GLib.timeout_add_seconds(1, self.updateCounter)

    def updateCounter(self):
        self.counter += 1
        self.timeLabel.set_text(time.strftime("%H:%M:%S", time.gmtime(self.counter)))  # Update the time label
        return True

    def finishReportButtonClicked(self, button):
        self.backend.stop_audio_stream()
        style_context = self.startTimerButton.get_style_context()
        if style_context.has_class('button-color'):
            style_context.remove_class('button-color')
        else:
            style_context.add_class('button-color')
        return
        reportTime = self.counter
        self.stopTimer()
        # "filename" is defined elsewhere
        dialog = Gtk.MessageDialog(text=f"Error reading something",
                                buttons=Gtk.ButtonsType.CLOSE)

        # "parent_window" is defined elsewhere
        dialog.set_transient_for(self.win)
        dialog.set_destroy_with_parent(True)
        dialog.set_modal(True)
        # Destroy the dialog when the user responds to it
        dialog.connect("response", lambda d: d.destroy())

    def reportButtonClicked(self, button):
        pass

    def resetButtonClicked(self, button):
        self.stopTimer()