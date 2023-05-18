import streamlit as st
from streamlit import session_state as ss

import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go

def area_plot(df, col_x, col_y, title, hover_text):
    fig = go.Figure()
    fig.add_trace(
                go.Scatter(
                        x=df[col_x],
                        y=df[col_y],
                        text=hover_text,
                        fill='tonexty',                                
                        )
                )
    fig.update_traces(hovertemplate=None)
    fig.update_layout(title=title, hovermode="x unified")
    return fig

