"""Renders texts, bitmaps and movies on the Launchpad's surface.
"""

import os
import json
import sys
from argparse import (ArgumentParser,
                      FileType,
                      RawDescriptionHelpFormatter)
from lpminimk3 import find_launchpads, Mode
from lpminimk3.graphics import Text, Bitmap, Movie


def render_character(character,
                     *,
                     on_screen=False,
                     lp=None):
    if on_screen:
        Text(character).print()
    elif lp:
        lp.grid.render(Text(character))
    else:
        raise RuntimeError("No Launchpad connected.")


def render_text(text,
                *,
                on_screen=False,
                count=-1,
                lp=None):
    if on_screen:
        Text(text).print()
    elif lp:
        lp.grid.render(Text(text).scroll(count=count))


def render_bitmap(filename, *, on_screen=False, lp=None):
    if on_screen:
        Bitmap(filename).print()
    elif lp:
        lp.grid.render(Bitmap(filename))


def render_movie(filename,
                 *,
                 on_screen=False,
                 count=-1,
                 lp=None):
    if on_screen:
        Movie(filename).print()
    elif lp:
        lp.grid.render(Movie(filename).play(count=count))


def find_lp():
    found_lps = find_launchpads()
    if len(found_lps):
        lp = found_lps[0]
        lp.open()
        lp.mode = Mode.PROG
        return lp
    return None


def _find_art(tag):
    path_prefix = os.path.dirname(os.path.realpath(__file__))
    if tag.startswith("bitmap:"):
        tag = tag.replace("bitmap:", "bitmaps/")
        tag = f"{path_prefix}/{tag}.bitmap.json"
        return tag
    elif tag.startswith("movie:"):
        tag = tag.replace("movie:", "movies/")
        tag = f"{path_prefix}/{tag}.movie.json"
        return tag

    return ""


def _render(args, *, lp=None):
    if args.f or args.t:
        filename = _find_art(args.t)
        filename = (os.path.abspath(args.f.name)
                    if not filename
                    else filename)
        data = None
        with open(filename) as f:
            data = json.load(f)

        if "bitmap" in data:
            render_bitmap(filename,
                          on_screen=args.s,
                          lp=lp)
        elif "frames" in data:
            render_movie(filename,
                         on_screen=args.s,
                         count=args.c,
                         lp=lp)
    elif len(args.text) == 1:
        render_character(args.text,
                         on_screen=args.s,
                         lp=lp)
    else:
        render_text(args.text,
                    on_screen=args.s,
                    count=args.c,
                    lp=lp)


def main(args=None):
    args = args if args else sys.argv[1:]
    try:
        parser = ArgumentParser(description="Render texts, bitmaps, "
                                            "and movies on the "
                                            "Launchpad Mini MK3")
        parser = ArgumentParser(description=__doc__,
                                formatter_class=RawDescriptionHelpFormatter)

        parser.add_argument("-c",
                            type=int,
                            metavar="COUNT",
                            default=1,
                            help="Stop after looping COUNT times")
        parser.add_argument("-f",
                            type=FileType('r', encoding='latin-1'),
                            metavar="FILE",
                            help="Bitmap/movie file to render")
        parser.add_argument("-s",
                            action="store_true",
                            help="Print to screen")
        parser.add_argument("-t",
                            type=str,
                            metavar="TAG",
                            help="Art tag")
        parser.add_argument("text",
                            nargs="?",
                            metavar="TEXT",
                            help="Text to render")
        parser.add_argument("--version",
                            action="version",
                            version="%(prog) 0.1")
        if len(args):
            args = parser.parse_args(args)
            lp = find_lp()
            _render(args, lp=lp)
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        return 1


if __name__ == '__main__':
    sys.exit(main())
