{ lib, pkgs, buildPythonPackage, fetchPypi, isPy38, autoPatchelfHook }:

assert isPy38;

buildPythonPackage rec {
  pname = "dearpygui";
  version = "1.0.2";
  format = "wheel";

  # src = fetchFromGitHub {
  #   owner = "hoffstadt";
  #   repo  = "DearPyGui";
  #   rev = "v${version}";
  #   sha256 = "094s1r1jjgj6512dp5z5gn50m5g5b7qg6c2wgxhjsn38mxivpd2h";
  #   fetchSubmodules = true;
  # };

  src = fetchPypi {
    inherit pname version format;
    python = "cp38";
    abi = "cp38";
    platform = "manylinux1_x86_64";
    sha256 = "10y8a3v135pziknnrzg8x5q5l6p7jvxgva8r8l5vjhdq9p5mxnab";
  };

  # dontUseCmakeConfigure = false;
  # nativeBuildInputs = with pkgs; [ cmake ];
  nativeBuildInputs = [ autoPatchelfHook ];

  buildInputs = (with pkgs; [
    libGL libGL_driver
  ]) ++ (with pkgs.xorg; [
    libX11 libXrandr libXinerama libXcursor libXi
  ]);

  meta = with lib; {};
}
