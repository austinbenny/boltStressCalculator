inputs.yml (or the inputs YAML file)
====================================

The inputs file should be a ``YAML`` or ``.yml`` file. 

There are two kinds (in terms of structure) of input files that this calculator recognizes. If you want to perform a single bolt analysis, the input file should look like :ref:`this <single>`. If you want to perform multiple bolting group analyses, or in other words, if you want to study multiple bolting patterns, you must first create a :ref:`separate input file <single>` for each bolting pattern. The paths to the bolting file can be organized in a single file like :ref:`this <multiple>` which the calculator will recognize. The inputs file must be in the same directory as ``run.py`` or the absolute path to the input file must be specified.

Single Fastener Group Analysis Input File
-----------------------------------------------

projectInformation
^^^^^^^^^^^^^^^^^^^

* ``output_dir``
    * `type`: String. 
    * `description`: Output directory for the results. Results include a ``.csv`` file that contains the resulting structural parameters, an ``.svg`` figure of the bolts, and a ``.html`` file presenting the results.
* ``project_name``
    * `type`: String. 
    * `description`: The name of the case(s)
* ``open_on_completion``
    * *This option is only available for a single bolting group study.*
    * `type`: Boolean. 
    * `description`: Options include "True" or "False". If "True", the ``.html`` file will be opened on completion.


frameofReference
^^^^^^^^^^^^^^^^^^^

* ``plane``
    * `type`: String. Options include any pair of ``x``, ``y``, and ``z``. 
    * `description`: Plane on which the fastener bottom heads are flush with. **The first character should be the axis in the longitudinal (right-left) direction, and the second should be the axis in the latitudinal (up-down) direction.** For example, in the schematic below, said plane would the ``xy``, ``x`` is in the longitudinal direction and ``y`` is the latitudinal axis. In a 2D bolting pattern, the program will determine the plane automatically and error-check the end-user's input plane. **Units**: [inches]

.. image:: figs/bolts_flush.svg

forces
^^^^^^^^^^^^^^^^^^^

force1
"""""""
``force1`` is a list element. To make more forces, repeat the fields and syntax of this element.

* ``force``
    * `type`: String
    * `description`: Name of force. 
* ``magnitude``: 
    * `type`: List in format ``[x,y,z]``
    * `description`: vector components of force. **Units**: [lbf]
* ``location``:
    * `type`: List in format ``[x,y,z]``
    * `description`: Point location of force. **Units**: [inches]

fasteners
^^^^^^^^^^^^^^^^^^^

fastener1
""""""""""
``fastener1`` is a list element. To make more fasteners, repeat the fields and syntax of this element.

* ``bolt``
    * `type`: String
    * `description`: Name of fastener
* ``major_diameter``: 
    * `type`: int, float
    * `description`: nominal or major diameter of fastener. **Units**: [inches]
* ``tpi``: 
    * `type`: int, float
    * `description`: threads-per-inch of fastener. **Units**: [Dimensionless]
* ``Sy``: 
    * `type`: int, float
    * `description`: yield strength of bolt material. **Units**: [Psi]
* ``location``:
    * `type`: List in format ``[x,y,z]``
    * `description`: location of fastener. **Units**: [inches]

Single Fastener Group Analysis Inputs File Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. _single:

The name ``inputs.yml`` is the default name for the inputs file, but this file name can be changed to anything. The ``inputs.yml`` file should be in the same directory as the ``run.py``.

.. code-block:: yaml 

  projectInformation:

    output_dir: '/usr/case/out'
    project_name: 'case1'
    open_on_completion: False

  frameOfReference:

      plane: 'xy'

  forces:

    - force: 'Force1'
      magnitude: [-400,0,0]
      location: [0,-1.20,0]
      
    - force: 'Force2'
      magnitude: [-42000,0,0]
      location: [2,0,0]

  fasteners:

    - bolt: '1/4"-14 TPI bolt at plate edge'
      major_diameter: 0.25
      tpi: 14
      Sy: 30000
      location: [-1.05,0,0]

    - bolt: '1/2"-14 TPI bolt at plate outside'
      major_diameter: 0.5
      tpi: 14
      Sy: 30000
      location: [-0.035,0,0]

Multiple Fastener Group Analysis Input File 
-----------------------------------------------

projectInformation
^^^^^^^^^^^^^^^^^^^

* ``output_dir``
    * `type`: String. 
    * `description`: Output directory for the results. Results include a ``.csv`` file that contains the resulting structural parameters, an ``.svg`` figure of the bolts, and an ``.html`` file presenting the results.
* ``project_name``
    * `type`: String. 
    * `description`: The name of the case(s)

files
^^^^^^

* `type`: List. 
* `description`: A list of single bolting group analysis input files. See below for example.


Multiple Fastener Group Analysis Input File Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. _multiple:

The name ``inputs_queue.yml`` is the default name for the inputs file, but this file name can be changed to anything. All absolute path to the inputs files must be specified.


.. code-block:: yaml 

  projectInformation:

  output_dir: '/usr/case/out/queue'
  project_name: 'multiple_cases'

  files:

    - '/usr/case/inputs1.yml'
    - '/usr/case/inputs2.yml'
    - '/usr/case/inputs3.yml'
    - '/usr/case/inputs4.yml'
    - '/usr/case/inputs5.yml'
    - '/usr/case/inputs6.yml'

