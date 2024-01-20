{ lib, stdenv, gcc }:

stdenv.mkDerivation rec {
  name = "virtual_keyboard";
  src = ./.;

  cmakeFlags = [ ];

  buildInputs = [ stdenv gcc ];

  buildPhase = ''
    make
  '';

  installPhase = ''
    mkdir -p $out/bin
    cp virtual_keyboard $out/bin
  '';
}
