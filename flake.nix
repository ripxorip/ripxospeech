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
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          gst_all_1.gstreamer.dev
          # Video/Audio data composition framework tools like "gst-inspect", "gst-launch" ...
          gst_all_1.gstreamer
          # Common plugins like "filesrc" to combine within e.g. gst-launch
          gst_all_1.gst-plugins-base
          # Specialized plugins separated by quality
          gst_all_1.gst-plugins-good
          gst_all_1.gst-plugins-bad
          gst_all_1.gst-plugins-ugly
          # Plugins to reuse ffmpeg to play almost every video format
          gst_all_1.gst-libav
          # Support the Video Audio (Hardware) Acceleration API
          gst_all_1.gst-vaapi
          #...
          python_pkgs.pygobject3
          python_pkgs.gst-python
          python_pkgs.numpy
          jacktrip
        ];
        nativeBuildInputs = with pkgs; [
          #pkgconfig
          gobject-introspection
          #wrapGAppsHook
          #python3Packages.wrapPython
        ];
      };
      packages.default = pkgs.python3Packages.buildPythonApplication {
        pname = "ripxospeech";
        version = "1.0";
        propagatedBuildInputs = with python_pkgs; [ flask pyserial ];
        src = ./.;
      };
    });
}
