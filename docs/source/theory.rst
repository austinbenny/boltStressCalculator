Theory
==============================

Choice of area 
--------------

This calculator uses the tensile stress area of the bolts given by equation

.. math::
  \frac{\pi}{4} \left( d_{nom} - \frac{0.9743}{TPI} \right)

as the preferred area when an area is required. Some manuals also use the "regular" cross-sectional area of the circle in place of the tensile area. In reality, this difference in selected area is only important when computing the tensile and shear stress. The approach taken here is to assume the end-user has knowledge on the characteristics of the fastener; thereby, feeding the calculator more information to make a more accurate solution.

Another important note is that the bolt tensile area is used to compute the shear and tensile stresses. This implies that the shear plane of the fastener is always at the threads. If this is not the case in the particular use case, the shear stress and IR shear do not apply; the end-user must ensure that the shear force from the results is divided by the appropriate area.