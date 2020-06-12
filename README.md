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
    * Add a parameter to change how it calculates the change over time: Linear, Exponential, Quadratic
    * Syntax: `vary [knob] [start_frame] [end_frame] [start_value] [end_value] [type]`
    * Ex. `vary tilt 0 100 0 1 pquadratic`
    * Types: `pquadratic`, `nquadratic`, `pexponential`, `nexponential`, `linear`
    * the prefixes p and n denote whether we are speeding up (p) or slowing down (n).
  * New primitive shapes
    * Cylinder: `cylinder cx cy cz r h`
    * Cone: `cone cx cy cz r h`

Running the program:
* Just type `make`
* A series of images and gifs will be generated in this order
  * face.mdl: Previous face image, gouraud shading
  * script0.mdl: Previous face image, phong shading
  * script1.mdl: Shuttle created using mesh, flat shading
  * script2.mdl: Shuttle created using mesh, phong shading
  * script3.mdl: Box speeding up using vary (pquadratic)
  * script4.mdl: Box slowing up using vary (nquadratic)
  * script5.mdl: New shapes (cone and cylinder) tiling using vary (pexponential and nexponential)
  * gallery.mdl: Gallery post! The grand finale
    * credits to Lucas Zanotto https://giphy.com/gifs/eyes-character-bouncing-U7KEaEro8JJMFeumBY
