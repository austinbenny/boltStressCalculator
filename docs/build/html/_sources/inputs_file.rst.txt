inputs.yml (or the inputs YAML file)
====================================

The ``inputs.yml`` file is created to be a user-friendly interface for the calculator. This page describes the fields or keys required to make the input file for this calculator. An example inputs.yml file is provided in this directory. The name ```inputs.yml``` is the default name for the inputs file, but this file name can be changed to anything.

frameofReference
----------------

* ``plane``
    * `type`: String. Options include any pair of ``x``, ``y``, and ``z``. 
    * `description`: Plane on which the fastener bottom heads are flush with. For example, in the schematic below, said plane would the ``xy``. In a 2D bolting pattern, the program will determine the plane automatically and error-check the end-user's input plane. **Units**: [inches]

.. image:: figs/bolts_flush.svg

forces
------

force1
^^^^^^
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
----------

fastener1
^^^^^^^^^
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

Example inputs.yml template
----------------------------

.. code-block:: yaml 

  projectInformation:

    output_dir: '/usr/case/out'
    project_name: 'case1'
    output_format: 'html'                      
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
