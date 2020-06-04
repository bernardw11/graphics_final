from display import *
from matrix import *
from gmath import *


def draw_scanline_shading(x0, z0, x1, z1, y, screen, zbuffer, color, vertices, view, ambient, light, symbols, reflect, shading):
    if x0 > x1:
        tx = x0
        tz = z0
        x0 = x1
        z0 = z1
        x1 = tx
        z1 = tz
        vertices = [vertices[1], vertices[0]]

    x = x0
    z = z0

    #ok so here. xr yg zb could be the x y z of the normals if it's phong shading,
    #OR they could be the r g b if it's gouraud shading. becasue essentially what
    #is going on is regardless of phong or gouraud, something is being incremented
    #and that something is in the parameter vertices. depending on whether shading
    #is "gouraud" or "phong", they are either the rgb or xyz. fuck this bullshit.
    xr = vertices[0][0]
    yg = vertices[0][1]
    zb = vertices[0][2]
    #changes in the vertices
    dxr = (vertices[1][0] - vertices[0][0]) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0
    dyg = (vertices[1][1] - vertices[0][1]) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0
    dzb = (vertices[1][2] - vertices[0][2]) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0

    while x <= x1:
        if shading == 'gouraud':
            gcolor = [ int(xr), int(yg), int(zb)]
            plot(screen, zbuffer, gcolor, x, y, z)

        elif shading == 'phong':
            colors = get_lighting([xr,yg,zb], view, ambient, light, symbols, reflect)
            plot(screen, zbuffer, colors, x, y, z)


        x += 1
        z += (z1 - z0) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0

        # update values based on those slopes
        if shading == 'gouraud' or shading == 'phong':
            xr += dxr
            yg += dyg
            zb += dzb

def scanline_convert_shading(polygons, point, screen, zbuffer, view, ambient, light, symbols, reflect, vectors, shading):
    flip = False
    BOT = 0
    TOP = 2
    MID = 1
    FIN = 3

    points = [ (polygons[point][0], polygons[point][1], polygons[point][2], vectors[0] ),
               (polygons[point+1][0], polygons[point+1][1], polygons[point+1][2], vectors[1]),
               (polygons[point+2][0], polygons[point+2][1], polygons[point+2][2], vectors[2]) ]

    points.sort(key = lambda x: x[1])
    x0 = points[BOT][0]
    z0 = points[BOT][2]
    x1 = points[BOT][0]
    z1 = points[BOT][2]
    y = int(points[BOT][1])

    distance0 = int(points[TOP][1]) - y * 1.0 + 1
    distance1 = int(points[MID][1]) - y * 1.0 + 1
    distance2 = int(points[TOP][1]) - int(points[MID][1]) * 1.0 + 1

    dx0 = (points[TOP][0] - x0) / distance0 if distance0 != 0 else 0
    dz0 = (points[TOP][2] - z0) / distance0 if distance0 != 0 else 0
    dx1 = (points[MID][0] - x1) / distance1 if distance1 != 0 else 0
    dz1 = (points[MID][2] - z1) / distance1 if distance1 != 0 else 0

    xr0 = points[BOT][FIN][0]
    xr1 = points[BOT][FIN][0]
    yg0 = points[BOT][FIN][1]
    yg1 = points[BOT][FIN][1]
    zb0 = points[BOT][FIN][2]
    zb1 = points[BOT][FIN][2]

    dxr0 = (points[TOP][3][0] - xr0) / distance0 if distance0 != 0 else 0
    dyg0 = (points[TOP][3][1] - yg0) / distance0 if distance0 != 0 else 0
    dzb0 = (points[TOP][3][2] - zb0) / distance0 if distance0 != 0 else 0
    dxr1 = (points[MID][3][0] - xr0) / distance1 if distance1 != 0 else 0
    dyg1 = (points[MID][3][1] - yg0) / distance1 if distance1 != 0 else 0
    dzb1 = (points[MID][3][2] - zb0) / distance1 if distance1 != 0 else 0

    while y <= int(points[TOP][1]):
        if ( not flip and y >= int(points[MID][1])):
            flip = True

            dx1 = (points[TOP][0] - points[MID][0]) / distance2 if distance2 != 0 else 0
            dz1 = (points[TOP][2] - points[MID][2]) / distance2 if distance2 != 0 else 0
            x1 = points[MID][0]
            z1 = points[MID][2]

            xr1 = points[MID][3][0]
            yg1 = points[MID][3][1]
            zb1 = points[MID][3][2]


            dxr1 = (points[TOP][3][0] - xr1) / distance2 if distance2 != 0 else 0
            dyg1 = (points[TOP][3][1] - yg1) / distance2 if distance2 != 0 else 0
            dzb1 = (points[TOP][3][2] - zb1) / distance2 if distance2 != 0 else 0

            xr1 = points[MID][3][0]
            yg1 = points[MID][3][1]
            zb1 = points[MID][3][2]



        color = None
        vertices = [[xr0, yg0, zb0], [xr1, yg1, zb1]]
        draw_scanline_shading(int(x0), z0, int(x1), z1, y, screen, zbuffer, color, vertices, view, ambient, light, symbols, reflect, shading)

        x0+= dx0
        z0+= dz0
        x1+= dx1
        z1+= dz1


        xr0 += dxr0
        yg0 += dyg0
        zb0 += dzb0
        xr1 += dxr1
        yg1 += dyg1
        zb1 += dzb1

        y+= 1


