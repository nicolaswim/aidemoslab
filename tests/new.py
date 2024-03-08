import plotly.graph_objects as go

fig = go.Figure(data=go.Heatmap(
    z=[[1, 20, 30], 
       [20, 1, 60], 
       [30, 60, 1]],
    colorbar=dict(
        title='n value',  # Setting the label/title of the colorbar
        # You can specify other colorbar properties here
    )
))

fig.show()
