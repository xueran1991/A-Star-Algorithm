import math

def shortest_path(M,start,goal):
    '''
    A star algorithm
    '''
    frontier = {start}
    explored = set()
    came_from = {}
    g_score = {start:0}
    f_score = {start:distance_between(M.intersections, start, goal)}
    
    # 轮循边界上所有的节点
    while len(frontier) > 0:
        
        #获取边界中的最优节点
        optimal_node = min(f_score, key=f_score.get)
        
        if optimal_node == goal:
            return reconstruct_path(came_from, optimal_node)
        else:
            # 更新边界集、已评估集
            explored.add(optimal_node)
            frontier.remove(optimal_node)
            
            # 遍历当前最优节点的相邻节点
            for node in get_neighbors(optimal_node, M.roads):
                if node not in explored:
                    frontier.add(node)
                else:
                    continue
                
                # 这里记录首次出现的最优节点的相邻节点
                if node not in g_score:
                    g_score[node] = g_score[optimal_node] + distance_between(M.intersections, optimal_node, node)
                    f_score[node] = g_score[node] + distance_between(M.intersections, node, goal)
                    came_from[node] = optimal_node
                
                # 若当前最优节点的相邻点是出现过的，比较这个节点的g_score，如果没有这个节点首次出现时的g_score小，则此次放弃记录
                # 这样若果有多条路径到达一个节点，总会选择使总cost最小的
                tentative_g_score = g_score[optimal_node] + distance_between(M.intersections, optimal_node, node)
                if tentative_g_score >= g_score[node]:
                    continue
                
                # 更新cost
                g_score[node] = tentative_g_score
                f_score[node] = g_score[node] + distance_between(M.intersections, node, goal)
                
                # 记录父节点
                came_from[node] = optimal_node
            
            # 删除已经处理过的最优节点的cost          
            del g_score[optimal_node]   
            del f_score[optimal_node]
     
    return best_path

### 获取h_score， 即两点间的直线距离
def distance_between(nodes, node_1, node_2):
    
    
    return math.sqrt(math.pow(nodes[node_1][0]-nodes[node_2][0], 2) + math.pow(nodes[node_1][1]-nodes[node_2][1], 2))

### 获取相邻节点
def get_neighbors(node, roads):
    neighbors = []
    for i in range(len(roads)):
        if node in roads[i]:
            neighbors.append(i)
    return neighbors

### 构建路径
def reconstruct_path(came_from, current_node):
    if current_node in came_from.keys():
        path = reconstruct_path(came_from, came_from[current_node])
        return path + [current_node]
    else:
        return [current_node]