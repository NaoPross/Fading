# vim: set ts=2 sw=2 et:
with import <nixpkgs> {};
let
  dearpygui = callPackage ./dearpygui.nix {
    buildPythonPackage = pkgs.python38Packages.buildPythonPackage;
    fetchPypi = pkgs.python38Packages.fetchPypi;
    isPy38 = pkgs.python38Packages.isPy38;
  };

in mkShell {
  buildInputs = [ dearpygui ] ++ (with pkgs; []);
}

# (pkgs.buildFHSUserEnv {
#   name = "pipzone";
#   targetPkgs = pkgs: (with pkgs; [
#     python38
#     python38Packages.pip
#     python38Packages.virtualenv
#     libGL
#     libGL_driver
#     xorg.libX11
#   ]);
#   runScript = "bash";
# }).env
