import numpy as np


def generate_polyline_buffer(points, dists):
    rot_mat = np.array([[0.0, -1.0], [1.0, 0.0]])
    left = []
    right = []

    if len(dists) != len(points) - 1:
        raise ValueError(
            "Number of distances must be equal to number of segments between the points\n"
            + f"Currently: {len(points) - 1} segments and {len(dists)} distances"
        )

    points = [np.array([p[0], p[1]]) for p in points]
    dists = [(d, d) if np.isscalar(d) else d for d in dists]
    prev_dist = dists[0]
    prev_dir = points[1] - points[0]
    prev_normal = rot_mat @ prev_dir
    prev_normal /= np.linalg.norm(prev_normal)
    last_dir = points[-1] - points[-2]
    points = [
        points[0] - last_dir,
        *points,
        points[-1] + last_dir,
    ]
    next_p = points[1]

    for i in range(1, len(points) - 1):
        p = next_p
        next_p = points[i + 1]
        next_dist = dists[min(i - 1, len(dists) - 1)]
        is_taper_left = next_dist[0] is False
        is_taper_right = next_dist[1] is False
        if is_taper_left:
            next_dist = (prev_dist[0], next_dist[1])
        if is_taper_right:
            next_dist = (next_dist[0], prev_dist[1])
        next_dir = next_p - p
        next_normal = rot_mat @ next_dir
        next_normal /= np.linalg.norm(next_normal)

        A = np.array([prev_normal, next_normal])
        b_left = np.array(
            [
                prev_normal @ p + prev_dist[0],
                next_normal @ p + next_dist[0],
            ]
        )
        b_right = np.array(
            [
                prev_normal @ p - prev_dist[1],
                next_normal @ p - next_dist[1],
            ]
        )

        if np.abs(np.linalg.det(A)) < 1e-4:  # parallel lines
            normal = (prev_normal + next_normal) / 2  # they are actually equal
            left.append(p + (next_dist[0] + prev_dist[0]) / 2 * normal)
            right.append(p - (next_dist[1] + prev_dist[1]) / 2 * normal)
        else:
            A_inv = np.linalg.inv(A)
            left.append(A_inv @ b_left)
            right.append(A_inv @ b_right)

        prev_normal = next_normal
        prev_dist = next_dist
        if is_taper_left:
            prev_dist = (dists[min(i, len(dists) - 1)][0], prev_dist[1])
        if is_taper_right:
            prev_dist = (prev_dist[0], dists[min(i, len(dists) - 1)][1])
        if prev_dist[0] is False or prev_dist[1] is False:
            raise ValueError("Taper segments can't be at the end or follow each other")

    for path in [left, right]:  # let's cleanup the paths
        i_segment = 1
        i_line = 2
        iteration = 0
        local_points = points[:]
        while i_segment < len(path) - 2:
            segment = path[i_segment + 1] - path[i_segment]
            line = local_points[i_line + 1] - local_points[i_line]
            if segment.dot(line) < 0:
                # if one of the segments is inversed, eliminate it and extend the adjacent ones such that they meet
                normal_before = rot_mat @ (path[i_segment] - path[i_segment - 1])
                normal_after = rot_mat @ (path[i_segment + 2] - path[i_segment + 1])
                A = np.array([normal_before, normal_after])
                A_inv = np.linalg.inv(A)
                b = np.array(
                    [
                        normal_before @ path[i_segment],
                        normal_after @ path[i_segment + 1],
                    ]
                )
                path.pop(i_segment + 1)
                path[i_segment] = A_inv @ b
                # in addition, we also need to modify the according segment in the original line
                b = np.array(
                    [
                        normal_before @ local_points[i_line],
                        normal_after @ local_points[i_line + 1],
                    ]
                )
                local_points.pop(i_segment + 1)
                local_points[i_line] = A_inv @ b

                if i_segment > 1:
                    # now that we modified the path, we need to check the previous segment again
                    i_segment -= 1
                    i_line -= 1
                iteration += 1
            else:
                i_segment += 1
                i_line += 1

    return left, right
