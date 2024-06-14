{
  description = "Flake for the rt audio client";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/release-23.11";
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

      python_pkgs = pkgs.python3Packages;
      virtual_keyboard = pkgs.callPackage ./virtual_keyboard {};
      ripxospeech_gtk = pkgs.callPackage ./ripxospeech_gtk {virtual_keyboard = virtual_keyboard;};

    in
    {
      formatter = pkgs.nixpkgs-fmt;
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          gcc
          pkg-config
          pipewire.dev
        ];
      };
    });
}
