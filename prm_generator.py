import numpy as np

from collections import defaultdict

class RoadMapGenerator(object):
    def __init__(self, scene_name, resolution):
        self.scene_name = scene_name
        self.resolution = resolution

    def generate(self, image):
        free_cells = self._get_free_cells(image)
        self._check_collision(free_cells)

    def _get_free_cells(self, image):
        free_cells = {}
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                if np.sum(image[x][y][:]) == 255*3:
                    free_cells[(y, image.shape[0] - 1 - x)] = 1

        return free_cells

    def _check_collision(self, free_cells):
        outfile = open("{}.txt".format(self.scene_name), 'w')
        checked_cells = defaultdict(list)
        edge_dict = defaultdict(dict)
        edges = []
        outfile.write("%d\n" % len(free_cells.keys()))
        for i, pos in enumerate(free_cells.keys()):
            for next_cell in [[0, -1], 
                              [0, 1], 
                              [-1, 0], 
                              [1, 0]]:
                new_x = pos[0] + next_cell[0]
                new_y = pos[1] + next_cell[1]
                new_pos = (new_x, new_y)
                if new_pos in free_cells:
                    checked_cells[pos].append(new_pos)
                    if not ((new_pos in checked_cells[pos]) and \
                            (pos in checked_cells[new_pos])):
                        edge_dict[new_pos][pos] = i
                    else:
                        j = edge_dict[pos][new_pos]
                        edges.append([j, i])
            
            num_edges = len(checked_cells[pos])
            outfile.write("%d %f %f\n" % (num_edges, 
                                          self.resolution*pos[0], 
                                          self.resolution*pos[1]))

        outfile.write('%d\n' % len(edges))
        for edge in edges:
            outfile.write("%d %d\n" % (edge[0], edge[1]))

        outfile.close()

if __name__ == "__main__":
    import imageio
    scene_name = "UTurn"
    wall_image = imageio.imread("../example/{}Walls.png".format(scene_name))
    generator = RoadMapGenerator(scene_name, 0.25)
    generator.generate(wall_image)
                    

         

