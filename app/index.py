from flask import Flask, redirect, url_for
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView, SimpleFormView
from flask_appbuilder.forms import DynamicForm
from wtforms import StringField, TextAreaField, BooleanField, FloatField, DateTimeField, DateTimeLocalField, TimeField, Field
import uuid
from wtforms.validators import DataRequired
from sqlalchemy import Column, String, Boolean, Text, Float, TIMESTAMP, Index, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from shapely import wkt
import os

app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:wykRJb.HvkkpVn9@db.psujsjvxctszhfxhduzk.supabase.co:5432/postgres"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/appbuilder"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSRF_ENABLED'] = True
app.config.update(SECRET_KEY=os.urandom(24))

db = SQLA(app)
appbuilder = AppBuilder(app, db.session)
@app.route('/')
def home():
    return redirect(url_for('PoiModelView.list'))
def convert_to_geometry(wkt_string):
    try:
        geometry = wkt.loads(wkt_string)
        return geometry
    except Exception as e:
        # Log the error and return None if conversion fails
        print(f"Error converting string to geometry: {e}")
        return None
    
class GeometryWidget(StringField):
    def _call_(self, field, **kwargs):
        # Custom rendering logic here if needed
        return super(GeometryWidget, self)._call_(field, **kwargs)

class GeometryField(Field):
    widget = GeometryWidget()
    
    def _value(self):
        # Convert geometry object to string representation if needed
        if self.data:
            return str(self.data)
        return ''
    
    def process_formdata(self, valuelist):
        if valuelist:
            # Convert string representation to geometry object if needed
            self.data = convert_to_geometry(valuelist[0])  # Implement convert_to_geometry as needed
        else:
            self.data = None


class Poi(db.Model):
    __tablename__ = 'poi'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        Index('poi_attributes_idx', 'attributes', postgresql_using='gin'),
        Index('poi_category_idx', 'category', postgresql_using='btree'),
        Index('poi_geom_idx', 'geom', postgresql_using='gist'),
        Index('poi_grid_idx', 'grid', postgresql_using='btree'),
        Index('poi_subcategory_idx', 'subcategory', postgresql_using='btree'),
    )

    id = Column(String(40), nullable=False, default=str(uuid.uuid1()))
    is_active = Column(Boolean)
    name = Column(Text)
    category = Column(Text)
    subcategory = Column(Text)
    description = Column(Text)
    address_street = Column(Text)
    address_city = Column(Text)
    address_state = Column(Text)
    address_postcode = Column(Text)
    address_country = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    phone = Column(Text)
    website = Column(Text)
    opening_hours = Column(Text)
    operational_status = Column(Text)
    notes = Column(Text)
    attributes = Column(JSONB, server_default='{}')
    grid = Column(String(8), nullable=False)
    geom = Column(Geometry(geometry_type='POINT'))
    google_place_id = Column(Text)
    google_place_updated_time = Column(TIMESTAMP)
    updated_time = Column(TIMESTAMP)
    source_attributes = Column(JSONB, server_default='{}')
    source = Column(Text, nullable=False)
    source_id = Column(Text, nullable=False)
    source_updated_time = Column(TIMESTAMP)

class PoiForm(DynamicForm):
    # id = StringField('ID')
    is_active = BooleanField('Is Active')
    name = StringField('Name')
    category = StringField('Category')
    subcategory = StringField('Subcategory')  # Include the 'subcategory' field here
    description = TextAreaField('Description')
    address_street = TextAreaField('Street Address')
    address_city = StringField('City')
    address_state = StringField('State')
    address_postcode = StringField('Postal Code')
    address_country = StringField('Country')
    latitude = FloatField('Latitude')
    longitude = FloatField('Longitude')
    phone = StringField('Phone')
    website = StringField('Website')
    opening_hours = StringField('Opening Hours')
    operational_status = StringField('Operational Status')
    notes = TextAreaField('Notes')
    attributes = TextAreaField('Attributes')
    grid = StringField('Grid')
    geom = StringField('Geometry')
    google_place_id = StringField('Google Place ID')
    updated_time = DateTimeLocalField('Updated Time')
    source_attributes = TextAreaField('Source Attributes')
    source = StringField('Source')
    source_id = StringField('Source ID')
class PoiView(ModelView):
    datamodel = SQLAInterface(Poi)
    list_columns = ['id', 'name', 'category', 'subcategory', 'description', 'address_street', 'address_city', 'address_state', 'address_postcode', 'address_country', 'latitude', 'longitude', 'phone', 'website', 'opening_hours', 'operational_status', 'notes']
    show_fieldsets = [('Summary', {'fields': ['id', 'name', 'category', 'subcategory']}),
                      ('Address', {'fields': ['address_street', 'address_city', 'address_state', 'address_postcode', 'address_country']}),
                      # Add other groupings as needed
                      ]
    add_form = PoiForm
    edit_form = PoiForm
    add_columns = edit_columns = ['is_active', 'name', 'category', 'subcategory', 'description', 'address_street', 'address_city', 'address_state', 'address_postcode', 'address_country', 'latitude', 'longitude', 'phone', 'website', 'opening_hours', 'operational_status', 'notes', 'attributes', 'grid', 'geom', 'google_place_id',  'source_attributes', 'source', 'source_id',]
    search_columns = ['id', 'name', 'category', 'subcategory', 'description', 'address_street', 'address_city', 'address_state', 'address_postcode', 'address_country', 'latitude', 'longitude', 'phone', 'website', 'opening_hours', 'operational_status', 'notes']
    related_views = []



appbuilder.add_view(PoiView, "Pois", icon="fa-table")

if __name__ == '__main__':
    app.run(debug=True)
