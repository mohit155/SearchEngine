import plotly.plotly as py
import plotly.graph_objs as go


def plot_graph(eigen_values, pages):
    plot_x = []
    for val in range(pages):
        plot_x.append(val)
    plot_y = eigen_values

    # Create a trace
    trace = go.Scatter(
        x=plot_x,
        y=plot_y
    )
    plot_data = [trace]

    py.plot(plot_data, filename='EigenValues-vs-Documents')