#special shading functions ^^ for gouraud and phong
#normal functions below for flat
##################################################################################################################



def draw_scanline(x0, z0, x1, z1, y, screen, zbuffer, color):
    if x0 > x1:
        tx = x0
        tz = z0
        x0 = x1
        z0 = z1
        x1 = tx
        z1 = tz

    x = x0
    z = z0
    delta_z = (z1 - z0) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0

    while x <= x1:
        plot(screen, zbuffer, color, x, y, z)
        x+= 1
        z+= delta_z

def scanline_convert(polygons, i, screen, zbuffer, color):
    flip = False
    BOT = 0
    TOP = 2
    MID = 1

    points = [ (polygons[i][0], polygons[i][1], polygons[i][2]),
               (polygons[i+1][0], polygons[i+1][1], polygons[i+1][2]),
               (polygons[i+2][0], polygons[i+2][1], polygons[i+2][2]) ]

    # alas random color, we hardly knew ye
    #color = [0,0,0]
    #color[RED] = (23*(i/3)) %256
    #color[GREEN] = (109*(i/3)) %256
    #color[BLUE] = (227*(i/3)) %256

    points.sort(key = lambda x: x[1])
    x0 = points[BOT][0]
    z0 = points[BOT][2]
    x1 = points[BOT][0]
    z1 = points[BOT][2]
    y = int(points[BOT][1])

    distance0 = int(points[TOP][1]) - y * 1.0 + 1
    distance1 = int(points[MID][1]) - y * 1.0 + 1
    distance2 = int(points[TOP][1]) - int(points[MID][1]) * 1.0 + 1

    dx0 = (points[TOP][0] - points[BOT][0]) / distance0 if distance0 != 0 else 0
    dz0 = (points[TOP][2] - points[BOT][2]) / distance0 if distance0 != 0 else 0
    dx1 = (points[MID][0] - points[BOT][0]) / distance1 if distance1 != 0 else 0
    dz1 = (points[MID][2] - points[BOT][2]) / distance1 if distance1 != 0 else 0

    while y <= int(points[TOP][1]):
        if ( not flip and y >= int(points[MID][1])):
            flip = True

            dx1 = (points[TOP][0] - points[MID][0]) / distance2 if distance2 != 0 else 0
            dz1 = (points[TOP][2] - points[MID][2]) / distance2 if distance2 != 0 else 0
            x1 = points[MID][0]
            z1 = points[MID][2]

        #draw_line(int(x0), y, z0, int(x1), y, z1, screen, zbuffer, color)
        draw_scanline(int(x0), z0, int(x1), z1, y, screen, zbuffer, color)
        x0+= dx0
        z0+= dz0
        x1+= dx1
        z1+= dz1
        y+= 1



def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0)
    add_point(polygons, x1, y1, z1)
    add_point(polygons, x2, y2, z2)

