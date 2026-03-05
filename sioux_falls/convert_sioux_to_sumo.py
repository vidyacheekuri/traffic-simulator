#!/usr/bin/env python3
"""
Convert Sioux Falls network (sioux.graphml) to SUMO format
"""
import xml.etree.ElementTree as ET
import networkx as nx

print("Converting Sioux Falls network to SUMO...")

# Read the GraphML file
G = nx.read_graphml("sioux.graphml")

print(f"Loaded network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# Create SUMO nodes XML
nodes_xml = ET.Element('nodes', {
    'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xsi:noNamespaceSchemaLocation': 'http://sumo.dlr.de/xsd/nodes_file.xsd'
})

for node_id in G.nodes():
    x = float(G.nodes[node_id]['x'])
    y = float(G.nodes[node_id]['y'])
    
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
print("✓ Created sioux_falls.nod.xml")

# Create SUMO edges XML
edges_xml = ET.Element('edges', {
    'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xsi:noNamespaceSchemaLocation': 'http://sumo.dlr.de/xsd/edges_file.xsd'
})

for u, v, data in G.edges(data=True):
    edge_id = f"{u}to{v}"
    
    # Use free_flow_time (in seconds) to calculate realistic length
    # Assume typical urban speed of 13.89 m/s (~50 km/h)
    free_flow_time = float(data.get('free_flow_time', 10))
    speed = 13.89  # meters per second (~50 km/h)
    length = speed * free_flow_time  # Calculate length from travel time
    
    # Ensure reasonable speed range (between 8-25 m/s = 30-90 km/h)
    speed = max(8.0, min(speed, 25.0))
    
    # Number of lanes (based on capacity - rough estimate)
    capacity = float(data.get('capacity', 1000))
    num_lanes = max(1, min(3, int(capacity / 10000)))  # 1-3 lanes
    
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
print("✓ Created sioux_falls.edg.xml")

print("\n✓ Conversion complete!")
print("\nNext step: Run netconvert to create the network:")
print("  netconvert --node-files=sioux_falls.nod.xml --edge-files=sioux_falls.edg.xml --output-file=sioux_falls.net.xml --tls.guess")
