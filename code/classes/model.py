from .path import Path

class Model():
    def __init__(self, chip):
        self.chip = chip
        self.paths = self.load_paths(chip)
    
    def load_paths(self, chip):
        paths = {}

        for net in chip.netlist:
            value = Path(chip.netlist[net])
            key = value.connection.id

            paths[key] = value
        
        return paths
    
    def complete_connection(self, net_id):
        return self.paths[net_id].complete()
    
    def valid_moves(self, path):
        chip = self.chip
        gates = [chip.gates[i].position for i in chip.gates]

        moves = path.moves()
        current_node = path.current_node()
        target = path.connection.end.position

        gates.remove(target)

        valid_moves = [p for p in moves if p not in gates]

        l, u = chip.dim
        valid_moves = [p for p in valid_moves if p[0] >= l[0] and p[1] >= l[1]]
        valid_moves = [p for p in valid_moves if p[0] <= u[0] and p[1] <= u[1]]

        valid_moves = self.check_collisions(current_node, valid_moves)

        return valid_moves
    
    def intersections(self, path):
        id = path.connection.id
        path_a = path.segments

        other_paths = [id for id in self.chip.netlist]
        other_paths.remove(id)

        crossings = set()
        for id in other_paths:
            path_b = self.paths[id].wires()

            crossing = [xy for xy in path_a if xy in path_b]
            crossings.update(crossing)
        
        k = len(crossings)

        return k
    
    def check_collisions(self, current_node, moves):
        for net in self.chip.netlist:
            path = self.paths[net]
            segments = path.segments

            if current_node in segments:
                neighbours = path.neighbours(current_node)

                moves = [x for x in moves if x not in neighbours]
        
        return moves
                
    
    def path_cost(self, path):
        length = len(path)

        k = self.intersections(path)

        return length + k * 300
    
    def print_netlist(self):
        for net in self.chip.netlist:
            print(self.chip.netlist[net], self.paths[net])