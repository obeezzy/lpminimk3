"""High-level rendering API for the Launchpad Mini MK3's surface.

This module provides high-level access to rendering on the Launchpad Mini MK3.

The Launchpad must be open and put in "programmer" mode before any API calls
are made. (See help for `lpminimk3` module for more details.)

Examples
--------
Render "A" on the Launchpad's surface:
    >>> lp.grid.render(Text('A'));

Scroll "Hello, world" on the Launchpad's surface indefinitely:
    >>> lp.grid.render(Text(' Hello, world').scroll());

Scroll "Hello, world" on the Launchpad's surface once:
    >>> lp.grid.render(Text(' Hello, world').scroll(count=1));

Render "Smiley" bitmap on the Launchpad's surface:
    >>> lp.grid.render(Bitmap('/path/to/smiley.bitmap.json'));

Render first frame of "Ping/Pong" movie on the Launchpad's surface:
    >>> lp.grid.render(Movie('/path/to/ping_pong.movie.json'));

Play "Ping/Pong" movie on the Launchpad's surface indefinitely:
    >>> lp.grid.render(Movie('/path/to/ping_pong.movie.json').play());

Play "Ping/Pong" movie on the Launchpad's surface once at a frame rate of 10:
    >>> lp.grid.render(Movie('/path/to/ping_pong.movie.json').play(framerate=10));
"""

from ._graphics import Text,\
                       Bitmap,\
                       Movie,\
                       Frame,\
                       Renderable,\
                       ScrollDirection,\
                       FlipAxis  # noqa
