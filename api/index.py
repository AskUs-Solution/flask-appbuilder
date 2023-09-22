from flask import Flask, redirect, url_for
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView
from sqlalchemy import Column, String, Boolean, Text, Float, TIMESTAMP, Index, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:wykRJb.HvkkpVn9@db.psujsjvxctszhfxhduzk.supabase.co:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSRF_ENABLED'] = True
app.config.update(SECRET_KEY=os.urandom(24))

db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

# @app.route('/')
# def home():
#     return redirect(url_for('PoiModelView.list'))

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

    id = Column(String(40), nullable=False)
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
    # attributes = Column(JSONB, server_default='{}')
    grid = Column(String(8), nullable=False)
    # geom = Column(Geometry(geometry_type='POINT'))
    google_place_id = Column(Text)
    google_place_updated_time = Column(TIMESTAMP)
    updated_time = Column(TIMESTAMP)
    # source_attributes = Column(JSONB, server_default='{}')
    source = Column(Text, nullable=False)
    source_id = Column(Text, nullable=False)
    source_updated_time = Column(TIMESTAMP)

class PoiView(ModelView):
    datamodel = SQLAInterface(Poi)
    list_columns = ['id', 'name', 'category', 'subcategory', 'description', 'address_street', 'address_city', 'address_state', 'address_postcode', 'address_country', 'latitude', 'longitude', 'phone', 'website', 'opening_hours', 'operational_status', 'notes']
    show_fieldsets = [('Summary', {'fields': ['id', 'name', 'category', 'subcategory']}),
                      ('Address', {'fields': ['address_street', 'address_city', 'address_state', 'address_postcode', 'address_country']}),
                      # Add other groupings as needed
                      ]
    add_columns = edit_columns = ['is_active', 'name', 'category', 'subcategory', 'description', 'address_street', 'address_city', 'address_state', 'address_postcode', 'address_country', 'latitude', 'longitude', 'phone', 'website', 'opening_hours', 'operational_status', 'notes', 'attributes', 'grid', 'geom', 'google_place_id', 'google_place_updated_time', 'updated_time', 'source_attributes', 'source', 'source_id', 'source_updated_time']
    search_columns = ['id', 'name', 'category', 'subcategory', 'description', 'address_street', 'address_city', 'address_state', 'address_postcode', 'address_country', 'latitude', 'longitude', 'phone', 'website', 'opening_hours', 'operational_status', 'notes']
    related_views = []

# appbuilder.add_view(PoiView, "Pois", icon="fa-table")

if __name__ == '__main__':
    app.run(debug=True)
