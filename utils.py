
from Automata import Automata
from Edge import Edge
from State import State
import graphviz
import itertools

def read_file(filename):
    f = open(filename, "r")
    return f


def mount_automata(file):
    states = []
    states_name = []
    edges = []
    symbols = []
    for index,row in enumerate(file):
        if(index == 0):
            row = row.replace("\n", "")
            row = row.split(" ")
            row.pop(1)
            for index, ele in enumerate(row):
                if index == 0:
                    initial_state = State(ele,final=False,initial=True)
                    states.append(initial_state)
                    states_name.append(initial_state.name)
                else:
                    final_state = State(ele,final=True,initial=False)
                    states.append(final_state)
                    states_name.append(final_state.name)
        else:
            row = row.replace("\n", "")
            row = row.split(' ')
            state_origin = State(row[0],final=False,initial=False)
            state_destiny = State(row[2],final=False,initial=False)
            symbol = row[1]
            if symbol not in symbols:
                symbols.append(symbol)
            if state_origin.name not in states_name:
                states.append(state_origin)
                states_name.append(state_origin.name)
            if state_destiny.name not in states_name:
                states.append(state_destiny)
                states_name.append(state_destiny.name)


            edge = Edge(state_origin,state_destiny,row[1])
            edges.append(edge)
    fnd = Automata(states,edges,symbols)
    return fnd


def generate_graph_viz(automata):
    dot = graphviz.Digraph()
    dot.node('start',style='invis') #gera um nó invisível para melhor visualização
    for state in automata.states:
        if(state.is_initial()):
            dot.edge('start',state.name)
        if(state.is_final()):
            dot.node(state.name, shape='doublecircle')
    for edge in automata.edges:
        dot.edge(edge.origin.name, edge.destiny.name, edge.symbol)
    
    dot.save('sample.gv') 


def initialize_partition(automata):
    partition = [[] for i in range(len(automata.states))] # a quantidade maxima possível de partições é a própria quantidade de estados existentes
    for index,ele in enumerate(automata.states):
        partition[index] = []
    for state in automata.states:
        if state.is_final():
            partition[1].append(state)
        else:
            partition[0].append(state)
    return partition


def is_on_same_partition(state_one,state_two,partition):
    list_index_stater_one = 0
    list_index_stater_two = 0
    founded_state_one = False
    founded_state_two = False
    for index,row in enumerate(partition):
        for state in row:
            if state.name == state_one.name: #caso eu tenha encontrado o estado 1
                list_index_stater_one = index
                founded_state_one = True
            elif state.name == state_two.name: #caso eu tenha encontrado o estado 2
                list_index_stater_two = index
                founded_state_two = True
            elif state_one.name == state_two.name:
                return True
        if (founded_state_one and founded_state_two) and (list_index_stater_one == list_index_stater_two): #caso tenha encontrado os dois estados e os index são iguais
            return True
    return False


def print_partition(partition):
    for index,row in enumerate(partition):
        for state in row:
            print("[" + str(state.name) + "] on index " + str(index))


def get_states_name_from_row(row):
    states_name = []
    for state in row:
        states_name.append(state.name)
    return states_name


def remove_estados_duplicados(states_list):
    temp_list = []

    for i in states_list:
        if i not in temp_list:
            temp_list.append(i)
    return temp_list

def make_edge_between_states(automata,list,dot, state,name):
    for symbol in automata.symbols: #pega o estino do estado atual para todos os simbolos existentes
                destiny = automata.get_destiny(state,symbol)
                for states_name in list:
                    for state_name in states_name: #anda pelos nós finais
                        if state_name == destiny.name:
                            dot.edge(str(name), str(states_name), symbol)
    
def transform_partitions_on_automata(partition, automata):
    dot = graphviz.Digraph()
    finals = []
    initials = []
    others = []

    for index,row in enumerate(partition):
        
        others.append(get_states_name_from_row(row))
        for state in row:
            if state.is_final():
                finals.append(get_states_name_from_row(row))
                if( get_states_name_from_row(row) in others):
                    others.remove(get_states_name_from_row(row))
            if state.is_initial():
                initials.append(get_states_name_from_row(row))
                if( get_states_name_from_row(row) in others):
                    others.remove(get_states_name_from_row(row))


    initials = [e for e in initials if e]
    finals = [e for e in finals if e]
    others = [e for e in others if e]
    initials = remove_estados_duplicados(initials)
    finals = remove_estados_duplicados(finals)
    others = remove_estados_duplicados(others)
    dot.node('start',style='invis') 


    for states_name_initials in initials:
        for state_name_initial in states_name_initials: #INICIALIZA OS NÓS INICIAIS GERANDO UMA EDGE INVISIVEL PARA ELA
            state = automata.get_state_by_name(state_name_initial)
            dot.edge('start',str(states_name_initials))
            
            make_edge_between_states(automata,finals,dot, state, states_name_initials)
            make_edge_between_states(automata,others,dot, state, states_name_initials)
            make_edge_between_states(automata,initials,dot, state, states_name_initials)

                            
    for states_name_finals in finals:
        for state_name_final in states_name_finals: #INICIALIZA OS NÓS INICIAIS GERANDO UM NODE WITH DOUBLE CIRCLE
            state = automata.get_state_by_name(state_name_final)
            dot.node(str(states_name_finals),shape='doublecircle')

            make_edge_between_states(automata,finals,dot, state, states_name_finals)
            make_edge_between_states(automata,others,dot, state, states_name_finals)
            make_edge_between_states(automata,initials,dot, state, states_name_finals)

    
    for states_name_others in others:
        for state_name_other in states_name_others: #INICIALIZA OS NÓS INICIAIS GERANDO UMA EDGE INVISIVEL PARA ELA
            state = automata.get_state_by_name(state_name_other)

            make_edge_between_states(automata,finals,dot, state, states_name_others)
            make_edge_between_states(automata,others,dot, state, states_name_others)
            make_edge_between_states(automata,initials,dot, state, states_name_others)
                    
    dot.save('minimized.gv')
            



