{ lib, stdenv, meson, gettext, gtk4, pkg-config, libadwaita, desktop-file-utils, ninja }:

stdenv.mkDerivation rec {
  name = "ripxospeech_gtk";
  src = ./.;

  cmakeFlags = [ ];

  buildInputs = [ meson gettext gtk4 pkg-config libadwaita desktop-file-utils ninja ];
}
