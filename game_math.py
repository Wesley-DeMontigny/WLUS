import math
import game_types
'''import gem, supposedly this library is good for 3D math but I have no idea how to work it'''


def quat_to_euler(quaternion : game_types.Vector4) -> game_types.Vector3:
	x = quaternion.X
	y = quaternion.Y
	z = quaternion.Z
	w = quaternion.W

	y_sqr = y * y

	t0 = +2.0 * (w * x + y * z)
	t1 = +1.0 - 2.0 * (x * x + y_sqr)
	X = math.degrees(math.atan2(t0, t1))

	t2 = +2.0 * (w * y - z * x)
	t2 = +1.0 if t2 > +1.0 else t2
	t2 = -1.0 if t2 < -1.0 else t2
	Y = math.degrees(math.asin(t2))

	t3 = +2.0 * (w * z + x * y)
	t4 = +1.0 - 2.0 * (y_sqr + z * z)
	Z = math.degrees(math.atan2(t3, t4))

	return game_types.Vector3(float(X), float(Y), float(Z))


#TODO: Fix
def front_vector(rotation : game_types.Vector4, position : game_types.Vector3, magnitude : float = 1.0) -> game_types.Vector3:

	direction = game_types.Vector3(2 * (rotation.X * rotation.Z - rotation.W * rotation.Y),
								   2 * (rotation.Y * rotation.Z - rotation.W * rotation.X),
								   1 - 2 * (rotation.X * rotation.X + rotation.Y * rotation.Y))
	return (position + direction * magnitude)






