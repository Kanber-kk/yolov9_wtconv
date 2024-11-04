from graphviz import Digraph

# Create a directed graph
dot = Digraph(comment='EMSFE Module Flowchart')

dot.attr(rankdir='LR')

# Input node
dot.node('Input', 'Input: (batch_size, in_channels, H, W)')

# Branch nodes
dot.node('Center', 'Center Branch\n3x3 Conv')
dot.node('Left', 'Left Branch\n3x1 + 1x3 + 3x1 + 1x3 + 1x1 Conv\nDilation=5')
dot.node('Right', 'Right Branch\n5x1 + 1x5 + 5x1 + 1x5 + 1x1 Conv\nDilation=7')
dot.node('One', 'One Branch\n1x1 Conv')

# Connections from input to each branch
dot.edge('Input', 'Center')
dot.edge('Input', 'Left')
dot.edge('Input', 'Right')
dot.edge('Input', 'One')

# Merge branches
dot.node('Concat', 'Concatenate\n(dim=1)')
dot.edge('Center', 'Concat')
dot.edge('Left', 'Concat')
dot.edge('Right', 'Concat')
dot.edge('One', 'Concat')

# Coordinate Attention node
dot.node('CoordAtt', 'Coordinate Attention')
dot.edge('Concat', 'CoordAtt')

# Channel reduction node
dot.node('ChannelReduction', '1x1 Conv\nChannel Reduction')
dot.edge('CoordAtt', 'ChannelReduction')

# Residual connection and output
dot.node('Residual', 'Residual Connection\n(Input + Output)')
dot.edge('Input', 'Residual', style='dashed')
dot.edge('ChannelReduction', 'Residual')

dot.node('Output', 'Output: (batch_size, out_channels, H, W)')
dot.edge('Residual', 'Output')

# Render the graph
dot.render('emsfe_flowchart', format='png', view=True)

# Displaying the flowchart
print(dot.source)
