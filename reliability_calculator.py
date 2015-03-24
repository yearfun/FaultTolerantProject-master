__author__ = 'yearfun'

def sol(mst_list, notused_list, rg, budget):
    notused_list = sorted(notused_list, key=lambda edge: edge.reliability, reverse=True)
    mst_list = sorted(mst_list, key=lambda edge: edge.vertice_1, reverse=True)

    # print notused_list


    r=1;
    cmin=0
    numOfEdges = len(mst_list) + len(notused_list)

    nodes1 = list()
    nodes2 = list()
    test_set = set()
    getGraph(mst_list)

    # cal R for mst
    for edge in mst_list:
        nodes1.append(edge.vertice_1)
        nodes2.append(edge.vertice_2)
        cmin = cmin+float(edge.getCost())
        # print 'edge:'
        # print edge



    for edge in notused_list:
        cmin = cmin+float(edge.getCost())


    # to find the total cities in the network
    nodes = nodes1+nodes2
    nodes1 = set(nodes1)
    # print nodes1
    nodes2 = set(nodes2)
    # print nodes2
    nodes = set(nodes)
    # print(nodes)
    numOfNodes = len(nodes)


    info_mst = trueTable (mst_list, rg, budget, nodes)
    rmst = info_mst.pop()
    cmst = info_mst.pop()

    print 'a)   Meet  a  given  reliability  goal by calculating the reliability for fully connected network '
    all_list = list(mst_list + notused_list)
    info = trueTable (all_list, rg, budget, nodes)
    rmax = info.pop()
    cost = info.pop()
    if rmax < rg:
        print 'cannot meet a given reliability goal since reliability for fully connected network is still smaller than the goal'
    else:
        print 'Network design'
        print info
        print 'Network Reliability'
        print rmax
        print 'Network Cost'
        print cost

    print 'b)   Meet  a  given  reliability  goal  subject  to  a  given  cost  constraint  '
    useful_listb = list(mst_list)
    useless_listb = sorted(notused_list, key=lambda edge: edge.cost, reverse=True)
    if rmst > budget:
        print 'only a) can be found'
    else:
        infob = trueTable (useful_listb, rg, budget, nodes)
        rb = infob.pop()
        cb = infob.pop()
        while rb < rg and cb<budget and len(useless_listb) > 0:
            useful_listb.append(useless_listb.pop())
            infob = trueTable (useful_listb, rg, budget, nodes)
            rb = infob.pop()
            cb = infob.pop()
        print 'Network design'
        print infob
        print 'Network Reliability'
        print rb
        print 'Network Cost'
        print cb



    print 'c)   Maximize  reliability  subject  to  a  given  cost  constraint'
    useful_listc = list(mst_list)
    useless_listc = sorted(notused_list, key=lambda edge: edge.reliability, reverse=True)
    room = budget - money(useful_listc)
    print room
    if money(mst_list) > budget:
        print 'only a) can be found'
    else:
        while money(useless_listc) > room:
            useless_listc.pop()
        print useless_listc
        try_listc = list(useful_listc + useless_listc)
        print try_listc
        infoc = trueTable (try_listc, rg, budget, nodes)
        rtryc = infoc.pop()
        costc = infoc.pop()
        print 'Network design'
        print infoc
        print 'Network Reliability'
        print rtryc
        print 'Network Cost'
        print costc








def trueTable (test_list, rg, budget, nodes):
    test_list = sorted(test_list,  key=lambda edge: edge.reliability, reverse=True)
    # useless_list = sorted(useless_list,  key=lambda edge: edge.reliability, reverse=True)
    testtable = truthtable(len(test_list));

    r = 0
    rtmp = 1
    r_list = []
    allConnected_list = []
    cost = 0



    for edge in test_list:
        r_list.append(edge.reliability)
        cost = edge.cost + cost


    # print 'Rlist'
    # print r_list

    for row in testtable:
        # print 'test table'
        # print row
        oconnected = isAllConnected(row, test_list)
        allConnected_list.append(oconnected)

    # print 'all connected list'
    # print allConnected_list

    for row in testtable:
        for i in xrange(len(test_list)):
            if row[i] :
                row[i] = r_list[i]
            else:
                row[i] = 1- r_list[i]

    # print testtable

    # print 'reliability table'
    # print testtable

    rproduct_list = []
    for row in testtable:
        for i in xrange(len(test_list)):
            rtmp = rtmp*row[i]
        rproduct_list.append(rtmp)
        rtmp = 1

    reliability = 0
    # print rproduct_list

    for i in xrange(len(rproduct_list)):
        reliability = reliability+rproduct_list[i]*allConnected_list[i]
    #
    # print 'calculated reliability'
    # print test_list
    # print reliability
    # print cost
    return [test_list, cost, reliability]




def truthtable (n):
    # n = len(test_list)
    if n < 1:
        return [[]]
    subtable = truthtable(n-1)
    return [ row + [v] for row in subtable for v in [0,1] ]


# graph example {'A': set(['C']), 'C': set(['A', 'B', 'D']), 'B': set(['C', 'E']), 'E': set(['B']), 'D': set(['C'])}

def dfs(graph, start):
    # print 'dfs'
    # print graph
    # print start
    visited = set()
    stack = [start]
    while stack:
        vertex = stack.pop()
        # print graph[vertex]
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    # print visited
    return visited

# dfs(graph, 'A') # {'E', 'D', 'F', 'A', 'C', 'B'}
# print graph


def isAllConnected(truth_list, input_list):
    # connected_list = []
    cities_list = list()
    new_list = []
    test_list = list(input_list)
    # print 'is all connected'
    # print input_list

    for edge in test_list:
        cities_list.append(edge.vertice_1)
        cities_list.append(edge.vertice_2)

    cities_list = set(cities_list)
    cities_list = list(cities_list)
    if len(cities_list) == 0:
        return False

    i = 0
    # print i
    for edge in test_list:
        if truth_list[i] == 0:
            test_list.remove(edge)
        i = i+1

    # print truth_list
    # print test_list

    if len(test_list) >= (len(cities_list)-1):
        test_graph = getGraph(test_list)
    else:
        return 0


    visited_list = dfs(test_graph,cities_list[1])
    # print 'visited cities'
    # print visited_list
    # print cities_list

    if len(cities_list) > len(visited_list):
        return False

    return True

def getGraph(test_list):
    dict_graph = {}
    for edge in test_list:
        if edge.vertice_1 not in dict_graph:
            dict_graph[edge.vertice_1] = set(edge.vertice_2)
            # print dict_graph
        else:
            dict_graph[edge.vertice_1].update(set(edge.vertice_2))
            # print dict_graph
        if edge.vertice_2 not in dict_graph:
            dict_graph[edge.vertice_2] = set(edge.vertice_1)
            # print dict_graph
        else:
            dict_graph[edge.vertice_2].update(set(edge.vertice_1))
            # print dict_graph
    # print dict_graph
    for key in dict_graph:
        dict_graph[key] = set(dict_graph[key])

    # print dict_graph
    return dict_graph

def money(list):
    cost = 0
    for edge in list:
        cost = cost+edge.cost
    return cost