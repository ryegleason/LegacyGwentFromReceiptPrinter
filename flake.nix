{
  description = "An automatic proxy printer that enables playing card games with a recipt printer.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    pkgs = nixpkgs.legacyPackages.x86_64-linux;
  in
  {
    devShells.x86_64-linux.default = pkgs.mkShell {
      buildInputs = [
        pkgs.python311
        pkgs.python311Packages.requests
        pkgs.python311Packages.web
        pkgs.python311Packages.pillow
        pkgs.python311Packages.python-escpos
        pkgs.python311Packages.python-dotenv
        pkgs.python311Packages.pyusb
        pkgs.usbutils # For lsusb
      ];
    };
  };
}
