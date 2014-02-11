#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7
from visual import *
import pdb
# length in centimeter
# weight in gram
# time step in second
# before any calculation, remember to convert unit
car_pos = vector(0,-100,0)
velocity = vector(0,0,0)
car_direction = vector(0.2,1,0)
detect_distance = 30
force = 0
m = 500
dt = 0.1

arrow_len = 10
line_width = 1
car_height = vector(0,0,3)
z_shift = vector(0,0,8)


def car_scan(car_pos, car_direction, detect_distance):
    """
    """
    # pdb.set_trace()
    car_pos = car_pos
    car_direction = car_direction
    detect_distance = detect_distance
    scan_range = 10 # might be a function of detect distance
    car.pos = car_pos+car_height
    car.axis = car_direction*car.length
    direction_arrow.pos=car_pos+z_shift
    direction_arrow.axis=arrow_len*car_direction
    detect_direction = car_direction*detect_distance
    scan_direction = scan_range*(cross(detect_direction, z_shift).norm())
    # scan_direction_norm = cross(detect_direction, z_shift).norm()
    # scan_direction = scan_range * scan_direction_norm
    scan_projection_x = scan_direction.dot(vector(1,0,0))
    scan_projection_y = scan_direction.dot(vector(0,1,0))
    div_x = line_width*scan_projection_x/scan_direction.mag
    if div_x == 0:
        scan_line.x = detect_direction[0]
    else:
        scan_line.x = arange(car.pos.x+detect_direction[0]-scan_projection_x, car.pos.x+detect_direction[0]+scan_projection_x, div_x)
    div_y = line_width*scan_projection_y/scan_direction.mag
    if div_y == 0:
        scan_line.y = detect_direction[1]
    else:
        scan_line.y = arange(car_pos.y+detect_direction[1]-scan_projection_y, car_pos.y+detect_direction[1]+scan_projection_y, div_y)
    scan_line.z = 0
    print scan_line.x, scan_line.y, scan_line.z, '..'
    return scan_line

def scan(track, detect_line):
    """
    Calculate intersection of two curve.

    return a list of vector for detected positions.
    """
    detected = []
    for i in range(len(track.pos)):
        distance = mag(detect_line.pos - track.pos[i])
        inside = less(distance, detect_line.radius)
        for j in range(len(inside)):
            if inside[j] == True:
                detected.append(detect_line.pos[j])
    return detected

def strategy(detected):
    """
    input: detected points
    output: steering angle, force
    """
    if len(detected) == 0:
        return 0, 0
    center = detected[len(detected)/2]
    car_to_detected = vector(center.tolist()) - car_pos
    steering_angle = (car_to_detected).diff_angle(car_direction)
    # print steering_angle, car_to_detected, car_direction, '...'
    # pdb.set_trace()
    # if steering_angle == nan:
    #     steering_angle = 0
    # else:
    if car_to_detected.cross(car_direction).z > 0:
        steering_angle = -steering_angle
    return steering_angle, 0

#initialization
car = box(length=30, height=15, width=5, color=color.blue, make_trail=True)
direction_arrow = arrow(color=color.red)
scan_line = curve(radius=line_width, color=color.yellow)
detected_points = []

track = curve(x=0, y=arange(-100, 100, 1), radius=line_width)

for _ in range(2):
# while True:
    # pdb.set_trace()
    rate(1)
    car_direction = car_direction.norm()
    velocity = car_direction*100
    detect_line = car_scan(car_pos, car_direction, detect_distance)
    # print detect_line
    detected = scan(track, detect_line)
    for i in range(len(detected_points[:])):
        detected_points[0].visible = False
        del detected_points[0]
    if len(detected):
        for point in detected:
            detected_points.append(sphere(pos=point, radius=2, color=color.red))
    # print detected_points
    steering_angle, force = strategy(detected)
    car_pos = car_pos + velocity * dt
    car_direction = car_direction.rotate(steering_angle, vector(0,0,1))
    # print car_direction, steering_angle