def create_dict_states_lists(automata):
    dict = {}
    for state in automata.states:
        dict[state.name] = []
    return dict

def split_new_partition(automata, equivalence_lists, partition):
    for state in automata.states: #passar por todos os estados do automato
        for index,row in enumerate(partition):
            #for state in row:
            if state in partition[index]: #get o index da partição em que o estado se encontra
                if len(equivalence_lists[str(state.name)]) == len(partition[index])-1: #-1 pois desconsideramos o estado atual e estamos olhando apenas para a adjacencia
                    count_equivalences = 0
                    for equivalence in equivalence_lists[str(state.name)]:
                            if(equivalence in partition[index]): #verifica se as equivalências estão dentro da partition e a cada equivalencia que esteja eu somo 1, se no fim o contador ficar do mesmo tamanho de len(partition[index])-1 então não faço mudanças na partition
                                count_equivalences += 1

                    if count_equivalences <= len(partition[index])-1: #caso a partition não precise ser alterada (todas as equivalencias estão corretas)
                        pass
                    else:
                        for idx,row in enumerate(partition):
                            if(len(row) == 0):
                                partition[index].remove(state) #retira o estado da partição
                                row.append(state) #adiciona o estado na nova partição
                                
                                for equivalence in equivalence_lists[str(state.name)]:
                                    partition[index].remove(equivalence)
                                    partition[index]
                                    row.append(equivalence)
                                break
                        print("\n")
                else: #caso a lista de equivalencia seja menor que a partition
                    for idx,row in enumerate(partition):
                            if(len(row) == 0):
                                partition[index].remove(state) #retira o estado da partição
                                row.append(state) #adiciona o estado na nova partição
                                for equivalence in equivalence_lists[str(state.name)]:
                                    for state_eq in equivalence:
                                        partition[index].remove(state_eq)
                                        row.append(state_eq)
                                break
    return partition


def minimize_automata(automata):
    print("\n Minimizando o automato \n")
    
    partition = initialize_partition(automata)
    n = 1
    flag_modified = True
    equivalence_lists = create_dict_states_lists(automata)

    while(flag_modified):
        equivalence_lists = create_dict_states_lists(automata)
        flag_modified = False
        for index,row in enumerate(partition):
            if len(row) >= 2: #caso a partição tenha pelo menos 2 estados
                permutation = itertools.permutations(row,2)
                for element in permutation:
                    count_equivalence = 0
                    for symbol in automata.symbols:
                        if(is_on_same_partition(automata.get_destiny(element[0],symbol),automata.get_destiny(element[1],symbol),partition)): #caso o destino dos dois estados na mesma partição vão para estados que também estão numa mesma partição
                            count_equivalence += 1
                    if(count_equivalence == len(automata.symbols)): # caso os dois estados, processando todos os simbolos do automato, tem como destino estados que estão, também, numa mesma partição
                        print(element[0].name + "," + element[1].name + " são " + str(n) + " equivalentes")
                        equivalence_lists[str(element[0].name)].append([element[1]])
                    else:
                        if [element[1]] in equivalence_lists[str(element[0].name)]:
                            equivalence_lists[str(element[0].name)].remove([element[1]])
                        if [element[0]] in equivalence_lists[str(element[1].name)]:
                            equivalence_lists[str(element[1].name)].remove([element[0]])
                        print(element[0].name + "," + element[1].name + " não são " + str(n) + " equivalentes")
                        flag_modified = True     
        if flag_modified:
            n  += 1
            partition = split_new_partition(automata,equivalence_lists,partition)
        elif not flag_modified:
            print("FIM DA EXECUÇÃO COM N = " + str(n))
            return partition




def remove_duplicated_edges(input_file):
    with open(input_file, "r") as fp:
        lines = fp.readlines()
        new_lines = []
        for line in lines:
            #- Strip white spaces
            line = line.strip()
            if line not in new_lines:
                new_lines.append(line)
    output_file = "minimized.gv"
    with open(output_file, "w") as fp:
        fp.write("\n".join(new_lines))
            
    