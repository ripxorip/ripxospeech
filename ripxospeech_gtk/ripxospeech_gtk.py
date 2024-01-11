import sys
import gi
import time
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
        self.counter = 0
        self.timerActive = False

    def on_activate(self, app):
        # Create a Builder
        builder = Gtk.Builder()
        builder.add_from_file("ripxospeech_gtk_window.ui")

        # Obtain the button widget and connect it to a function
        startTimerButton = builder.get_object("startTimerButton")
        startTimerButton.connect("clicked", self.startTimerButtonClicked)

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
        if not self.timerActive:
            self.counter = 0
            self.timerActive = True
            self.timer_id = GLib.timeout_add_seconds(1, self.updateCounter)

    def updateCounter(self):
        self.counter += 1
        self.timeLabel.set_text(time.strftime("%H:%M:%S", time.gmtime(self.counter)))  # Update the time label
        return True

    def finishReportButtonClicked(self, button):
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

app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
