=========================
Extended Graphics Support
=========================

:code:`lpminimk3` is also capable of rendering graphics from **bitmaps** and **movies**. These are JSON files that describe the rendering data in a high-level format. Data in these files are grouped as **frames**. A **frame** is a sequence of bits and their color configurations. A **bitmap** file consists of a single frame while a **movie** file consists of a sequence of frames.

Syncing with LP Sketch
======================

If you want to create and edit bitmaps and/or movies with a graphical tool, try `LP Sketch <https://www.github.com/obeezzy/lpsketch>`_. LP Sketch is a free online Launchpad editor specifically designed for use with :code:`lpminimk3`. You can also sync your Launchpad with LP Sketch by starting :code:`lpminimk3`'s sync server:

    .. code-block:: bash

        $ python -m lpminimk3.graphics.sync

Once the server is running, visit the `LP Sketch <https://www.github.com/obeezzy/lpsketch>`_ website to start creating bitmaps and movies live.

Rendering bitmaps and movies
============================

Render :code:`smiley.bitmap.json` on Launchpad's surface:

    .. code-block:: python

        """Render "Smiley" bitmap.
        """

        from lpminimk3 import Mode, find_launchpads
        from lpminimk3.graphics import Bitmap

        lp = find_launchpads()[0]  # Get the first available launchpad
        lp.open()  # Open device for reading and writing on MIDI interface (by default)

        lp.mode = Mode.PROG  # Switch to the programmer mode

        lp.grid.render(Bitmap("/path/to/smiley.bitmap.json"))  # Display bitmap

Render :code:`ping_pong.movie.json` on Launchpad's surface:

    .. code-block:: python

        """Render "Ping/Pong" movie.
        """

        from lpminimk3 import Mode, find_launchpads
        from lpminimk3.graphics import Movie

        lp = find_launchpads()[0]  # Get the first available launchpad
        lp.open()  # Open device for reading and writing on MIDI interface (by default)

        lp.mode = Mode.PROG  # Switch to the programmer mode

        print('Watch movie played on the Launchpad\'s surface.\n'
              'Press Ctrl+C to quit.\n')

        lp.grid.render(Movie("/path/to/ping_pong.movie.json").play())  # Play movie indefinitely

For convenience, you can use the render script, :code:`render.py`:

    .. code-block:: bash

        $ python -m lpminimk3.graphics.render -f /path/to/bitmap/or/movie.json

:code:`render.py` can be used to render text, bitmaps and movies on the Launchpad and on the console. For more options, run:

    .. code-block:: bash

        $ python -m lpminimk3.graphics.render -h