def draw_polygons( polygons, screen, zbuffer, view, ambient, lights, symbols, reflect, shading ):
    if len(polygons) < 2:
        print ('Need at least 3 points to draw')
        return

    point = 0
    if shading == 'gouraud' or shading == 'phong':
        normals = {}

        pts = 0
        for pts in polygons:
            normals[tuple(pts)] = [0,0,0]

        pts = 0

        while point < len(polygons) - 2:
            normal = calculate_normal(polygons, point)[:]
            normalize(normal)
            normals[tuple(polygons[point])] = [normals[tuple(polygons[point])][0] + normal[0], normals[tuple(polygons[point])][1] + normal[1], normals[tuple(polygons[point])][2] + normal[2]] if tuple(polygons[point]) in normals else normal
            normals[tuple(polygons[point + 1])] = [normals[tuple(polygons[point + 1])][0] + normal[0], normals[tuple(polygons[point + 1])][1] + normal[1], normals[tuple(polygons[point + 1])][2] + normal[2]] if tuple(polygons[point + 1]) in normals else normal
            normals[tuple(polygons[point + 2])] = [normals[tuple(polygons[point + 2])][0] + normal[0], normals[tuple(polygons[point + 2])][1] + normal[1], normals[tuple(polygons[point + 2])][2] + normal[2]] if tuple(polygons[point + 2]) in normals else normal

            point += 3

    point = 0
    while point < len(polygons) - 2:
        face_normal = calculate_normal(polygons, point)[:]
        normalize(face_normal)
        if dot_product(face_normal, view) > 0:
            if shading == 'flat':
                color = get_lighting(face_normal, view, ambient, lights, symbols, reflect)
                scanline_convert(polygons, point, screen, zbuffer, color)
            elif shading == 'gouraud':
                normal0 = normals[tuple(polygons[point])]
                normal1 = normals[tuple(polygons[point + 1])]
                normal2 = normals[tuple(polygons[point + 2])]
                colors = [[0,0,0],[0,0,0],[0,0,0]]
                colors[0] = get_lighting(normal0, view, ambient, lights, symbols, reflect)
                colors[1] = get_lighting(normal1, view, ambient, lights, symbols, reflect)
                colors[2] = get_lighting(normal2, view, ambient, lights, symbols, reflect)
                scanline_convert_shading(polygons, point, screen, zbuffer, view, ambient, lights, symbols, reflect, colors, shading)


            elif shading == 'phong':
                normal0 = normals[tuple(polygons[point])]
                normal1 = normals[tuple(polygons[point + 1])]
                normal2 = normals[tuple(polygons[point + 2])]
                tempNormals = [normal0, normal1, normal2]
                scanline_convert_shading(polygons, point, screen, zbuffer, view, ambient, lights, symbols, reflect, tempNormals, shading)

        point += 3

def add_mesh(polygons, meshfile):
    meshfile_lines = meshfile.readlines()

    #create a list of points (x, y, z) and faces (p1, p2, p3, p4 optional)
    #each point has 3 coordinates
    #each face has 3 or 4 points[] indices.
    points = []
    faces = []
    for line in meshfile_lines:
        elements = line.split()
        if len(elements) > 0:
            if elements[0] == 'v':
                coords = []
                for x in elements[1:]:
                    coords.append(float(x))
                points.append(coords)
            if elements[0] == 'f':
                vertices = []
                for x in elements[1:]:
                    vertices.append(int(x) - 1)
                faces.append(vertices)

    #put everything together: draw triangles btwn the triangles in faces
    #or if each face has four points (quadrilateral geometry),
    #draw two triangles.
    for face in faces:
        #pi means points index
        pi0 = face[0]
        pi1 = face[1]
        pi2 = face[2]
        if len(face) == 3:
            #three points, (0, 1, 2), draw one triangle.
            add_polygon(polygons, points[pi0][0], points[pi0][1], points[pi0][2],
                                  points[pi1][0], points[pi1][1], points[pi1][2],
                                  points[pi2][0], points[pi2][1], points[pi2][2])
        if len(face) == 4:
            pi3 = face[3]
            #four points, (0, 1, 2, 3), draw two triangles.
            # (0, 1, 2)
            add_polygon(polygons, points[pi0][0], points[pi0][1], points[pi0][2],
                                  points[pi1][0], points[pi1][1], points[pi1][2],
                                  points[pi2][0], points[pi2][1], points[pi2][2])
            # (0, 2, 3)
            add_polygon(polygons, points[pi0][0], points[pi0][1], points[pi0][2],
                                  points[pi2][0], points[pi2][1], points[pi2][2],
                                  points[pi3][0], points[pi3][1], points[pi3][2])

