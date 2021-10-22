# vim: set ts=2 sw=2 et:
with import <nixpkgs> {};
let
  dearpygui = callPackage ./dearpygui.nix {
    buildPythonPackage = pkgs.python38Packages.buildPythonPackage;
    fetchPypi = pkgs.python38Packages.fetchPypi;
    isPy38 = pkgs.python38Packages.isPy38;
  };

in mkShell {
  buildInputs = [ dearpygui ] ++ (with pkgs; [
    gnuradio
    python38Packages.setuptools
    # gnuradio block dev dependencies
    cmake ninja pkg-config log4cpp mpir boost175 gmp volk
    python38Packages.pybind11
  ]) ++ (with pkgs.python38Packages; [
    numpy
  ]);
}
