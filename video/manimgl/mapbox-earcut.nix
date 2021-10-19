{ lib, pkgs, buildPythonPackage, fetchPypi }:

buildPythonPackage rec {
  pname = "mapbox_earcut";
  version = "0.12.10";
  src = fetchPypi {
    inherit pname version;
    format = "setuptools";
    sha256 = "0ly48lijgd9inq07x42pfp9c24fn16vn9axpmfwqrkn979krbnah";
  };

  dontUseCmakeConfigure = true;

  nativeBuildInputs = with pkgs; [ cmake ];

  buildInputs = with pkgs.python3Packages; [
    setuptools_scm pybind11
  ];

  propagatedBuildInputs = with pkgs.python3Packages; [
    numpy
  ];

  meta = with lib; {};
}
