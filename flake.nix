{
  description = "hoshihoshi: A open source high performance vtubing platform";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.pypi-deps-db = {
    url = "github:DavHau/pypi-deps-db";
    flake = false;
  };
  inputs.mach-nix = {
    url = "github:DavHau/mach-nix";
    inputs = {
      # nixpkgs.follows = "nixpkgs";
      flake-utils.follows = "flake-utils";
      pypi-deps-db.follows = "pypi-deps-db";
    };
  };

  outputs = { self, nixpkgs, flake-utils, ... }@inputs:
    flake-utils.lib.eachDefaultSystem
      (
        system:
        let
          pkgs = import nixpkgs {
            inherit system;
          };
          mach-nix = inputs.mach-nix.lib."${system}";
        in
        {
          packages.hoshihoshi = mach-nix.buildPythonApplication {
            pname = "hoshihoshi";
            version = "0.1.0";
            src = ./.;
            requirements = builtins.readFile ./requirements.txt;

            postInstall = ''
              cp -R hh $out/bin
              cp -R index $out/bin
            '';
          };

          devShell = mach-nix.mkPythonShell {
            requirements = builtins.readFile ./requirements.txt;
          };
        }
      );
}
