{ lib, pkgs, buildPythonPackage, fetchPypi }:

buildPythonPackage rec {
  pname = "ManimPango";
  version = "0.3.1";

  src = fetchPypi {
    inherit pname version;
    sha256 = "09fc7zv953ni7pilv869ldbjgz59j41a8vbz637rqzjh2yjfb9x3";
  };

  nativeBuildInputs = with pkgs; [
    gcc pkgconfig
  ];

  propagatedBuildInputs = with pkgs; [ pango ]
  ++ (with pkgs.python3Packages; [
    cython pytest numpy pillow
  ]);

  meta = with lib; {};
}
