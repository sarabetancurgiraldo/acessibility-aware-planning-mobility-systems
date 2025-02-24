# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 16:34:17 2024

@author: sarab
"""

import pickle
import copy
import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
from collections import defaultdict
import scipy.io



def coord_list(G):
    """
    Collect the coordinates of all nodes in a graph, type dict().
    Supported types: FlexibleGraph, DiGraph.
    """
    coordList = {}
    for idx in G._node.keys():
        coordList[idx] = [G._node[idx]['x'], G._node[idx]['y']]
    return coordList

def wait_switch(G, type_edge):
    G = copy.deepcopy(G)
    t_ow = [G[e1][e2]['weight'] 
            for e1, e2 in G.edges 
            if G[e1][e2]['type'] == type_edge]
    avg = sum(t_ow)/len(t_ow)
    print(type_edge, avg)

def plot_paths(G, path, pc4d_crop, type_graph, nodes, edges, od, flag_save, 
               pos_all):
    G = copy.deepcopy(G)
    
    node_o = path[0]
    node_d = path[-1]
    nodes_in_path = path
    path_draw = [(nodes_in_path[i], nodes_in_path[i+1]) 
                  for i in range(len(nodes_in_path)-1)]
    
    switching_edges = [edge for edge in edges
                       if G[edge[0]][edge[1]]['type'][0] == 's']
    
    nd_colors = [G._node[u]['color'] for u in nodes]
    edg_colors = [G[u][v]['color'] for u,v in edges]

    edg_width = [5 if edg in path_draw 
                  else 0 if edg in switching_edges 
                  else 0.1 for edg in edges]
    nd_size = [20 if node in  nodes_in_path else 0.1 for node in nodes]
    
    # pos_all = coord_list(G)
    
    fig_g, ax_g = plt.subplots(figsize=(10, 10))
    pc4d_crop.boundary.plot(ax=ax_g, linewidth=0.2, color='k')
    nx.draw_networkx(G, 
                     ax=ax_g, 
                     pos=pos_all, 
                     with_labels=False, 
                     node_size=nd_size, 
                     width=edg_width, 
                     arrows=False, 
                     nodelist=nodes, 
                     node_color=nd_colors, 
                     edgelist=edges, 
                     edge_color=edg_colors)
    nx.draw_networkx_nodes(G, 
                           ax=ax_g, 
                           pos=pos_all, 
                           nodelist=[node_o], 
                           node_shape="o", 
                           node_size=50, 
                           node_color='k')
    nx.draw_networkx_nodes(G, 
                           ax=ax_g, 
                           pos=pos_all, 
                           nodelist=[node_d], 
                           node_shape="s", 
                           node_size=50, 
                           node_color='k')
    # mode_color = [mpatches.Patch(color=color_blue, label='$\\textrm{Car}$'),
    #               mpatches.Patch(color=color_red, label='$\\textrm{Bike}$'),
    #               mpatches.Patch(color=color_green, label='$\\textrm{Waiting PT}$'),
    #               mpatches.Patch(color=color_yellow, label='$\\textrm{Walk}$'),
    #               mpatches.Patch(color=color_purple, label='$\\textrm{PT}$'),
    #               Line2D([0],[0],label='$\\textrm{Origin}$',marker="o", 
    #                      markeredgecolor='k', markersize=10, 
    #                      markerfacecolor='k', linestyle=''),
    #               Line2D([0],[0],label='$\\textrm{Destination}$',marker="s", 
    #                      markeredgecolor='k', markersize=10, 
    #                      markerfacecolor='k', linestyle='')]
    # plt.legend(handles=mode_color,fontsize=16,loc=(0.08,0.59))
    ax_g.set_axis_off()
    
        
    if flag_save:
        fp = os.path.join(os.getcwd(), f'figures_check\\od{od}_{type_graph}.jpg')
        plt.savefig(fp,
                    bbox_inches = "tight",
                    pad_inches = 0, 
                    transparent = True,
                    dpi = 100)
        plt.close()
    print('OD: ' + str(od))
    
    # fp = os.path.join(os.getcwd(), f'figures\\od{od}_{type_graph}.svg')

def save_od(od_pairs):
    fp_save = os.path.join(os.getcwd(), 'variables\\od_pairs.pkl')
    with open(fp_save, 'wb') as f:  
        pickle.dump([od_pairs], f)

def read_od():
    fp_save = os.path.join(os.getcwd(), 'variables\\od_pairs.pkl')
    with open(fp_save, 'rb') as f:  
        od_pairs = pickle.load(f)
    return od_pairs[0]

def save_paths(data):
    fp_save = os.path.join(os.getcwd(), 'variables\\od_paths.pkl')
    with open(fp_save, 'wb') as f:  
        pickle.dump([data], f)
    save_mat = os.path.join(os.getcwd(), 
                            'variables\\matlab_data_od_paths.mat')
    scipy.io.savemat(save_mat,data)





os.chdir('..')

plt.rcParams.update({"text.usetex": True,'font.size': 25})
plt.rc('axes.spines', **{'bottom':True, 'left':True, 'right':False, 'top':False})

fp_save = os.path.join(os.getcwd(), 'variables\\data_Eindhoven.pkl')
with open(fp_save, 'rb') as f:  
    [G_w, G_b, G_c, pc4d_crop, pc4d_join, pc4d_data, multiplier_low_income, 
     G_cbw, G_o, G_ocbw, pc4_info, G_pt, G_ocbwpt, G_d, G_ocbwptd, G_obwptd, 
     full_demand, data_matlab, G_pt] = pickle.load(f)
    
# predefined variables maybe worth saving if not on .txt file outside
fp_save_vars = os.path.join(os.getcwd(), 'variables\\data_Eindhoven_vars.pkl')
with open(fp_save_vars, 'rb') as f:  
    [average_speed_car, average_speed_walk, bbox, crs, default_wait_pt, 
     dict_weird_nodes, flag_bike, flag_create_pt, flag_load, flag_parking, 
     max_nodes_pc, modes, modes_percentage, motives_to_remove, parking_time, 
     share_nodes, target_nodes, total_av_trips] = pickle.load(f)


color_blue = (0, 0.4470, 0.7410)
color_red = (0.8500, 0.3250, 0.0980)
color_green = (0.4660, 0.6740, 0.1880)
color_yellow = (0.9290, 0.6940, 0.1250)
color_purple  = (0.4940, 0.1840, 0.5560)
color_light_blue = (0.3010, 0.7450, 0.9330)
color_burgundy = (0.6350, 0.0780, 0.1840)

edg_types = [G_ocbwptd[e1][e2]['type'] for e1, e2 in G_ocbwptd.edges]
# print(set(edg_types))

node_types = [G_ocbwptd._node[node]['type'] for node in G_ocbwptd._node]
# print(set(node_types))

lst = [pop for pop in pc4_info['population'].values()]

# print(sum(lst)) 
# print('Eindhoven population ~ 238326')
# print('Veldhoven population ~ 45500')
# print('Sum demand: ',sum(sum(full_demand)))
# print('Sum population * av. trips: ',sum(lst)*modes['total'])

# switching edges waiting times
wait_switch(G_ocbwptd, 's-o-w')
wait_switch(G_ocbwptd, 's-o-b')
wait_switch(G_ocbwptd, 's-b-w')
wait_switch(G_ocbwptd, 's-w-c')
wait_switch(G_ocbwptd, 's-c-w')
wait_switch(G_ocbwptd, 's-w-pt')
wait_switch(G_ocbwptd, 's-pt-w')
wait_switch(G_ocbwptd, 's-c-pt')
wait_switch(G_ocbwptd, 's-pt-c')
wait_switch(G_ocbwptd, 's-w-d')

# Check negative weights
negative_weights = [(e1, e2) 
                    for e1, e2 in G_ocbwptd.edges 
                    if G_ocbwptd[e1][e2]['weight'] < 0]

_0_weights = [(e1, e2) 
              for e1, e2 in G_ocbwptd.edges 
              if G_ocbwptd[e1][e2]['weight'] == 0]



#%%% Shortest paths

# od_pairs = read_od()

nodes = list(data_matlab['nodes'][0])
edges = [(data_matlab['edges'].loc[i,0], data_matlab['edges'].loc[i,1]) 
         for i in range(len(data_matlab['edges']))]

origin_nodes_ind = data_matlab['origin_nodes_ind']
origins = [nodes[i] for i in origin_nodes_ind]
origins_from_graph = list(G_o._node.keys())
# print([ori for ori in origins_from_graph if ori not in origins])

destination_nodes_ind = data_matlab['destination_nodes_ind']
destinations = [nodes[i] for i in destination_nodes_ind]
destinations_from_graph = list(G_d._node.keys())
# print([dest for dest in destinations_from_graph if dest not in destinations])

od_pairs = np.where(full_demand>0)
demand_o_notin_origins = [ori for ori in od_pairs[0] 
                          if ori not in origin_nodes_ind]
demand_d_notin_origins = [dest for dest in od_pairs[1] 
                          if dest not in destination_nodes_ind]

# print(demand_o_notin_origins, demand_d_notin_origins)

short_path_dict = defaultdict(list)
type_graph = ['full','no_car', 'no_bike']



G_owptd = copy.deepcopy(G_obwptd)
G_owptd.remove_nodes_from(list(G_b._node.keys()))

for od in range(len(od_pairs[0])): #range(3, len(od_pairs[0]), 100):
    for k in range(3):
        if k == 0:
            G = G_ocbwptd
        if k == 1:
            G = G_obwptd
        if k == 2:
            G = G_owptd
        origin = nodes[od_pairs[0][od]]
        destination = nodes[od_pairs[1][od]]
        path = nx.shortest_path(G, source=origin, target=destination, 
                                weight='weight')
        short_path_dict[type_graph[k]].append(path)
        path_draw = [(path[i], path[i+1]) 
                      for i in range(len(path)-1)]
        time = sum([G[u][v]['weight'] for u, v in path_draw])
    #     print('k: ' + str(k) + '. od: ' + str(od) + '. Time: ' + str(time/60))
    # print(origin, destination)
    # print('{:.4f}, {:.4f}'.format(G._node[origin]['y'], G._node[origin]['x']))
    # print('{:.4f}, {:.4f}'.format(G._node[destination]['y'], G._node[destination]['x']))
    print(od)

# print(len(od_pairs[0]))
# print(len(short_path_dict['full']))
# print(len(short_path_dict['no_car']))

mask_edges_nocar = data_matlab['mask_edges_nocar']
mask_nodes_nocar = data_matlab['mask_nodes_nocar']

edges_nocar = [edg for (edg, mask) in zip(edges, mask_edges_nocar) if mask]
nodes_nocar = [node for (node, mask) in zip(nodes, mask_nodes_nocar) if mask]



save_od(od_pairs)

data = {"od_pairs": od_pairs, 
        "paths_dict": short_path_dict}

save_paths(data)



# #%%% # Check type of edges used in path, which paths use bike and take longer than 20 mins?
# typ_nodes_paths = defaultdict(list)
# with_bike = defaultdict(list)
# times_paths = defaultdict(list)
# for k in range(2):
#     if k == 0: 
#         G = G_ocbwptd
#         edges_ = edges.copy()
#         nodes_ = nodes.copy()
#     if k == 1: 
#         G = G_obwptd
#         edges_ = edges_nocar.copy()
#         nodes_ = nodes_nocar.copy()
#     paths_list = short_path_dict[type_graph[k]]
#     for od in range(len(paths_list)):
#         nodes_in_path = paths_list[od]
#         path_draw = [(nodes_in_path[i], nodes_in_path[i+1]) 
#                       for i in range(len(nodes_in_path)-1)]
#         time = sum([G[u][v]['weight'] for u, v in path_draw])
#         typ_edges = [G[u][v]['type'] for u, v in path_draw]
#         times_paths[type_graph[k]].append(time)
#         if (('b' in typ_edges or 's-o-b' in typ_edges or 's-b-w' in typ_edges) 
#             and time > 20*60):
#             with_bike[type_graph[k]].append(od)


# # Check which paths from case1 (graph with cars) use bike by default and take 
# # more than 20 mins are also on case 2 with same characteristics
# print([od in with_bike[type_graph[1]] for od in with_bike[type_graph[0]]])


# # Find ods w/ bike > 20 mins to be checked again
# check_bike_nc = [od for od in with_bike[type_graph[1]] ]
#                   # if od not in no_prob_nc]
# check_bike_full = [od for od in with_bike[type_graph[0]] ]
#                     # if od not in no_prob_full]

# # Create new graph w/out car&bike to compare od paths w/ pt only
# G_owptd = copy.deepcopy(G_obwptd)
# G_owptd.remove_nodes_from(list(G_b._node.keys()))

# # Get shortest path for problematic ods on pt only graph
# prob_od_paths = defaultdict(list)
# prob_od_times = defaultdict(list)
# for k in range(2):
#     if k == 0: 
#         G = G_obwptd
#         edges_ = edges.copy()
#         nodes_ = nodes.copy()
#         type_g = 'no car'
#     if k == 1:
#         G = G_owptd
#         edges_ = list(G_owptd.edges)
#         nodes_ = list(G_owptd._node.keys())
#         type_g = 'no bike'
#     edges_ = list(G.edges)
#     nodes_ = list(G._node.keys())
#     pos_all = coord_list(G)
#     for od in check_bike_nc: 
#         origin = nodes[od_pairs[0][od]]
#         destination = nodes[od_pairs[1][od]]
#         path = nx.shortest_path(G, source=origin, target=destination, 
#                                 weight='weight')
#         plot_paths(G, path, pc4d_crop, type_g, nodes_, edges_, od, 
#                     True, pos_all)
#         prob_od_paths[type_g].append(path)
#         path_draw = [(path[i], path[i+1]) 
#                       for i in range(len(path)-1)]
#         time = sum([G[u][v]['weight'] for u, v in path_draw])
#         prob_od_times[type_g].append(time)


# # Compare times of bike & pt
# compare_t_ptb = []
# for ind, od in enumerate(check_bike_nc):
#     t_bike = prob_od_times['no car'][ind]/60
#     t_pt = prob_od_times['no bike'][ind]/60
#     comp_t_bpt = t_bike > t_pt
#     print("od: {}, b: {:.2f}, pt: {:.2f}. {}".format(od, 
#                                                      round(t_bike, 2), 
#                                                      round(t_pt, 2),
#                                                      comp_t_bpt))
#     compare_t_ptb.append(comp_t_bpt)

# od_pt_faster = [check_bike_nc[ind] 
#                 for ind, value in enumerate(compare_t_ptb) 
#                 if value]



# # fp_save_checks = os.path.join(os.getcwd(), 'variables\\check_vars.pkl')
# # with open(fp_save_checks, 'wb') as f:  
# #     pickle.dump([od_pt_faster, G_owptd, od_pairs], f)


# for od in [72, 147, 258, 393, 482, 539, 641, 770, 941, 1014, 1260]:
#     for k in range(2):
#         if k == 0:
#             G = G_obwptd
#         if k == 1:
#             G = G_owptd
#         origin = nodes[od_pairs[0][od]]
#         destination = nodes[od_pairs[1][od]]
#         path = nx.shortest_path(G, source=origin, target=destination, 
#                                 weight='weight')
#         path_draw = [(path[i], path[i+1]) 
#                       for i in range(len(path)-1)]
#         time = sum([G[u][v]['weight'] for u, v in path_draw])/60
#         print(time)
#         print(k, od)
#     print(G._node[origin])
#     print(G._node[destination])

# #%%%

# # # Maybe get positions from matlab data and pass to fn
# for k in range(2):
#     if k == 0: 
#         G = G_ocbwptd
#         edges_ = edges.copy()
#         nodes_ = nodes.copy()
#     if k == 1: 
#         G = G_obwptd
#         edges_ = edges_nocar.copy()
#         nodes_ = nodes_nocar.copy()
#     paths_list = short_path_dict[type_graph[k]]
#     for od in range(len(paths_list)): #range(0, len(paths_list), 100):
#         path = paths_list[od]
#         plot_paths(G, path, pc4d_crop, type_graph[k], nodes_, edges_, od)











#%% Test for cost model on car layer?

# # g1_cost0_c_edg = []
# # g1_cost0_c_nd = []
# # for edg in G1_edges:
# #     if G1[edg[0]][edg[1]]['cost'] == 0  and G1[edg[0]][edg[1]]['type'] == 'c':
# #         g1_cost0_c_edg.append(edg)
# #         g1_cost0_c_nd.extend(edg)

# # nodes_g1 = [k for k, v in G1._node.items() if v['type'] == 'c']

# # nd_colors_g1 = [G1._node[u]['color'] for u in nodes_g1]

# # edges_g1 = [(u, v) for u, v in list(G1.edges()) if G1[u][v]['type'] == 'c' ]

# # edg_colors_g1 = [G1[u][v]['color'] for u,v in edges_g1]

# # edg_width_g1 = [2 if edg in g1_cost0_c_edg else 0.1 for edg in edges_g1]

# # nd_size_g1 = [2 if node in  g1_cost0_c_nd else 0.1 for node in nodes_g1]







