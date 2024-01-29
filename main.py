from code.classes import chip
from code.classes import model as mod

from code.visualization import visualize as vis
from code.visualization import display_data as display
from code.algorithms.netlist_solver import net_solver as ns
from code.algorithms.netlist_solver import shortest_first_solver as sfs
from code.algorithms.netlist_solver import hardest_first_solver as hfs
from code.algorithms.netlist_solver import hillclimber as hc
from code.algorithms.netlist_solver import simulated_annealing as sa

from code.analysis import test1000 as test

if __name__ == "__main__":
    chip_id = 0
    net_id = 1

    chip_file = f'gates&netlists/chip_{chip_id}/print_{chip_id}.csv'
    netlist = f'gates&netlists/chip_{chip_id}/netlist_{net_id}.csv'

    # Create a chip and load in a netlist from our data
    test_chip = chip.Chip(chip_id, chip_file, net_id, netlist)

    # Create a model from our chip to create the connections in
    model = mod.Model(test_chip)
    # ------------------------ Random order astar -------------------
    rno = ns.Random_Net_Order(model)
    print(rno.nets)

    rno.run()
    rno.results()
    vis.vis_solver(rno)

    # ------------------------ baseline test ------------------------
    baseline_test = False
    if baseline_test:
        m, costs, comp = test.run_n(model, ns.Random_Net_Order, 200, save=True)
        display.distribution(costs)
        print(m.nets)
        vis.vis_solver(m)

    # ------------------------ shortest first astar -----------------
    # sno = sfs.Shortest_Net_Order(model)
    # sno.run(pathfinder='standard')
    # sno.results()
    # vis.vis_solver(sno)

    # ------------------------ hardest first astar ------------------
    # hno = hfs.Hardest_Net_Order(model)
    # hno.run(pathfinder='make_space')
    # hno.results()
    # vis.vis_solver(hno)

    # ------------------------ reconnect astar ----------------------
    # reconnected = sfs.Shortest_Net_Order(hno.model)
    # reconnected.run(pathfinder='standard', from_scratch=False)
    # reconnected.results()
    # vis.vis_solver(reconnected)

    # ------------------------ hillclimber --------------------------
    # climber = hc.Hillclimber(rno)
    # climber.run(30, verbose=True)

    # best = climber.best_solution
    # best.results()
    # vis.vis_solver(best)

    # display.cost_decrease(climber)

    # ------------------------ simmulated annealing -----------------
    # simmaneal = sa.Simulated_Annealing(hno, temperature=500)
    # simmaneal.run(30, pathfinder='standard', from_scratch=False, verbose=True)
    
    # best = simmaneal.best_solution
    # best.results()
    # vis.vis_solver(best)

    # display.cost_decrease(simmaneal)
    
    # data = "outputs/test200.txt"
    # display.distribution(display.load_txt(data))