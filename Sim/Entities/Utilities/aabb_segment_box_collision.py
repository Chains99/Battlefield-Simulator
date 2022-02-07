
def sign(value):
    if value < 0:
        return -1
    return 1


def detect_box_segment_collision_diagonal(box_center_p, box_half_dim, start_p, end_p):

    pos = start_p
    delta = (end_p[0] - start_p[0], end_p[1] - start_p[1])

    scale_x = 1.0/delta[1]
    scale_y = 1.0/delta[0]

    sign_x = sign(scale_x)
    sign_y = sign(scale_y)

    near_time_x = (box_center_p[1] - sign_x*(box_half_dim[1]) - pos[1])*scale_x
    near_time_y = (box_center_p[0] - sign_y*(box_half_dim[0]) - pos[0])*scale_y
    far_time_x = (box_center_p[1] + sign_x*(box_half_dim[1]) - pos[1])*scale_x
    far_time_y = (box_center_p[0] + sign_y*(box_half_dim[0]) - pos[0])*scale_y

    near_time = max(near_time_x, near_time_y)
    far_time = min(far_time_x, far_time_y)

    if near_time_x > far_time_y or near_time_y > far_time_x:
        return False

    if near_time >= 1 or far_time <= 0:
        return False

    return True


def detect_box_segment_collision_vertical(box_center_p, start_p, end_p):

    if box_center_p[1] != start_p[1]:
        return False

    if start_p[0] <= box_center_p[0] <= end_p[0] or end_p[0] <= box_center_p[0] <= start_p[0]:
        return True


def detect_box_segment_collision_horizontal(box_center_p, start_p, end_p):

    if box_center_p[0] != start_p[0]:
        return False

    if start_p[1] <= box_center_p[1] <= end_p[1] or end_p[1] <= box_center_p[1] <= start_p[1]:
        return True


# Parametros:
#   box_center_p: punto que define el centro de la caja
#   box_half_dim: distancia del centro a los lados de la caja
#   start_p: punto inicial del segmento
#   end_p: punto final del segmento
def detect_box_segment_collision(box_center_p, box_half_dim, start_p, end_p):

    # Si el segmento es horizontal
    if start_p[0] == end_p[0]:
        return detect_box_segment_collision_horizontal(box_center_p, start_p, end_p)
    # Si el segmento es vertical
    if start_p[1] == end_p[1]:
        return detect_box_segment_collision_vertical(box_center_p, start_p, end_p)

    return detect_box_segment_collision_diagonal(box_center_p, box_half_dim, start_p, end_p)



