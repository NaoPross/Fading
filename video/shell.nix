with import <nixpkgs> {};
let
  manimpango = callPackage manimpango/default.nix {
    buildPythonPackage = pkgs.python3Packages.buildPythonPackage;
    fetchPypi = pkgs.python3Packages.fetchPypi;
  };

  mapbox-earcut = callPackage manimgl/mapbox-earcut.nix {
    buildPythonPackage = pkgs.python3Packages.buildPythonPackage;
    fetchPypi = pkgs.python3Packages.fetchPypi;
  };

  manimgl = callPackage manimgl/default.nix {
    buildPythonApplication = pkgs.python3Packages.buildPythonApplication;
    buildPythonPackage = pkgs.python3Packages.buildPythonPackage;
    fetchPypi = pkgs.python3Packages.fetchPypi;
    pythonOlder = pkgs.python3Packages.pythonOlder;
    manimpango = manimpango;
    mapbox-earcut = mapbox-earcut;
  };

in mkShell {
  buildInputs = [ manimpango manimgl ];
  shellHook = ''
  manimgl qam.py
  '';
}
