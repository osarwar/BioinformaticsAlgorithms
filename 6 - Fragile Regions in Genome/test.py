import numpy as np

def reversal(p, i, k):
    prefix = p[:i]
    suffix = p[k+1:]
    root = p[i:k+1]
    return prefix + map(lambda x: -x, root[::-1]) + suffix

def greedy_sorting(p):
    '''
    CODE CHALLENGE: Implement GREEDYSORTING.
    Input: A permutation P.
    Output: The sequence of permutations corresponding to 
    applying GREEDYSORTING to P, ending with
    the identity permutation.
    '''
    s = []
    for i in range(1,len(p)+1):
        try:
            k = p.index(-i)
            p = reversal(p,i-1,k)
            s.append(p)
        except ValueError:
            k = p.index(i)
            if (k != i-1):
                p = reversal(p,i-1,k)
                s.append(p)
                p = p[:]
                p[i-1] = -p[i-1]
                s.append(p)
    return s

def permutation_list_to_str(p):
    def str_val(i):
        if (i>0):
            return '+'+str(i)
        else:
            return str(i)
    return '(' + ' '.join(map(str_val,p)) + ')'

def permutation_str_to_list(str_p):
    p = map(int,str_p.strip()[1:-1].split(' '))
    return p
        
def format_sequence(s):
    fs = []
    for p in s:
        str_p = permutation_list_to_str(p)
        fs.append(str_p)
    return fs
    

def number_of_breakpoints(p):
        '''
        CODE CHALLENGE: Solve the Number of Breakpoints Problem.
        
        Number of Breakpoints Problem: Find the number of breakpoints in a permutation.
        Input: A permutation.
        Output: The number of breakpoints in this permutation.        
        '''
        adj = 0
        p = [0,] + p + [len(p)+1]
        for i in range(0,len(p)-1):
            if (p[i+1]==p[i]+1):
                adj += 1
        return len(p) - 1 - adj

def permutation_irreductible(p):
    min_bk = number_of_breakpoints(p)
    for i in range(0,len(p)):
        for j in range(i,len(p)):
            bk = number_of_breakpoints(reversal(p,i,j))
            print(min_bk,bk)
            if bk < min_bk:
                return False
    return True
    

def chromosome_to_cycle(p):
    '''
    CODE CHALLENGE: Implement ChromosomeToCycle.
    Input: A chromosome Chromosome containing n synteny blocks.
    Output: The sequence Nodes of integers between 1 and 2n resulting 
    from applying ChromosomeToCycle to Chromosome.
    '''
    nodes = []
    
    for i in p:
        if (i>0):
            nodes.append(2*i-1)
            nodes.append(2*i)
        else:
            nodes.append(-2*i)
            nodes.append(-2*i-1)
    return nodes

def cycle_to_chromosome(nodes):
    '''
    CODE CHALLENGE: Implement CycleToChromosome.
    Input: A sequence Nodes of integers between 1 and 2n.
    Output: The chromosome Chromosome containing n synteny blocks resulting 
    from applying CycleToChromosome to Nodes.
    '''
    p = []
    for j in range(0,len(nodes)/2):
        if nodes[2*j] < nodes[2*j+1]:
            s = j+1
        else:
            s = -(j+1)
        p.append(s)
    return p


def genome_str_to_list(genome):
    lp = []
    for p in genome.split('(')[1:]:
        p = permutation_str_to_list( '(' + p )
        lp.append(p)
    return lp

def colored_edges(genome):
    '''
    CODE CHALLENGE: Implement ColoredEdges.
    Input: A genome P.
    Output: The collection of colored edges in the genome graph of P 
    in the form (x, y).
    '''
    g = []
    for p in genome:
        s = chromosome_to_cycle(p)
        for j in range(int(len(s)/2)):
            head = 1+2*j
            tail = (2+2*j) % len(s)
            e = (int(s[head]),int(s[tail]))
            g.append(e)
    return g
    
def graph_to_genome(g):
    '''
    CODE CHALLENGE: Implement GraphToGenome.
    Input: The colored edges ColoredEdges of a genome graph.
    Output: The genome P corresponding to this genome graph.
    '''
    
    genome = []
    visit = []
    adj = np.zeros(len(g)*2, dtype = np.int)
    for t in g:
        adj[t[0]-1] = t[1]-1
        adj[t[1]-1] = t[0]-1
    
    for t in g:
        orig = t[0]
        if orig in visit:
            continue
        visit.append(orig)
        if (orig%2 == 0):
            closing = orig-1
        else:
            closing = orig+1
        p = []
        i = 0
        while(True):
            if (orig%2 == 0):
                p.append(orig/2)
            else:
                p.append(-(orig+1)/2)
            dest = adj[orig-1]+1
            i = i + 1
            if (i>100):
                assert False
                return
            visit.append(dest)
            if (dest == closing):
                genome.append(p)
                break
            if (dest%2 == 0):
                orig = dest -1
            else:
                orig = dest + 1
            assert orig > 0
            visit.append(orig)
    return genome
  
