# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 13:11:00 2023

@author: KristenMcCaffrey
"""

"""
Testing app with pages structure
"""

import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('This is our Home page'),
    html.Div('This is our Home page content.'),
])