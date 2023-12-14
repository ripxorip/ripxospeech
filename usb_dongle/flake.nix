{
  description = "Embedded software for the USB dongle firmware.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/release-23.05";
    flake-utils.url = "github:numtide/flake-utils";

    nix-formatter-pack.url = "github:Gerschtli/nix-formatter-pack";
    nix-formatter-pack.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs =
    { self
    , nixpkgs
    , nix-formatter-pack
    , flake-utils
    }:

    flake-utils.lib.eachDefaultSystem (system:

    let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [ ];
      };

      pico_openocd = pkgs.callPackage ./pico_openocd { };
      rp2040 = pkgs.callPackage ./rp2040 { openocd = pico_openocd; };

      python_pkgs = ps: with ps; [ future ];

    in
    {
      formatter = pkgs.nixpkgs-fmt;

      devShells.default = with pkgs; pkgs.mkShell {
        packages = [ pico_openocd ];
      };

      devShells.rp2040_debug = pkgs.mkShell {
        packages = [ pico_openocd ];
      };

      devShells.mavgen = pkgs.mkShell {
          packages = [ (pkgs.python3.withPackages python_pkgs) ];
      };

      packages = {
        rp2040 = rp2040;
        pico_openocd = pico_openocd;
      };
    });
}
