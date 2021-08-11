from utils import read_file,mount_automata, generate_graph_viz,minimize_automata, print_partition,transform_partitions_on_automata,remove_duplicated_edges

def main(file_name = 'new_sample.txt'):
    file = read_file(file_name)
    fnd = mount_automata(file)
    fnd.print_automata()
    generate_graph_viz(fnd)
    print("***")
    fndm = minimize_automata(fnd)
    print_partition(fndm)
    transform_partitions_on_automata(fndm, fnd)
    remove_duplicated_edges('minimized.gv')



main()