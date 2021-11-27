{ lib, pkgs, buildPythonPackage, fetchPypi, isPy38, autoPatchelfHook }:

buildPythonPackage rec {
  pname = "numpy_ringbuffer";
  version = "0.2.1";
  src = fetchPypi {
    inherit pname version;
    sha256 = "1vrw38jb3cy9m0c1xxvkk5sf1hpgv58x649a2nnqi9ljdl5wcydc";
  };

  buildInputs =  (with pkgs.python3Packages; [ numpy ]);
}
