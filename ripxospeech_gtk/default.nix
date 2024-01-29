{ lib
, python3Packages
, gtk4
, libadwaita
, wrapGAppsHook4
, gst_all_1
, gobject-introspection
, virtual_keyboard
}:
with python3Packages;
buildPythonApplication {
  pname = "Ripxospeech gtk4 GUI";
  version = "1.0";

  nativeBuildInputs = [ gst_all_1.gstreamer gst_all_1.gst-plugins-base gst_all_1.gst-plugins-good gst_all_1.gst-plugins-bad gst_all_1.gst-plugins-ugly gst_all_1.gst-libav gobject-introspection wrapGAppsHook4 libadwaita gtk4 virtual_keyboard ];

  propagatedBuildInputs = [ pygobject3 pyserial libadwaita gtk4 pytesseract virtual_keyboard ];

  src = ./.;
}