def add_box(polygons, x, y, z, width, height, depth):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon(polygons, x, y, z, x1, y1, z, x1, y, z)
    add_polygon(polygons, x, y, z, x, y1, z, x1, y1, z)
    #back
    add_polygon(polygons, x1, y, z1, x, y1, z1, x, y, z1)
    add_polygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1)

    #right side
    add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1)
    add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1)
    #left side
    add_polygon(polygons, x, y, z1, x, y1, z, x, y, z)
    add_polygon(polygons, x, y, z1, x, y1, z1, x, y1, z)

    #top
    add_polygon(polygons, x, y, z1, x1, y, z, x1, y, z1)
    add_polygon(polygons, x, y, z1, x, y, z, x1, y, z)
    #bottom
    add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z)
    add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1)

def add_sphere(polygons, cx, cy, cz, r, step):
    points = generate_sphere(cx, cy, cz, r, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    step += 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):
            p0 = lat * step + longt
            p1 = p0 + 1
            p2 = (p1 + step) % (step * (step - 1))
            p3 = (p0 + step) % (step * (step - 1))

            if longt != step - 2:
                add_polygon(polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p1][0],
                             points[p1][1],
                             points[p1][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2])
            if longt != 0:
                add_polygon(polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2],
                             points[p3][0],
                             points[p3][1],
                             points[p3][2])

def generate_sphere(cx, cy, cz, r, step):
    points = []

    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation / float(step)
        for circle in range(circ_start, circ_stop + 1):
            circ = circle / float(step)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2 * math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2 * math.pi * rot) + cz

            points.append([x, y, z])
    return points

def add_torus(polygons, cx, cy, cz, r0, r1, step):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):
            p0 = lat * step + longt;
            if (longt == (step - 1)):
                p1 = p0 - longt;
            else:
                p1 = p0 + 1;
            p2 = (p1 + step) % (step * step);
            p3 = (p0 + step) % (step * step);

            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p3][0],
                        points[p3][1],
                        points[p3][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2])
            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2],
                        points[p1][0],
                        points[p1][1],
                        points[p1][2])

