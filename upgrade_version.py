"""Upgrades lpminimk3 version.

This script upgrades all the files required for a version
upgrade. The files include:
    - setup.py
    - README.md
    - docs/source/conf.py
    - docs/source/index.rst
    - lpminimk3/__version__.py

This script should only be run on fresh commits so failed
upgrades can easily be reverted.
"""
from argparse import (Action,
                      ArgumentParser,
                      RawDescriptionHelpFormatter)
from collections import namedtuple
import sys
import re
import os
import pathlib
import lpminimk3
from abc import ABC, abstractmethod

# The directory containing this file
ROOT_DIR = pathlib.Path(__file__).parent
RUN_FROM_SHELL = __name__ != "__main__"


class ValidateVersion(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not re.match(r"^\d+\.\d+\.\d+$", values):
            raise ValueError(f"Invalid version format: {values}")
        setattr(namespace, self.dest, values)


class Upgrade(ABC):
    def __init__(self, current_version, new_version):
        if current_version == new_version:
            raise ValueError("Cannot upgrade to "
                             f"current version {current_version}.")
        self._current_version = current_version
        self._new_version = new_version

    @property
    def filename(self):
        return self.filename

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def test(self):
        pass

    def ensure_current_version(self, version, file):
        if version != self._current_version:
            raise ValueError(f"Expected {self._current_version}, "
                             f"but got {version} in {file}")

    def ensure_new_version(self, version, file):
        if version != self._new_version:
            raise ValueError(f"Expected {self._new_version}, "
                             f"but got {version} in {file}")


class VersionUpgrade(Upgrade):
    def __init__(self, current_version, new_version):
        super().__init__(current_version, new_version)
        self._upgrades = [
            SetupUpgrade(self._current_version,
                         self._new_version),
            ReadmeUpgrade(self._current_version,
                          self._new_version),
            SphinxConfUpgrade(self._current_version,
                              self._new_version),
            SphinxIndexUpgrade(self._current_version,
                               self._new_version),
            PackageVersionUpgrade(self._current_version,
                                  self._new_version)
                ]

    def run(self):
        print(f"Upgrading from {self._current_version} "
              f"to {self._new_version} ...")
        for u in self._upgrades:
            u.run()
            print(f"{os.path.basename(u.filename)} upgraded.")
        return self

    def test(self):
        print(f"\nTesting upgrade from {self._current_version} "
              f"to {self._new_version} ...")
        for u in self._upgrades:
            u.test()
            print(f"{os.path.basename(u.filename)} test passed.")
        return self


class SetupUpgrade(Upgrade):
    @property
    def filename(self):
        return str(ROOT_DIR / "setup.py")

    def run(self):
        lines = []
        with open(self.filename, "r") as f:
            lines = f.readlines()

        for index, line in enumerate(lines):
            m = re.match(r"\s*version=\"(.*)\"", line)
            if m:
                version = m.group(1)
                self.ensure_current_version(version,
                                            self.filename)
                lines[index] = re.sub(version, self._new_version, line)
        with open(self.filename, "w") as f:
            f.writelines(lines)
        return self

    def test(self):
        with open(self.filename, "r") as f:
            for line in f.readlines():
                m = re.match(r"\s*version=\"(.*)\"", line)
                if m:
                    version = m.group(1)
                    self.ensure_new_version(version,
                                            self.filename)
        return self


class ReadmeUpgrade(Upgrade):
    @property
    def filename(self):
        return str(ROOT_DIR / "README.md")

    def run(self):
        lines = []
        with open(self.filename, "r") as f:
            lines = f.readlines()

        for index, line in enumerate(lines):
            m = re.search(r"badge\.svg\?branch=v(.*?)\)", line)
            if m:
                version = m.group(1)
                self.ensure_current_version(version,
                                            self.filename)
                lines[index] = re.sub(version, self._new_version, line)
        with open(self.filename, "w") as f:
            f.writelines(lines)
        return self

    def test(self):
        with open(self.filename, "r") as f:
            for line in f.readlines():
                m = re.search(r"badge\.svg\?branch=v(.*?)\)", line)
                if m:
                    version = m.group(1)
                    self.ensure_new_version(version,
                                            self.filename)
        return self


class SphinxConfUpgrade(Upgrade):
    @property
    def filename(self):
        return str(ROOT_DIR / "docs/source/conf.py")

    def run(self):
        lines = []
        with open(self.filename, "r") as f:
            lines = f.readlines()

        for index, line in enumerate(lines):
            m = re.match(r"^release\s*=\s*'v(.*)'$", line)

            if m:
                version = m.group(1)
                self.ensure_current_version(version,
                                            self.filename)
                lines[index] = re.sub(version, self._new_version, line)
        with open(self.filename, "w") as f:
            f.writelines(lines)
        return self

    def test(self):
        with open(self.filename, "r") as f:
            for line in f.readlines():
                m = re.match(r"^release\s*=\s*'v(.*)'$", line)
                if m:
                    version = m.group(1)
                    self.ensure_new_version(version,
                                            self.filename)
        return self


class SphinxIndexUpgrade(Upgrade):
    @property
    def filename(self):
        return str(ROOT_DIR / "docs/source/index.rst")

    def run(self):
        lines = []
        with open(self.filename, "r") as f:
            lines = f.readlines()

        for index, line in enumerate(lines):
            m = re.search(r"badge\.svg\?branch=v(.*)$", line)
            if m:
                version = m.group(1)
                self.ensure_current_version(version,
                                            self.filename)
                lines[index] = re.sub(version, self._new_version, line)

        with open(self.filename, "w") as f:
            f.writelines(lines)

        return self

    def test(self):
        with open(self.filename, "r") as f:
            for line in f.readlines():
                m = re.search(r"badge\.svg\?branch=v(.*)$", line)
                if m:
                    version = m.group(1)
                    self.ensure_new_version(version,
                                            self.filename)
        return self


class PackageVersionUpgrade(Upgrade):
    @property
    def filename(self):
        return str(ROOT_DIR / "lpminimk3/__version__.py")

    def run(self):
        lines = []
        with open(self.filename, "r") as f:
            lines = f.readlines()

        for index, line in enumerate(lines):
            m = re.match(r"VERSION\s*=\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\s*\)",
                         line)
            if m:
                major, minor, patch = m.group(1, 2, 3)
                version = f"{major}.{minor}.{patch}"
                self.ensure_current_version(version,
                                            self.filename)
                major, minor, patch = (re.match(r"(\d+)\.(\d+)\.(\d+)",
                                                self._new_version)
                                       .group(1, 2, 3))
                lines[index] = f"VERSION = ({major}, {minor}, {patch})\n"

        with open(self.filename, "w") as f:
            f.writelines(lines)

        return self

    def test(self):
        with open(self.filename, "r") as f:
            for line in f.readlines():
                m = re.match(r"VERSION\s*=\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\s*\)",  # noqa
                             line)
                if m:
                    major = m.group(1)
                    minor = m.group(2)
                    patch = m.group(3)
                    version = f"{major}.{minor}.{patch}"
                    self.ensure_new_version(version,
                                            self.filename)
        return self


def main(*, new_version=""):
    """Upgrades lpminimk3 version.

    Parameters
    ----------
    new_version : str
        Version to upgrade to.

    Raises
    ------
    ValueError
        If same version is set.
        If version set does not follow the SemVer spec.
    """
    args = None
    try:
        if RUN_FROM_SHELL and new_version:
            Args = namedtuple("Args", ["u"])
            args = Args(new_version)

        args = args if args else sys.argv[1:]
        current_version = lpminimk3.__version__

        parser = ArgumentParser(description=__doc__,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-u",
                            action=ValidateVersion,
                            type=str,
                            metavar="NEW_VERSION",
                            help=("Version to upgrade to "
                                  "(format: major.minor.patch) "
                                  "(e.g. 0.1.2)"))
        parser.add_argument("--version",
                            action="version",
                            version="%(prog) 0.1")
        if len(args):
            args = (args if RUN_FROM_SHELL
                    else parser.parse_args(args))
            if args.u:
                VersionUpgrade(current_version,
                               args.u).run().test()
                print("\nUpgrade successful. "
                      "Run 'git diff' to confirm changes.")
        else:
            parser.print_help()
            print(f"\nCurrent lpminimk3 version: {current_version}")
            return 1
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
