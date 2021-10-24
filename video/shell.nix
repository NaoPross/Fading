with import <nixpkgs> {};
let
  manimpango = callPackage ./nix/manimpango.nix {
    buildPythonPackage = pkgs.python3Packages.buildPythonPackage;
    fetchPypi = pkgs.python3Packages.fetchPypi;
  };

  mapbox-earcut = callPackage ./nix/mapbox-earcut.nix {
    buildPythonPackage = pkgs.python3Packages.buildPythonPackage;
    fetchPypi = pkgs.python3Packages.fetchPypi;
  };

  manimgl = callPackage ./nix/manimgl.nix {
    buildPythonApplication = pkgs.python3Packages.buildPythonApplication;
    buildPythonPackage = pkgs.python3Packages.buildPythonPackage;
    fetchPypi = pkgs.python3Packages.fetchPypi;
    pythonOlder = pkgs.python3Packages.pythonOlder;
    manimpango = manimpango;
    mapbox-earcut = mapbox-earcut;
  };

in mkShell {
  buildInputs = [ manimpango manimgl ];
  # shellHook = ''
  # manimgl qam.py
  # '';
}
