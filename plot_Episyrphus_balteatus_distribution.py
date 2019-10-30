from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, TapTool, OpenURL
from bokeh.models.tools import HoverTool
from bokeh.tile_providers import get_provider, Vendors
import pandas as pd

input_file = '/home/chris/Dropbox/Python/species_mapping/Data/Insecta/Diptera/Episyrphus_balteatus_extended_3857.csv'
output_file('/home/chris/Dropbox/Python/species_mapping/distribution_modelling/Episyrphus_balteatus.html')

# Read the csv to a dataframe:
df = pd.read_csv(input_file, sep=',')

# Create a data source of the type ColumnDataSource:
source = ColumnDataSource(df)

# Get map tile provider (in EPSG:3857):
tile_provider = get_provider(Vendors.CARTODBPOSITRON)

# range bounds supplied in web mercator coordinates
p = figure(x_axis_type="mercator", y_axis_type="mercator", plot_width=1200, plot_height=960, tools=['pan', 'tap',
                                                                                                    'wheel_zoom',
                                                                                                    'save', 'reset'])
p.title.text = 'Occurence of the marmelade hoverfly (Episyrphus balteatus) in the Netherlands'
p.xaxis.axis_label = 'Longitude'
p.yaxis.axis_label = 'Latitude'
p.add_tile(tile_provider)
# Add species data (points)
p.circle(x="lat_3857", y="lon_3857", size=5, fill_color="green", fill_alpha=0.8, source=source)
# Add a hovertool:
hover = HoverTool()
hover.tooltips=[
    ('Location', '@locality'),
    ('Number of Individuals counted', '@individualCount'),
    ('Observation Date', '{0}-{1}-{2}'.format('@day','@month', '@year')),
    ('Rights Holder', '@rightsHolder')
]
p.add_tools(hover)

url = "@occurrenceID/"
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)

show(p)