def generate_torus(cx, cy, cz, r0, r1, step):
    points = []
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation / float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle / float(step)

            x = math.cos(2 * math.pi * rot) * (r0 * math.cos(2 * math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -math.sin(2 * math.pi * rot) * (r0 * math.cos(2 * math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points


def add_cylinder(polygons, cx, cy, cz, r, h, step):
    points = generate_cylinder(cx, cy, cz, r, h, step)
    i = 1
    while i < step + 1:
        top = points[0] #top face
        bottom = points[1] #bottom face
        p1 = i
        p2 = i % step + 1
        add_polygon(polygons,
                    top[0][0], top[0][1], top[0][2],
                    top[p2][0], top[p2][1], top[p2][2],
                    top[p1][0], top[p1][1], top[p1][2])
        add_polygon(polygons,
                    bottom[0][0],bottom[0][1], bottom[0][2],
                    bottom[p1][0], bottom[p1][1], bottom[p1][2],
                    bottom[p2][0], bottom[p2][1], bottom[p2][2])
        add_polygon(polygons,
                    top[p1][0], top[p1][1], top[p1][2],
                    bottom[p2][0], bottom[p2][1], bottom[p2][2],
                    bottom[i][0], bottom[i][1], bottom[i][2])
        add_polygon(polygons,
                    bottom[p2][0], bottom[p2][1], bottom[p2][2],
                    top[p1][0], top[p1][1], top[p1][2],
                    top[p2][0], top[p2][1], top[p2][2])
        i += 1



def generate_cylinder(cx, cy, cz, r, h, step ):
    points = []

    #top face
    top = []
    top.append([cx, cy, cz])
    for i in range(step):
        rot = float(i)/step
        x1 = r * math.cos(2 * math.pi * rot) + cx
        z1 = r * math.sin(2 * math.pi * rot) + cz
        top.append([x1, cy, z1])
    points.append(top)

    #bottom face
    bottom = []
    bottom.append([cx, cy - h, cz])
    for i in range(step):
        rot = float(i)/step
        x1 = r * math.cos(2 * math.pi * rot) + cx
        z1 = r * math.sin(2 * math.pi * rot) + cz
        bottom.append([x1, cy - h, z1])
    points.append(bottom)
    return points


def add_cone(polygons, cx, cy, cz, r, h, step ):
    points = generate_cone(cx, cy, cz, r, h, step)
    p0 = 0 #center of bottom of cone
    p3 = len(points) - 1 #tip of cone
    for i in range(1, step + 1):
        p1 = i
        p2 = i % step + 1
        add_polygon(polygons,
                    points[p0][0], points[p0][1], points[p0][2],
                    points[p1][0], points[p1][1], points[p1][2],
                    points[p2][0], points[p2][1], points[p2][2])
        add_polygon(polygons,
                    points[p3][0], points[p3][1], points[p3][2],
                    points[p2][0], points[p2][1], points[p2][2],
                    points[p1][0], points[p1][1], points[p1][2])


def generate_cone(cx, cy, cz, r, h, step):
    points = []
    points.append([cx, cy, cz])
    for i in range(step):
        rot = float(i)/step
        x = cx + r * math.cos(2 * math.pi * rot)
        z = cz + r * math.sin(2 * math.pi * rot)
        points.append([x, cy, z])
    points.append([cx, cy + h, cz])
    return points


def add_circle(points, cx, cy, cz, r, step):
    x0 = r + cx
    y0 = cy
    i = 1

    while i <= step:
        t = float(i) / step
        x1 = r * math.cos(2 * math.pi * t) + cx;
        y1 = r * math.sin(2 * math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i += 1

def add_curve(points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type):
    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i) / step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i += 1

def draw_lines(matrix, screen, zbuffer, color):
    if len(matrix) < 2:
        print ('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line(int(matrix[point][0]),
                   int(matrix[point][1]),
                   matrix[point][2],
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   matrix[point+1][2],
                   screen, zbuffer, color)
        point += 2

def add_edge(matrix, x0, y0, z0, x1, y1, z1):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point(matrix, x, y, z = 0):
    matrix.append([x, y, z, 1])

def draw_line(x0, y0, z0, x1, y1, z1, screen, zbuffer, color):
    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        zt = z0
        x0 = x1
        y0 = y1
        z0 = z1
        x1 = xt
        y1 = yt
        z1 = zt

    x = x0
    y = y0
    z = z0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)
    wide = False
    tall = False

    if (abs(x1-x0) >= abs(y1 - y0)): #octants 1/8
        wide = True
        loop_start = x
        loop_end = x1
        dx_east = dx_northeast = 1
        dy_east = 0
        d_east = A
        distance = x1 - x + 1
        if (A > 0): #octant 1
            d = A + B / 2
            dy_northeast = 1
            d_northeast = A + B
        else: #octant 8
            d = A - B / 2
            dy_northeast = -1
            d_northeast = A - B

    else: #octants 2/7
        tall = True
        dx_east = 0
        dx_northeast = 1
        distance = abs(y1 - y) + 1
        if (A > 0): #octant 2
            d = A / 2 + B
            dy_east = dy_northeast = 1
            d_northeast = A + B
            d_east = B
            loop_start = y
            loop_end = y1
        else: #octant 7
            d = A / 2 - B
            dy_east = dy_northeast = -1
            d_northeast = A - B
            d_east = -B
            loop_start = y1
            loop_end = y

    dz = (z1 - z0) / distance if distance != 0 else 0

    while (loop_start < loop_end):
        plot(screen, zbuffer, color, x, y, z)
        if ((wide and ((A > 0 and d > 0) or (A < 0 and d < 0))) or
            (tall and ((A > 0 and d < 0) or (A < 0 and d > 0)))):

            x += dx_northeast
            y += dy_northeast
            d += d_northeast
        else:
            x += dx_east
            y += dy_east
            d += d_east
        z += dz
        loop_start += 1
    plot(screen, zbuffer, color, x, y, z)