def colored_edges_cycles(blue, red):
    '''    
    returns all alternating red-blue-edge cycles
    '''
    cycles = []
    size = len(blue)+len(red) 
    adj = np.zeros(shape = (size,2), dtype = np.int)
    visited = np.zeros(shape = size, dtype = np.bool)
    for e in blue:
        adj[e[0]-1,0] = e[1]-1
        adj[e[1]-1,0] = e[0]-1
    for e in red:
        adj[e[0]-1,1] = e[1]-1
        adj[e[1]-1,1] = e[0]-1
    
    for node in range(size):
        if not visited[node]:
            visited[node] = True
            head = node
            cycle = [head+1]
            # arbitrary we start with a blue edge
            color = 0
            while (True):
                node = adj[node,color]
                if (node == head):
                    # cycle found, we got back to the visited head node, 
                    # just break
                    cycles.append(cycle)
                    break
                cycle.append(node+1)
                visited[node] = True
                color = (color+1) % 2
    return cycles

def two_break_distance(P, Q):
    '''
    CODE CHALLENGE: Solve the 2-Break Distance Problem.
    Input: Genomes P and Q.
    Output: The 2-break distance d(P, Q).
    '''
    blue = colored_edges(P)
    red = colored_edges(Q)

    assert len(blue) == len(red)
    assert len(blue)+len(red) == max([element for tupl in blue+red for element in tupl])
    
    size = len(blue)+len(red) 
    
    l = colored_edges_cycles(blue,red)
    return size/2 - len(l)

def two_break_on_genome_graph(g,i,j,k,l):
    '''
    CODE CHALLENGE: Implement 2-BreakOnGenomeGraph.
    Input: The colored edges of a genome graph GenomeGraph, 
    followed by indices i, j, k, and l.
    Output: The colored edges of the genome graph resulting from applying 
    the 2-break operation 2-BreakOnGenomeGraph(GenomeGraph, i, j, k, l).
    '''
    bg = []
    # equivalent and more elegant but not accepted by the grader ...
#    d = {(i,j):(i,k), (j,i):(j,l), (k,l):(k,i), (l,k):(l,j)}    
#    for t in g:
#        if (t in d):
#            bg.append(d[t])
#        else:
#            bg.append(t)
    
    # so do it this way
    rem = ((i,j), (j,i), (k,l), (l,k))
    bg = [ t for t in g if t not in rem]
    bg.append((i,k))
    bg.append((j,l))
    
    return bg

def two_break_on_genome(genome,i,j,k,l):
    '''
    CODE CHALLENGE: Implement 2-BreakOnGenome.
    Input: A genome P, followed by indices i, i', j, and j'.
    Output: The genome P' resulting from applying the 2-break operation
    2-BreakOnGenomeGraph(GenomeGraph, i, i′, j, j′).
    '''
    g = colored_edges(genome)
    g = two_break_on_genome_graph(g,i,j,k,l)
    print("genome graph after break", g)
    genome = graph_to_genome(g)
    return genome


def two_break_sorting(P,Q):
    '''
    CODE CHALLENGE: Solve the 2-Break Sorting Problem.     
    2-Break Sorting Problem: Find a shortest transformation 
    of one genome into another via 2-breaks.
    Input: Two genomes with circular chromosomes on the same 
    set of synteny blocks.
    Output: The collection of genomes resulting from applying 
    a shortest sequence of 2-breaks transforming one genome into the other.
    '''
    red = colored_edges(Q)
    path = [P]
    while two_break_distance(P,Q) > 0:
        cycles = colored_edges_cycles(colored_edges(P),red)
        print(cycles)
        for c in cycles:
            if len(c) >= 4:
                P = two_break_on_genome(P,c[0],c[1],c[3],c[2])
                path.append(P)
                break     
        # break      
    return path

file = open(r"2BreakSort_sample.txt", "r")
file = open(r"dataset_397361_5.txt", "r")
file = open(r"2BreakSorting_test.txt", "r")
# file = open(r"dataset_397361_4.txt", "r"))
# file = open(r"2BreakSort_test.txt", "r")
data = file.readlines()

for idx, line in enumerate(data): 
    line = line.strip('\n').strip(')')[1:].split(")(")
    if idx == 0: 
        P = []
        for chromosome in line: 
            chromosome = chromosome.split()
            for idx, elem in enumerate(chromosome): 
                chromosome[idx] = int(elem)
            P.append(chromosome)
    elif idx == 1: 
        Q = []
        for chromosome in line: 
            chromosome = chromosome.split()
            for idx, elem in enumerate(chromosome): 
                chromosome[idx] = int(elem)
            Q.append(chromosome)
    else: 
        pass 
print("Two break on genome graph")
print(two_break_on_genome_graph(colored_edges([[1, -2, -4, 3]]), 1, 6, 3, 8))
print("two break on genome")
print(two_break_on_genome([[1, -2, -4, 3]], 1, 6, 3, 8))
print("TWo break sorting")
print(two_break_sorting(P,Q))