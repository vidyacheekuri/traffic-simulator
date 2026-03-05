#!/usr/bin/env python3
"""
Convert Sioux Falls to SUMO with COMPACT coordinates (scale down by 20x)
"""
import xml.etree.ElementTree as ET
import networkx as nx

print("Converting Sioux Falls to COMPACT SUMO network...")

# Read the GraphML file
G = nx.read_graphml("sioux.graphml")

print(f"Loaded network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# Create SUMO nodes XML
nodes_xml = ET.Element('nodes', {
    'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xsi:noNamespaceSchemaLocation': 'http://sumo.dlr.de/xsd/nodes_file.xsd'
})

# SCALE DOWN by 20x for better viewing!
SCALE_FACTOR = 20.0

for node_id in G.nodes():
    x = float(G.nodes[node_id]['x']) / SCALE_FACTOR
    y = float(G.nodes[node_id]['y']) / SCALE_FACTOR
    
    # Traffic light if multiple incoming edges
    incoming_edges = list(G.predecessors(node_id))
    node_type = 'traffic_light' if len(incoming_edges) > 1 else 'priority'
    
    node_elem = ET.SubElement(nodes_xml, 'node', {
        'id': node_id,
        'x': str(x),
        'y': str(y),
        'type': node_type
    })

# Write nodes file
tree = ET.ElementTree(nodes_xml)
ET.indent(tree, space="  ")
tree.write('sioux_falls.nod.xml', encoding='utf-8', xml_declaration=True)
print("✓ Created sioux_falls.nod.xml (COMPACT - 20x smaller)")

# Create SUMO edges XML (edges stay the same)
edges_xml = ET.Element('edges', {
    'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xsi:noNamespaceSchemaLocation': 'http://sumo.dlr.de/xsd/edges_file.xsd'
})

for u, v, data in G.edges(data=True):
    edge_id = f"{u}to{v}"
    
    # Use free_flow_time (in seconds) to calculate realistic length
    free_flow_time = float(data.get('free_flow_time', 10))
    speed = 13.89  # meters per second (~50 km/h)
    
    # Scale down length too for compact network
    length = (speed * free_flow_time) / 2  # Half the normal length for compact view
    
    # Ensure reasonable speed range
    speed = max(8.0, min(speed, 25.0))
    
    # Number of lanes - 2 per direction for all roads
    num_lanes = 2
    
    edge_elem = ET.SubElement(edges_xml, 'edge', {
        'id': edge_id,
        'from': u,
        'to': v,
        'numLanes': str(num_lanes),
        'speed': f"{speed:.2f}",
        'length': f"{length:.2f}"
    })

# Write edges file
tree = ET.ElementTree(edges_xml)
ET.indent(tree, space="  ")
tree.write('sioux_falls.edg.xml', encoding='utf-8', xml_declaration=True)
print("✓ Created sioux_falls.edg.xml (COMPACT)")

print("\n✓ Conversion complete! Network is now 20x more compact!")
print(f"\nOriginal coordinates: 1000-20000")
print(f"New coordinates: 50-1000 (much more viewable!)")
print("\nRun: python3 rebuild_network.py  (rebuilds with wider lanes)")
