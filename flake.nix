{
  description = "Nix environment for my speech library";

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
          python_pkgs.pyserial
          jacktrip
        ];
        nativeBuildInputs = with pkgs; [
          #pkgconfig
          gobject-introspection
          #wrapGAppsHook
          #python3Packages.wrapPython
        ];
      };

      packages.ripxospeech_gtk = ripxospeech_gtk;
      packages.virtual_keyboard = virtual_keyboard;

      packages.default = pkgs.python3Packages.buildPythonApplication {
        pname = "ripxospeech";
        version = "1.0";
        propagatedBuildInputs = with python_pkgs; [ flask pyserial ];
        src = ./.;
      };
    });
}
