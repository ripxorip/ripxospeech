{ lib
, python3Packages
, gtk4
, libadwaita
, wrapGAppsHook4
, gobject-introspection
, virtual_keyboard
}:
with python3Packages;
buildPythonApplication {
  pname = "Ripxospeech gtk4 GUI";
  version = "1.0";

  nativeBuildInputs = [ gobject-introspection wrapGAppsHook4 libadwaita gtk4 virtual_keyboard ];

  propagatedBuildInputs = [ pygobject3 pyserial libadwaita gtk4 pytesseract virtual_keyboard ];

  src = ./.;
}