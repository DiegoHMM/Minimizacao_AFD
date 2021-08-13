from utils import read_file,mount_automata, generate_graph_viz,minimize_automata, print_partition,transform_partitions_on_automata,remove_duplicated_edges
import os
#INSERIR O CAMINHO DO GRAPHVIZ NA LINHA ABAIXO
os.environ["PATH"] += os.pathsep +'C:/Program Files/Graphviz/bin'


def main(file_name = 'input2.txt'):
    try:
        table_file = open("./files/table.txt", "w",encoding='utf-8')
        file = read_file("./files/"+ file_name)
        fnd = mount_automata(file)
        fnd.print_automata()
        generate_graph_viz(fnd)
        fndm = minimize_automata(fnd, table_file)
        print_partition(fndm)
        transform_partitions_on_automata(fndm, fnd)
        remove_duplicated_edges('minimized.dot')
    except:
        print("Automato Inválido")
    

main(input('Nome do arquivo de entrada: (ex.: input1.txt) '))