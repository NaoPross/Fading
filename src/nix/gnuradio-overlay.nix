self: super: {
  gnuradio = super.gnuradio.override {
    extraPythonPackages = super.lib.attrVals [
      "setuptools"
      # Add more python packages here if you need any.
    ] super.gnuradio.unwrapped.python.pkgs;
  };
}
