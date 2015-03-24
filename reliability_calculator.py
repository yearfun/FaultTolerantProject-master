__author__ = 'yearfun'

def sol(mst_list, notused_list, rg, budget):
    notused_list = sorted(notused_list, key=lambda edge: edge.reliability, reverse=True)
    mst_list = sorted(mst_list, key=lambda edge: edge.vertice_1, reverse=True)


    cmin=0


    nodes1 = list()
    nodes2 = list()

    # for debug graph function
    # getGraph(mst_list)

    for edge in mst_list:
        nodes1.append(edge.vertice_1)
        nodes2.append(edge.vertice_2)
        cmin = cmin+float(edge.getCost())




    for edge in notused_list:
        cmin = cmin+float(edge.getCost())


    # to find the total cities in the network
    nodes = nodes1+nodes2
    nodes = set(nodes)
    numOfNodes = len(nodes)


    info_mst = reliabilityTable (mst_list)
    rmst = info_mst.pop()
    cmst = info_mst.pop()

    print 'a)   Meet  a  given  reliability  goal by calculating the reliability for fully connected network '
    all_list = list(mst_list + notused_list)
    info = reliabilityTable (all_list)
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
        infob = reliabilityTable (useful_listb)
        rb = infob.pop()
        cb = infob.pop()
        if rb>= rg:
            print 'minimum spanning tree meets reliability goal and the constrain'
            print 'Network design'
            print infob
            print 'Network Reliability'
            print rb
            print 'Network Cost'
            print cb

        else:
            while rb < rg and cb<budget and len(useless_listb) > 0:
                useful_listb.append(useless_listb.pop())
                infob = reliabilityTable (useful_listb)
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
    uselessLength = len(useless_listc)
    room = budget - money(useful_listc)
    print 'After building the minimum spanning tree we still have $' + str(room)
    if money(mst_list) > budget:
        print 'only a) can be found since '
    else:
        while money(useless_listc) > room:
            useless_listc.pop()

        if uselessLength == len(useless_listc):
            print 'All the not used edges are too expensive to add into the network'
        else:
            try_listc = list(useful_listc + useless_listc)
            infoc = reliabilityTable (try_listc)
            rtryc = infoc.pop()
            costc = infoc.pop()
            print 'Network design'
            print infoc
            print 'Network Reliability'
            print rtryc
            print 'Network Cost'
            print costc








def reliabilityTable (test_list):
    test_list = sorted(test_list,  key=lambda edge: edge.reliability, reverse=True)
    testtable = truthtable(len(test_list));

    r = 0
    rtmp = 1
    r_list = []
    allConnected_list = []
    cost = 0



    for edge in test_list:
        r_list.append(edge.reliability)
        cost = edge.cost + cost

    for row in testtable:
        oconnected = isAllConnected(row, test_list)
        allConnected_list.append(oconnected)



    for row in testtable:
        for i in xrange(len(test_list)):
            if row[i] :
                row[i] = r_list[i]
            else:
                row[i] = 1- r_list[i]


    rproduct_list = []
    for row in testtable:
        for i in xrange(len(test_list)):
            rtmp = rtmp*row[i]
        rproduct_list.append(rtmp)
        rtmp = 1

    reliability = 0


    for i in xrange(len(rproduct_list)):
        reliability = reliability+rproduct_list[i]*allConnected_list[i]

    return [test_list, cost, reliability]




def truthtable (n):
    if n < 1:
        return [[]]
    subtable = truthtable(n-1)
    return [ row + [v] for row in subtable for v in [0,1] ]


# graph example {'A': set(['C']), 'C': set(['A', 'B', 'D']), 'B': set(['C', 'E']), 'E': set(['B']), 'D': set(['C'])}

def dfs(graph, start):
    visited = set()
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)

    return visited



def isAllConnected(truth_list, input_list):
    cities_list = list()
    test_list = list(input_list)


    for edge in test_list:
        cities_list.append(edge.vertice_1)
        cities_list.append(edge.vertice_2)

    cities_list = set(cities_list)
    cities_list = list(cities_list)
    if len(cities_list) == 0:
        return False

    i = 0
    for edge in test_list:
        if truth_list[i] == 0:
            test_list.remove(edge)
        i = i+1


    if len(test_list) >= (len(cities_list)-1):
        test_graph = getGraph(test_list)
    else:
        return 0


    visited_list = dfs(test_graph,cities_list[1])

    if len(cities_list) > len(visited_list):
        return False

    return True

def getGraph(test_list):
    dict_graph = {}
    for edge in test_list:
        if edge.vertice_1 not in dict_graph:
            dict_graph[edge.vertice_1] = set(edge.vertice_2)
        else:
            dict_graph[edge.vertice_1].update(set(edge.vertice_2))
        if edge.vertice_2 not in dict_graph:
            dict_graph[edge.vertice_2] = set(edge.vertice_1)
        else:
            dict_graph[edge.vertice_2].update(set(edge.vertice_1))
    for key in dict_graph:
        dict_graph[key] = set(dict_graph[key])

    return dict_graph

def money(list):
    cost = 0
    for edge in list:
        cost = cost+edge.cost
    return cost