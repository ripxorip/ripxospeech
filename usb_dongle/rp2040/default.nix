{ lib, stdenv, cmake, gcc-arm-embedded, pico-sdk, openocd }:

stdenv.mkDerivation rec {
  name = "rp2040";
  src = ./.;

  cmakeFlags = [ ];

  buildInputs = [ gcc-arm-embedded cmake pico-sdk openocd ];
}
