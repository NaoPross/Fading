{ lib, pkgs, buildPythonApplication, buildPythonPackage, fetchPypi, pythonOlder,
  manimpango, mapbox-earcut }:

buildPythonApplication rec {
  pname = "manimgl";
  version = "1.2.0";

  src = fetchPypi {
    inherit pname version;
    sha256 = "1bsrn72vjzfz3ldh3cjn9r2gxr18408ja2shz50qwh7jnwi8alyb";
  };

  preConfigure = ''
  sed -i '/argparse/d' manimgl.egg-info/requires.txt
  sed -i '/argparse/d' setup.cfg
  '';

  doCheck = false;

  propagatedBuildInputs = [ manimpango mapbox-earcut ] ++ (with pkgs; [
    texlive.combined.scheme-full ffmpeg
  ]) ++ (with pkgs.python3Packages; [
    cython sympy numpy pydub scipy pyyaml pyopengl pyopengl-accelerate moderngl moderngl-window
    matplotlib colour rich screeninfo tqdm validators
  ]);

  disabled = pythonOlder "3.7";

  meta = { };
}
