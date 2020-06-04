# graphics_final

Team Members:
* Christy Guan (4th pd)
* Bernard Wang (4th pd)

Features we want to implement:
* Existing, MDL Commands/Features:
  * Mesh
    * Use an external .obj file for polygons
  * Shading
    * Use different shading techniques / calculating I more or less frequently.
    * Ex. Gouraud and Phong Shading
* Additions to MDL that require changes to the language:
  * Change the behavior of vary
    * Add a parameter to change how it calculates the change over time: Linear, Exponential, Logarithmic
    * Syntax: `vary [knob] [start_frame] [end_frame] [start_value] [end_value] [equation]`
    * Ex. `vary tilt 0 100 0 1 2x^2`
  * New primitive shapes
    * Cylinder: `cylinder cx cy cz r h`
    * Cone: `cone cx cy cz r h`
