# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 13:07:47 2023

@author: KristenMcCaffrey
"""

"""
Testing app with pages structure
"""
#%% Contents
# -----------------------------------------------------------------------------------------------
# ### Framework
# 1. Startup & Imports
# 2. Initialize App (i.e., the web app)
# 3. Global Program Elements (e.g. read in data and prep it)
# 4. Layout (i.e, the UI layout)
# 5. Callbacks (functions that respond to UI)
# 6. Run App
# -----------------------------------------------------------------------------------------------

#%% 1. STARTUP & IMPORTS

# standard library packages (included with python and always available)
import os, sys, datetime as dt
from pathlib import Path
import inspect
import requests
import io

print(f"[{dt.datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:19]}] Starting {__name__}")
print(f"[{dt.datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:19]}] cwd = {os.getcwd()}")
print(f"[{dt.datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:19]}] {sys.path[:2] = }")
print(f"[{dt.datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:19]}] {sys.version = }")

# Third party packages (ie, those installed with pip )
import dash
from dash import html, dcc, Input, Output, State, dash_table, ctx, Dash
import dash_bootstrap_components as dbc  # Allows easy access to all bootstrap themes
import dash_daq as daq
import dash_auth
import numpy as np
import scipy as sp
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import geopandas as gpd
from flask import Flask, redirect
# private (fa) libraries
import lib.fa_dash_utils as fa

#### PARAMETERS
prod                         = False   # Use when testing/dev mode to remove auth

#%% 2. INITIALIZE APP
###############################################################################################
# - App named here... if name is changed here, must also be changed elsewhere below
# - Either JupyterDash or just Dash for traditional .py program in Spyder. (Latter requires: 'from dash import Dash' above)
# - There are other dbc.themes (e.g. "SANDSTONE") and other options besides dash_bootstrap_components
###############################################################################################
app_title = 'AHLE Case Study Dash UI'
external_stylesheets=[dbc.themes.BOOTSTRAP]
flask_server, app = fa.instantiate_app(app_title, external_stylesheets) # dont change name "flask_server".  Gunicorn expects to find it
gbadsDash = app  # an alias for app; the app name used within this program

if prod:
    ## USERNAMES AND PASSWORDS
    # Keep this out of source code repository - save in a file or a database
    VALID_USERNAME_PASSWORD_PAIRS = {
        'gbads': 'welcometogbads',
        'GBADS': "welcometogbads",
        'GBADs': "welcometogbads"
    }

    # BASIC AUTHORIZATION:  USERNAME:PASSWORD
    auth = dash_auth.BasicAuth(
        gbadsDash,
        VALID_USERNAME_PASSWORD_PAIRS
        )


app.config.suppress_callback_exceptions = True    # Use to remove warnings when assigning callbacks to components that are generated by other callbacks (and therefore not in the initial layout)

#%% 3. GLOBAL PROGRAM ELEMENTS
###############################################################################################
# - Global variables and functions that aren't directly involved in the UI interactivity (Callbacks)
# - Typical example would be functions that read, store, and prep data to be used in the app
###############################################################################################
# Define tab styles

# Tab colors based on grouping
ecs_tab_style = {
    'backgroundColor': '#d7bce1',
    'border-color': 'grey',
    'fontWeight': 'bold'
}
ecs_tab_selected_style = {
    'backgroundColor': '#d7bce1',
    'border-color': 'grey',
    'fontWeight': 'bold'
}

user_guide_tab_style ={
    'border-color': 'grey',
    'fontWeight': 'bold'
}

user_guide_tab_selected_style ={
    'border-color': 'grey',
    'fontWeight': 'bold'
}


# =============================================================================
# # For reference, the first version of the plots was based on Excel files
#
# # Data for the waterfall chart
# waterfall_df = pd.read_excel("data/chickens_bod_plotdata.xls", header=0,sheet_name="Waterfall")
#
# # Data for the sankey diagram
# sankey_df = pd.read_excel("data/chickens_bod_plotdata.xls", header=0,sheet_name="Sankey")
#
# # Data for the data table
# background_df = pd.read_excel('data/chickens_bod_backgrounddata.xls')
#
# =============================================================================

# =============================================================================
#### Read data
# =============================================================================
# Define folder location
CWD = os.getcwd()
DASH_DATA_FOLDER = os.path.join(CWD ,'data')

# Folder location for ethiopia case study
GBADsLiverpool=Path(os.getcwd()).parent.parent
Data_and_Processing_Code = "Data and Processing Code"

# Folder location for global aggregate
if prod:
    # Output folders:
    ECS_PROGRAM_OUTPUT_FOLDER = os.path.join(CWD, Data_and_Processing_Code, "Program outputs")
else:
    # Output folders:
    ECS_PROGRAM_OUTPUT_FOLDER = os.path.join(GBADsLiverpool, Data_and_Processing_Code, "Program outputs")

# -----------------------------------------------------------------------------
# Ethiopia Case Study
# -----------------------------------------------------------------------------
# Compartmental model results summary
ecs_ahle_summary = pd.read_csv(os.path.join(DASH_DATA_FOLDER ,'ahle_all_summary.csv'))
## Using alternative data which summarizes results from age/sex specific scenarios
ahle_all_scensmry = pd.read_csv(os.path.join(DASH_DATA_FOLDER ,'ahle_all_scensmry.csv'))

# Compartmental model results summary with AHLE calculated
# for stacked bar
ecs_ahle_summary2 = pd.read_csv(os.path.join(DASH_DATA_FOLDER ,'ahle_all_summary2.csv'))

# Attribution Summary
# ecs_ahle_all_withattr = pd.read_csv(os.path.join(DASH_DATA_FOLDER ,'ahle_all_withattr.csv'))
## Using data with disease-specific attribution
ecs_ahle_all_withattr = pd.read_csv(os.path.join(DASH_DATA_FOLDER ,'ahle_all_withattr_disease.csv'))

# JR 2023-4-19: added regional results. Testing with Nationl level (should be same as before).
# ahle_all_scensmry = ahle_all_scensmry.query("region == 'National'").copy()
ecs_ahle_summary2 = ecs_ahle_summary2.query("region == 'National'")
# ecs_ahle_all_withattr = ecs_ahle_all_withattr.query("region == 'National'")

# Ethiopia geojson files from S3
# Regional level
url = 'https://gbads-data-repo.s3.ca-central-1.amazonaws.com/shape-files/eth_admbnda_adm1_csa_bofedb_2021.geojson'
r = requests.get(url, allow_redirects=True)
geojson_ecs = r.json()

# Alternative: read from local copy
# geojson_ecs = gpd.read_file(os.path.join(DASH_DATA_FOLDER ,'eth_admbnda_adm1_csa_bofedb_2021.geojson'))

# Expert opinion files
ecs_expertattr_smallrum = pd.read_csv(os.path.join(DASH_DATA_FOLDER ,'attribution_experts_smallruminants.csv'))
ecs_expertattr_cattle = pd.read_csv(os.path.join(DASH_DATA_FOLDER ,'attribution_experts_cattle.csv'))
ecs_expertattr_poultry = pd.read_csv(os.path.join(DASH_DATA_FOLDER ,'attribution_experts_chickens.csv'))

# Economic data is very simple. From Dashboard WEI 08082023.xlsx shared by Tom Marsh
wei_ethiopia_raw = pd.DataFrame({
    'species':'Cattle and Small Ruminants'
    ,'scenario':['Current' ,'Zero Mortality' ,'Ideal']
    ,'scenario_numeric':[0 ,0.5 ,1]
    ,'production_change_pct':[0 ,.402 ,1.8048]
    ,'gdp_change_pct':[0 ,.0251 ,.0357]
    ,'economic_surplus_mlnusd':[0 ,1760.050 ,2452.180]
})

# =============================================================================
#### User options and defaults
# =============================================================================
# -----------------------------------------------------------------------------
# All species
# -----------------------------------------------------------------------------
# Region options
region_structure_options = [{'label': i, 'value': i, 'disabled': False} for i in ["WOAH",
                                                                       "FAO",
                                                                       "World Bank",]]

# WOAH regions
WOAH_region_options = [{'label': i, 'value': i, 'disabled': False} for i in ["All",
                                                                        "Africa",
                                                                       "Americas",
                                                                       "Asia, Far East and Oceania",
                                                                       "Europe"
                                                                       ]]
WOAH_region_options += [{'label': "Middle East", 'value': "Middle East", 'disabled': True}]  # Include, but disable, Middle East

# WOAH region-country mapping
WOAH_africa_options = [{'label': i, 'value': i, 'disabled': True} for i in ["Ethiopia"]]

WOAH_americas_options = [{'label': i, 'value': i, 'disabled': False} for i in ["Brazil",
                                                                          "United States of America"]]

WOAH_asia_options = [{'label': i, 'value': i, 'disabled': False} for i in ["India",
                                                                          "United States of America"]]

WOAH_europe_options = [{'label': i, 'value': i, 'disabled': False} for i in ["France",
                                                                        "Germany",
                                                                       "Italy",
                                                                       "Netherlands",
                                                                       "Poland",
                                                                       "United Kingdom"]]

# FAO regions
fao_region_options = [{'label': i, 'value': i, 'disabled': False} for i in ["All",
                                                                        "Africa",
                                                                       "Asia",
                                                                       "Europe and Central Asia",
                                                                       "Latin America and the Caribbean",
                                                                       "South West Pacific"
                                                                       ]]

fao_region_options += [{'label': "Near East and North Africa", 'value': "Near East and North Africa", 'disabled': True}]  # Include, but disable, Middle East

# FAO region-country mapping
fao_africa_options = [{'label': i, 'value': i, 'disabled': True} for i in ["Ethiopia"]]

fao_asia_options = [{'label': i, 'value': i, 'disabled': False} for i in ["India"]]

fao_eca_options = [{'label': i, 'value': i, 'disabled': False} for i in ["France",
                                                                        "Germany",
                                                                       "Italy",
                                                                       "Netherlands",
                                                                       "Poland",
                                                                       "United Kingdom"]]

fao_lac_options = [{'label': i, 'value': i, 'disabled': False} for i in ["Brazil"]]

fao_swp_options = [{'label': i, 'value': i, 'disabled': False} for i in ["France",
                                                                          "United States of America"]]

# World Bank regions
wb_region_options = [{'label': i, 'value': i, 'disabled': False} for i in ["All",
                                                                        "Sub-Saharan Africa",
                                                                       "Europe & Central Asia",
                                                                       "Latin America & the Caribbean",
                                                                       "North America",
                                                                       "South Asia"
                                                                       ]]

wb_region_options += [{'label': i, 'value': i, 'disabled': True} for i in ["East Asia & Pacific",
                                                                       "Middle East & North Africa"
                                                                       ]]

# World Bank region-country mapping

wb_africa_options = [{'label': i, 'value': i, 'disabled': True} for i in ["Ethiopia"]]

wb_eca_options = [{'label': i, 'value': i, 'disabled': False} for i in ["France",
                                                                        "Germany",
                                                                       "Italy",
                                                                       "Netherlands",
                                                                       "Poland",
                                                                       "United Kingdom"]]

wb_lac_options = [{'label': i, 'value': i, 'disabled': False} for i in ["Brazil"]]

wb_na_options = [{'label': i, 'value': i, 'disabled': False} for i in ["United States of America"]]

wb_southasia_options = [{'label': i, 'value': i, 'disabled': False} for i in ["India"]]


# Define country shortnames
# These taken from https://en.wikipedia.org/wiki/List_of_alternative_country_names
# Keys in this dictionary must match country names in data
# Should include superset of countries from all species
country_shortnames = {
   'Brazil':'BRA'
   ,'China':'CHN'
   ,'Denmark':'DNK'
   ,'France':'FRA'
   ,'Germany':'DEU'
   ,'India':'IND'
   ,'Italy':'ITA'
   ,'Netherlands':'NLD'
   ,'Poland':'POL'
   ,'Russia':'RUS'
   ,'Spain':'ESP'
   ,'United Kingdom':'GBR'
   ,'United States of America':'USA'
}

# Metrics
# Labels are shown in dropdown, Values are shown in plot titles
# Values must match column names created in prep_bod_forwaterfall()
metric_options = [
   {'label':"Tonnes", 'value':"tonnes", 'disabled':False}
   ,{'label':"US Dollars", 'value':"US dollars", 'disabled':False}
   ,{'label':"Percent of GDP", 'value':"percent of GDP", 'disabled':False}
   ,{'label':"Percent of Breed Standard", 'value':"percent of breed standard", 'disabled':False}
   ,{'label':"Percent of Realised Production", 'value':"percent of realised production", 'disabled':False}
]

# =============================================================================
#### Ethiopia case study options
# =============================================================================
# Species
# ecs_species_options = []
# for i in np.sort(ecs_ahle_summary['species'].unique()):
#     str(ecs_species_options.append({'label':i,'value':(i)}))
# Specify the order of the species
ecs_species_options = [{'label': i, 'value': i, 'disabled': False} for i in ["Cattle",
                                                                             "All Small Ruminants",
                                                                             "Goat",
                                                                             "Sheep",
                                                                             "All Poultry",
                                                                             "Poultry hybrid",
                                                                             "Poultry indigenous",
                                                                             ]]

# Production system
# Rename Overall to more descriptive
ecs_ahle_summary['production_system'] = ecs_ahle_summary['production_system'].replace({'Overall': 'All Production Systems'})

# ecs_prodsys_options are now defined dynamically in a callback based on selected species
# ecs_prodsys_options = []
# for i in np.sort(ecs_ahle_summary['production_system'].unique()):
#    str(ecs_prodsys_options.append({'label':i,'value':(i)}))

# Year
# Year options are now set in a callback
# ecs_year_options=[]
# for i in np.sort(ecs_ahle_summary['year'].unique()):
#     str(ecs_year_options.append({'label':i,'value':(i)}))

# Sex
ecs_agesex_options=[]
for i in np.sort(ecs_ahle_summary['group'].unique()):
   str(ecs_agesex_options.append({'label':i,'value':(i)}))

# Currency
ecs_currency_options = [{'label': "Birr", 'value': "Birr", 'disabled': False},
                        {'label': "USD", 'value': "USD", 'disabled': False}]

# Attribution hierarchy
ecs_hierarchy_attr_options = [{'label': "Cause", 'value': "cause", 'disabled': False},
                              {'label': "Production System", 'value': "production_system", 'disabled': False},
                              {'label': "Age Group", 'value': "age_group", 'disabled': False},
                              {'label': "Sex", 'value': "sex", 'disabled': False},
                              {'label': "AHLE Component", 'value': "ahle_component", 'disabled': False},
                              {'label': "Disease", 'value': "disease", 'disabled': False}
                              ]

# Drill down options for hierarchy
ecs_hierarchy_dd_attr_options = [{'label': i, 'value': i, 'disabled': False} for i in ["None"]]
ecs_hierarchy_dd_attr_options += ecs_hierarchy_attr_options

# Region - removing 'National' from the options
ecs_region_options = []
for i in ecs_ahle_summary.query("region != 'National'").region.unique():
    str(ecs_region_options.append({'label':i,'value':(i)}))

# Display
ecs_display_options = [{'label': i, 'value': i, 'disabled': False} for i in ["Difference",
                                                                             "Side by Side",
                                                                            ]]
# Item

# Compare
ecs_compare_options = [{'label': i, 'value': i, 'disabled': False} for i in ["Ideal",
                                                                             "Zero Mortality",
                                                                             "Improvement"
                                                                             ]]
# August 2023: updated scenarios do not include zero mortality or improvement
ecs_compare_options_limited = [
    {'label': "Ideal", 'value': "Ideal", 'disabled': False}
    ,{'label': "Zero Mortality", 'value': "Zero Mortality", 'disabled': True}
    ,{'label': "Improvement", 'value': "Improvement", 'disabled': True}
    ]

# Factor
ecs_factor_options = [{'label': i, 'value': i, 'disabled': True} for i in ["Mortality",
                                                                           "Live Weight",
                                                                           "Parturition Rate",
                                                                           "Lactation"
                                                                           ]]

# Reduction
ecs_improve_options = [{'label': i, 'value': i, 'disabled': True} for i in ['25%',
                                                                            '50%',
                                                                            '75%',
                                                                            '100%',
                                                                            ]]
# Map Denominator
ecs_map_denominator_options = [{'label': i, 'value': i, 'disabled': False} for i in ['Per kg biomass',
                                                                                     'Total',
                                                                                     ]]

# =============================================================================
#### Prep data for plots
# =============================================================================
def prep_ahle_fortreemap_ecs(INPUT_DF):
   ecs_ahle_attr_treemap = INPUT_DF.copy()

   # # Trim the data to keep things needed for the treemap
   # ecs_ahle_attr_treemap = working_df[[
   #     'species',
   #     'production_system',
   #     'age_group',
   #     'sex',
   #     'year',
   #     'ahle_component',
   #     'cause',
   #     'disease',
   #     'mean',
   #     # 'pct_of_total'
   #     ]]

   # Can only have positive values
   ecs_ahle_attr_treemap['mean'] = abs(ecs_ahle_attr_treemap['mean'])

   # Replace 'overall' values with more descriptive values
   # ecs_ahle_summary_tree_pivot['age_group'] = ecs_ahle_summary_tree_pivot['age_group'].replace({'Overall': 'Overall Age'})
   ecs_ahle_attr_treemap['sex'] = ecs_ahle_attr_treemap['sex'].replace({'Overall': 'Overall Sex'})

   # Replace mortality with mortality loss
   ecs_ahle_attr_treemap['ahle_component'] = ecs_ahle_attr_treemap['ahle_component'].replace({'Mortality': 'Mortality Loss'})

   # Fill in missing values with 0
   ecs_ahle_attr_treemap = ecs_ahle_attr_treemap.fillna(0)

   OUTPUT_DF = ecs_ahle_attr_treemap

   return OUTPUT_DF


def prep_ahle_forwaterfall_ecs(INPUT_DF):
   ecs_ahle_waterfall = INPUT_DF.copy()

   # Fill missing values with 0
   ecs_ahle_waterfall.fillna(0)

   # Keep only items for the waterfall
   # This also specifies the ordering of the bars
   waterfall_plot_items = ('Value of Offtake',
                            'Value of Eggs consumed',
                            'Value of Eggs sold',
                            'Value of Herd Increase',
                            'Value of draught',
                            'Value of Milk',
                            'Value of Manure',
                            'Value of Hides',
                            'Feed Cost',
                            'Labour Cost',
                            'Health Cost',
                            'Infrastructure Cost',
                            'Capital Cost',
                            'Gross Margin')
   waterfall_plot_items_upper = [i.upper() for i in waterfall_plot_items]
   ecs_ahle_waterfall = ecs_ahle_waterfall.loc[ecs_ahle_waterfall['item'].str.upper().isin(waterfall_plot_items_upper)]

   # Sort Item column to keep values and costs together
   ecs_ahle_waterfall['item'] = ecs_ahle_waterfall['item'].astype('category')
   ecs_ahle_waterfall.item.cat.set_categories(waterfall_plot_items, inplace=True)
   ecs_ahle_waterfall = ecs_ahle_waterfall.sort_values(["item"])

   # Rename costs values to be more descriptive
   ecs_ahle_waterfall['item'] = ecs_ahle_waterfall['item'].replace({'Feed Cost': 'Expenditure on Feed',
                                                                    'Labour Cost': 'Expenditure on Labour',
                                                                    'Health Cost': 'Expenditure on Health',
                                                                    'Infrastructure Cost': 'Expenditure on Housing',
                                                                    'Capital Cost': 'Expenditure on Capital',
                                                                    'Value of draught': 'Value of Draught'})

   OUTPUT_DF = ecs_ahle_waterfall

   return OUTPUT_DF

def prep_ahle_forstackedbar_ecs(INPUT_DF, cols_birr_costs, cols_usd_costs, pretty_ahle_cost_names):
   working_df = INPUT_DF.copy()

   # Birr costs
   # Ordering here determines order in plot
   cols_birr_costs = cols_birr_costs

   # USD costs
   cols_usd_costs = cols_usd_costs

   # If any costs are missing, fill in zero
   for COL in cols_birr_costs + cols_usd_costs:
      working_df[COL] = working_df[COL].replace(np.nan ,0)

   # Melt birr costs into rows
   output_birr = working_df.melt(
      id_vars=['species' ,'production_system']
      ,value_vars=cols_birr_costs
      ,var_name='ahle_due_to'
      ,value_name='cost_birr'
   )
   # output_actual['opt_or_act'] = 'Actual'  # Value here determines bar label in plot

   # Melt usd costs into rows
   output_usd = working_df.melt(
      id_vars=['species' ,'production_system']
      ,value_vars=cols_usd_costs
      ,var_name='ahle_due_to'
      ,value_name='cost_usd'
   )
   # output_ideal['opt_or_act'] = 'Ideal + Burden of disease'  # Value here determines bar label in plot

   # Stack
   OUTPUT_DF = pd.concat(
      [output_birr ,output_usd]
      ,axis=0
      ,join='outer'
      ,ignore_index=True
   )

   # Recode cost item names
   pretty_ahle_cost_names = pretty_ahle_cost_names
   OUTPUT_DF['AHLE Due To'] = OUTPUT_DF['ahle_due_to'].replace(pretty_ahle_cost_names)

   # Create new string column for label
   OUTPUT_DF['Age_group_string'] = OUTPUT_DF['ahle_due_to'].str.slice(10,12)
   OUTPUT_DF['Age_group_string'] = OUTPUT_DF['Age_group_string'].str.upper()

   # Add column with labels for each segment
   OUTPUT_DF['label_birr'] = OUTPUT_DF['Age_group_string'] + ' - ' + OUTPUT_DF['cost_birr'].map('{:,.0f}'.format).astype(str) + ' Birr'
   OUTPUT_DF['label_usd'] = OUTPUT_DF['Age_group_string'] + ' - ' + OUTPUT_DF['cost_usd'].map('{:,.0f}'.format).astype(str) + ' USD'

   return OUTPUT_DF

# =============================================================================
#### Define the figures
# =============================================================================
# Define the Waterfall
def create_waterfall(x, y, text):
     waterfall_fig = go.Figure(go.Waterfall(
        name = "20",
        orientation = "v",

        measure = ["relative", "relative", "relative", "relative", "total"],  # This needs to change with number of columns in waterfalll
        x=x,
        y=y,
        hoverinfo = 'none',  # Disable the hover over tooltip
        text=text,
        textposition = ["outside","outside","auto","auto","outside"],
        decreasing = {'marker':{"color":'#F7931D'}},
        increasing = {'marker':{"color":'#3598DB'}},
        totals = {'marker':{"color":'#5BC0DE'}},
        connector = {"line":{"color":"darkgrey"}}#"rgb(63, 63, 63)"}},
        ))

     waterfall_fig.update_layout(clickmode='event+select', ### EVENT SELECT ??????
                                 plot_bgcolor="#ededed")
     waterfall_fig.update_xaxes(
         fixedrange=True
         )
     waterfall_fig.update_yaxes(
         fixedrange=True
         )

     return waterfall_fig

# Define the Sankey
def create_sankey(label_list, color, x, y, source, target, values, n):
    sankey_fig = go.Figure(data=go.Sankey(
        textfont = dict(size=15),
        arrangement = 'fixed',
        hoverinfo = 'none',  # Disable the hover over tooltip
        valueformat = ",.0f",
        node = dict(
            pad = 25,
            thickness = 15,
            line = dict(color = "black", width = 0.5),
            label = label_list,
            x = x,
            y = y,
            color = color
            ),
        link = dict(
            source = source,
            target = target,
            value = values,
            color = ['#ededed']*n),
        ))
    return sankey_fig

# Define the attribution treemap
def create_attr_treemap_ecs(input_df, path):
    treemap_fig = px.treemap(
        input_df,
        # path=[
        #    'cause',
        #    'production_system',
        #    'age_group',
        #    'sex',
        #    'ahle_component',
        #    ],
        path = path,
        values='mean',
        # hover_data=['pct_of_total'],
        # custom_data=['pct_of_total'],
        color='cause',            # cause only applys to the cause level
        color_discrete_map={      # Cause colors match the Human health dashboard
            '(?)':'lightgrey',
            'Infectious':'#68000D',
            'Non-infectious':'#08316C',
            'External':'#00441B'
            }
        )

    return treemap_fig

# Define the AHLE waterfall
def create_ahle_waterfall_ecs(input_df, name, measure, x, y):
    waterfall_fig = go.Figure(go.Waterfall(
        name = name,
        orientation = "v",
        measure = measure,  # This needs to change with number of columns in waterfalll
        x=x,
        y=y,
        decreasing = {'marker':{"color":'#E84C3D'}},
        increasing = {'marker':{"color":'#3598DB'}},
        totals = {'marker':{"color":'#F7931D'}},
        connector = {"line":{"color":"darkgrey"}},
        customdata=np.stack((y, input_df['item']), axis=-1),
        ))

    waterfall_fig.update_layout(clickmode='event+select', ### EVENT SELECT ??????
                                plot_bgcolor="#ededed",)

    waterfall_fig.add_annotation(x=4, xref='x',         # x position is absolute on axis
                                 y=0, yref='paper',     # y position is relative [0,1] to work regardless of scale
                                 text="Source: GBADs",
                                 showarrow=False,
                                 yshift=10,
                                 font=dict(
                                     family="Helvetica",
                                     size=18,
                                     color="black"
                                     )
                                 )
    waterfall_fig.update_xaxes(
        fixedrange=True
        )
    waterfall_fig.update_yaxes(
        fixedrange=True
        )

    return waterfall_fig

# Define the stacked bar
def create_stacked_bar_ecs(input_df, x, y, text, color, yaxis_title):
    bar_fig = px.bar(
        input_df,
        x=x,
        y=y,
        text = text,
        color=color,
        color_discrete_map={
          "Neonatal male":"#2A80B9",
          "Neonatal":"#2A80B9",
          "Neonatal female":"#6eb1de",
          "Juvenile male":"#9B58B5",
          "Juvenile":"#9B58B5",
          "Juvenile female":"#caa6d8",
          "Adult male":"#2DCC70",
          "Adult female":"#82e3aa",
          })
    bar_fig.update_layout(
        plot_bgcolor="#ededed",
        hovermode=False,
        showlegend=True,
        xaxis_title=None,
        yaxis_title=yaxis_title,
        )
    bar_fig.update_xaxes(
        fixedrange=True
        )
    bar_fig.update_yaxes(
        fixedrange=True
        )
    return bar_fig

# Define Ethiopia subnation level map
def create_map_display_ecs(input_df, geojson, location, featurekey, color_by, color_scale):
    ecs_map_fig = px.choropleth_mapbox(input_df,
                                       geojson=geojson,
                                       locations=location,
                                       featureidkey=featurekey,
                                       color=color_by,
                                       color_continuous_scale=color_scale,
                                       opacity=0.7,
                                       mapbox_style="carto-positron",
                                       zoom=5,
                                       center = {"lat": 9.1450, "lon": 40.4897},
                                       labels={'region': 'State',
                                               'mean_current': 'Current',
                                               'mean_ideal': 'Ideal',
                                               'mean_diff_ideal': 'AHLE'}
                                       )

    return ecs_map_fig

# Wider Economic Impact charts for Ethiopia
def create_wei_chart(
        input_df                # Dataframe
        ,plot_xvar              # String: variable to use for x axis
        ,plot_yvar              # String: variable to use for y axis. Will be interpolated over range min(X), max(X).
        ,plot_color
        ,interpolation_kind     # 'linear', 'quadratic', or 'cubic'. Integer n: spline of order n.
        ,yvar_divisor=None      # Divide y values by this number before interpolation and plotting
    ):
    # Generate range of x-axis values
    gen_end = input_df[plot_xvar].max()
    step_size = 0.01
    gen_num = int(input_df[plot_xvar].max() / step_size)
    gen_x = np.linspace(
    	start=0 				# Start value. Can be integer or float.
    	,stop=gen_end 				# Stop value. Can be integer or float.
    	,num=gen_num 				# Number of elements to generate. Will be evenly spaced from START to STOP.
        )
    # Create dataframe and name generated data for predictor variable
    gen_x_df = pd.DataFrame({
        plot_xvar:gen_x
    })

    # Adjust scale
    if yvar_divisor:
        input_df[plot_yvar] = input_df[plot_yvar] / yvar_divisor

    # Get interpolation line
    interpolator = sp.interpolate.interp1d(
        input_df[plot_xvar]
        ,input_df[plot_yvar]
        ,kind=interpolation_kind
        )
    interp_y = interpolator(gen_x)		# Calculate y-axis values on fit line
    gen_x_df[plot_yvar] = interp_y

    # Plot data
    fig = px.scatter(
        input_df
        ,x=plot_xvar
        ,y=plot_yvar
        ,text='scenario'
        ,hover_name='scenario'
        ,hover_data={
            'scenario':False    # Used for hover name, remove from hover data
            }
        )
    fig.update_traces(
        marker_size=20
        ,marker_color=plot_color
        ,textposition='top center'
        )

    # Plot fit line
    fig_interp = px.scatter(
        gen_x_df
        ,x=plot_xvar
        ,y=plot_yvar
        )
    fig_interp.update_traces(
        mode='lines'
        ,line_width=2
        ,line_color=plot_color
        )
    fig.add_trace(fig_interp.data[0])

    # Draw
    fig.update_layout(xaxis_title=plot_xvar ,yaxis_title=plot_yvar)
    fig.update_xaxes(dtick=0.2)
    return fig

# This function creates a plotly treemap with an option to show weighted averages
# instead of sums for boxes above the base level.
# It first calculates weighted averages using a pivot table, then draws the treemap by
# specifying the id and parent for each box.
# 2023/3/22: There is a bug causing a blank chart when AGGREGATION == 'mean'. Not using this at this time.
def create_treemap_withagg(
        INPUT_DF
        ,HIERARCHY              # List: categorical variables that define hierarchy, in desired order most to least aggregated
        ,COLOR_BY               # String: variable to color by. WARNING: must be one of the variables in HIERARCHY.
        ,VALUE_VAR              # String: variable with values to plot
        ,AGGREGATION='sum'      # String: how to aggregate VALUE_VAR. 'sum' (default) or 'mean'.
        ,WEIGHT_VAR=None        # String (optional): variable to use for weighting if AGGREGATION='mean'.
    ):
    if AGGREGATION == 'mean':
        dfmod = INPUT_DF.copy()

        # Create weighted value
        if WEIGHT_VAR:
            dfmod['treemap_weight'] = dfmod[WEIGHT_VAR]
        else:
            dfmod['treemap_weight'] = 1
        dfmod['treemap_weighted_value'] = dfmod[VALUE_VAR] * dfmod['treemap_weight']

        # For each variable in the hierarchy, create summary rows where that variable is ALL
        # Calculate the mean of the weighted value
        treemap_df = pd.DataFrame()     # Initialize dataframe to hold results
        for i ,VAR in enumerate(HIERARCHY):
            summary_rows = dfmod.pivot_table(
                index=HIERARCHY[:i+1]     # Index is all hierarchy variables up to i
                ,values=['treemap_weighted_value' ,'treemap_weight']
                ,aggfunc='sum'
                ).reset_index()
            # summary_rows['treemap_value'] = summary_rows['treemap_weighted_value'] / summary_rows['treemap_weight']
            treemap_df = pd.concat([treemap_df ,summary_rows] ,axis=0 ,ignore_index=True)

        # Add a row for the global total
        global_row = pd.DataFrame(dfmod[['treemap_weighted_value' ,'treemap_weight']].sum()).transpose()
        treemap_df = pd.concat([global_row ,treemap_df] ,axis=0 ,ignore_index=True)

        # Calculate weighted mean
        treemap_df['treemap_value'] = treemap_df['treemap_weighted_value'] / treemap_df['treemap_weight']

        # Drop rows with zero or negative value - these cause plotly to fail silently!
        treemap_df = treemap_df.query("treemap_value > 0")

        # Add columns for id and parent
        treemap_df['treemap_id'] = treemap_df[f'{HIERARCHY[0]}'].str.cat(treemap_df[HIERARCHY[1:]] ,sep='|' ,na_rep='_all_')
        treemap_df['treemap_id'] = treemap_df['treemap_id'].str.replace('|_all_' ,'' ,regex=False)
        treemap_df[['treemap_parent' ,'treemap_parent_remainder']] = treemap_df['treemap_id'].str.rsplit('|' ,n=1 ,expand=True)

        treemap_df.loc[treemap_df['treemap_parent_remainder'].isnull() ,'treemap_parent'] = '_all_'  # First level of hierarchy gets parent _all_
        treemap_df.loc[treemap_df['treemap_id'] == '_all_' ,'treemap_parent'] = ''  # Global level of hierarchy gets parent blank

        # Draw tree map
        # Figure is blank with no errors!!
        tree_map_fig = px.treemap(
            ids=treemap_df['treemap_id']
            ,parents=treemap_df['treemap_parent']
            ,values=treemap_df['treemap_value']
            ,color=treemap_df[COLOR_BY]
            )

        # Figure is blank with no errors!!
        # tree_map_fig = go.Figure(go.Treemap(
        #     ids=treemap_df['treemap_id']
        #     ,parents=treemap_df['treemap_parent']
        #     ,values=treemap_df['treemap_value']
        #     ))

    elif AGGREGATION == 'sum':
        tree_map_fig = px.treemap(
            INPUT_DF
            ,path=HIERARCHY
            ,values=VALUE_VAR
            ,color=COLOR_BY
            )

    return tree_map_fig



#%% 4. LAYOUT
##################################################################################################
# Here we layout the webpage, including dcc (Dash Core Component) controls we want to use, such as dropdowns.
##################################################################################################
app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    #### BRANDING & HEADING
    dbc.Row([

        # GBADs Branding
        dbc.Col(
            html.Div([
                html.A(href="https://animalhealthmetrics.org/",
                       target='_blank',
                       children=[
                       html.Img(title="Link to GBADS site", src=(os.environ.get("DASH_BASE_URL") if os.environ.get("DASH_BASE_URL") else "") + '/assets/GBADs-LOGO-Black-sm.png')
                       ]
                       ),
                html.H5("Inclusiveness Challenge Delivery Rigour Transparency",
                        style={"font-style": "italic",
                               "margin-top": "0",
                               "padding": "0"}),
                ], style = {'margin-left':"10px",
                            "margin-bottom":"10px",
                            'margin-right':"10px"},
                )
            ),
        ], justify='between'),
                            
    #### LANDING PAGE TEXT
        html.H3("Country Case Study: Animal Health Loss Envelope (AHLE)"),
        html.Label(["This interactive dashboard takes publicly available data and consults with \
                    experts to create models that provide a country-specific estimate of the \
                    animal health loss envelope. The tool will guide you through this calculations, \
                    the outputs, and the many scenarios that allow us to use the information to \
                    aid decision makers with regard to animal health and production."]),
    ### END OF LANDING PAGE TEXT
    
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
    
