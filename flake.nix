{
  description = "Nix environment for my speech library";

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

      python_pkgs = pkgs.python3Packages;

    in
    {
      formatter = pkgs.nixpkgs-fmt;
      packages.default = pkgs.python3Packages.buildPythonApplication {
        pname = "ripxospeech";
        version = "1.0";
        propagatedBuildInputs = with python_pkgs; [ flask pyserial ];
        src = ./.;
      };
    });
}
