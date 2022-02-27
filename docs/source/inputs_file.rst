inputs.yml (or the inputs YAML file)
====================================

The ``inputs.yml`` file is created to be a user-friendly interface for the calculator.

frameofReference
----------------

patternCentroid
^^^^^^^^^^^^^^^

Should include all the information for the centroid of the pattern. 

* ``location``
    * `type`: list with format ``[x,y,z]``
    * `description`: Location of the centroid in the cartesian coordinate system. 
* ``plane``
    * `type`: String. Options include any pair of ``x``, ``y``, and ``z``. 
    * `description`: Plane on which the fastener bottom heads are flush with. For example, in the schematic below, said plane would the ``xy``. In a 2D bolting pattern, the program will determine the plane automatically and error-check the end-user's input plane.

.. image:: figs/bolts_flush.svg

forces
------

force1
^^^^^^
This object is a list element. To make more forces, repeat the fields and syntax found in this element.

* ``force``
    * `type`: String
    * `description`: Name of force
* ``magnitude``: 
    * `type`: List in format ``[x,y,z]``
    * `description`: vector components of force
* ``location``:
    * `type`: List in format ``[x,y,z]``
    * `description`: Point location of force