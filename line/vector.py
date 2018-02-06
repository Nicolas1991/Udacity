from math import sqrt, pi, acos
from decimal import Decimal, getcontext

getcontext().prec = 5


class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'cannot compute an angle of zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'no unique parallel component'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'no unique orthogonal component'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'only defined in two and three dims'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __iter__(self):
        return iter(self.coordinates)

    # def next(self):
    #     if self.start >= len(self.coordinates):
    #         raise StopIteration
    #     item = self.coordinates[self.start]
    #     self.start += 1
    #     return item
    #
    def __getitem__(self, item):
        return self.coordinates[item]

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        new_coordinates = [x + y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, n):
        new_coordinates = [Decimal(n) * x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        coordinates_squared = [x ** 2 for x in self.coordinates]
        return Decimal.sqrt(sum(coordinates_squared))

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0') / magnitude)
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def dot(self, v):
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])

    def angle_with(self, v, in_degree=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radius = acos(u1.dot(u2))
            if in_degree:
                degree_per_redian = Decimal('180.0') / pi
                return angle_in_radius * degree_per_redian
            else:
                return angle_in_radius
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('cannot compute an angle of zero vector')
            else:
                raise e

    def is_parallel_to(self, v):
        return (self.is_zero() or v.is_zero() or self.angle_with(v) == 0 or self.angle_with(v) == pi)

    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def projection(self, v):
        u = v.normalized()
        return u.times_scalar(self.dot(u))

    def component_orthogonal_to(self, v):
        try:
            projection = self.component_parallel_to(v)
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def component_parallel_to(self, b):
        try:
            u = b.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def cross_product(self,v):
        try:
            x1,y1,z1 = self.coordinates
            x2,y2,z2 = v.coordinates
            new_coordinates = [ y1*z2 - y2*z1,
                                -(x1*z2 - x2*z1),
                                x1*y2 - x2*y1]
            return Vector(new_coordinates)
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross_product(v_embedded_in_R3)
            elif (msg == 'too many values to unpack' or
                  msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e

    def area_of_triangle_with(self, v):
        return self.area_of_parallelgram_with(v) / Decimal('2.0')

    def area_of_parallelgram_with(self, v):
        return self.cross_product(v).magnitude()



# v2 = Vector([-9.88, -3.264, -8.159])
# v3 = Vector([-2.155, -9.353, -9.473])
# print v2.is_parallel_to(v3)
# print v2.is_orthogonal_to(v3)
# print v2.projection(v3)
# print(v2.component_orthogonal_to(v3))