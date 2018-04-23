from PIL import Image, ImageDraw


class CircleDrawer:
    def __init__(self, circle_graph):
        self.cg = circle_graph

        self.max_x = max(circ.x + circ.r for circ in circle_graph.circles)
        self.min_x = min(circ.x - circ.r for circ in circle_graph.circles)
        self.max_y = max(circ.y + circ.r for circ in circle_graph.circles)
        self.min_y = min(circ.y - circ.r for circ in circle_graph.circles)
        self.width = int(round(self.max_x - min(0, self.min_x)))
        self.height = int(round(self.max_y - min(0, self.min_y)))
        self.check_dim()
        self.x_offset = abs(min(0, self.min_x))
        self.y_offset = abs(min(0, self.min_y))
        self.image = Image.new("RGB", (self.width, self.height), color=(255, 255, 255))
        self.drawer = ImageDraw.Draw(self.image)

    def check_dim(self):
        if(self.width > 2000 or self.height > 2000):
            raise Exception("WARNING GOT DIM: " + str((self.width, self.height)))

    def point_offset(self, coord):
        return (coord[0] + self.x_offset, coord[1] + self.y_offset)

    def pf(self, coord):
        return self.point_offset(coord)

    def draw(self, neighbor_lines=True, intersect_pts=True, bounding_circle=True):
        if neighbor_lines:
            self.cg.create_adj()

        if bounding_circle:
            # add later
            bound = self.cg.get_bounding_circle()
            self.drawer.ellipse([self.pf((bound.x - bound.r, bound.y - bound.r)),
                                 self.pf((bound.x + bound.r, bound.y + bound.r))
                                    ], outline=(0,255,0))


        for index, circ in enumerate(self.cg.circles):

            self.drawer.ellipse([self.pf((circ.x - circ.r, circ.y - circ.r)),
                                 self.pf((circ.x + circ.r, circ.y + circ.r))],
                                outline=0,  # black
                                fill=None)

            for adj_index, adj_entry in enumerate(self.cg.adj_m[index]):
                if adj_entry == 1:
                    neighbor_circle = self.cg.circles[adj_index]
                    if neighbor_lines:
                        self.drawer.line([self.pf((circ.x, circ.y)),
                                          self.pf((neighbor_circle.x, neighbor_circle.y))],
                                         fill=(0, 0, 255),
                                         width=1)

                    if intersect_pts:
                        for p in circ.intersect(neighbor_circle):
                            self.drawer.rectangle([self.pf((p[0] - 1, p[1] - 1)),
                                                   self.pf((p[0] + 1, p[1] + 1))],
                                                  fill=(255, 0, 0))

        self.save()

        return self.image

    def save(self, name=None):
        self.image.save("ex.png" if name is None else name)
