
# PhysicsObject

This class is useful to draw different physical objects that could be rotated and to draw vectors on them.

## Parameters

`angle` - image rotation, in degrees (default: 0)

`source` - source image for display (default: '')

`scale` - scale of image and vectors (default: 1.0)

`color` - image color tint (default: [1,1,1,1])

`constraints` - list `[MIN_X, MAX_X, MIN_Y, MAX_Y]` which holds boundaries for object.
Use `after_update` method to return object to it's boundaries. (default: [0, 100, 0, 100])

`constraint_x` - check for X-axis boundary, (default: True)

`constraint_y` - check for Y-axis boundary, (default: True)

`show_trajectory` - if set to True - draw trajectory of object (default: False)

## Methods

`update(dt)` - if you inherit from PhysicsObject class, you can calculate movement and set object position in this method. Don't forget to call *super* method to calculate trajectory

`clear_trajectory()` - clears object trajectory

`add_vector(self, name, title, length, angle=0.0, color=(1, 1, 1, 1), mode='object')` - adds vector. `mode` parameter is currently not used

`update_vector(self, name, length, angle)` - updates vector with name `name`