from utils import read_file,mount_automata, generate_graph_viz,minimize_automata, print_partition,transform_partitions_on_automata,remove_duplicated_edges
import os

os.environ["PATH"] += os.pathsep +'C:/Program Files/Graphviz/bin'


def main(file_name = 'input2.txt'):
    try:
        file = read_file("./files/"+ file_name)
        fnd = mount_automata(file)
        fnd.print_automata()
        generate_graph_viz(fnd)
        fndm = minimize_automata(fnd)
        print_partition(fndm)
        transform_partitions_on_automata(fndm, fnd)
        remove_duplicated_edges('minimized.dot')
    except:
        print("Automato Inválido")
    

main()