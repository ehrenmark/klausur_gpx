import gpxpy
from gpxpy.gpx import GPXTrackPoint
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLAlchemy-Modell für die Datenbanktabelle erstellen
Base = declarative_base()

class TrackPoint(Base):
    __tablename__ = 'track_points'
    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
    time = Column(DateTime)

# SQLite-Datenbank erstellen und Tabelle erstellen
engine = create_engine('sqlite:///gpx_data.db', echo=True)
Base.metadata.create_all(engine)

# GPX-Datei öffnen und Daten in die Datenbank speichern
print("Dateipfad:")
path = input()

gpx_file = open(path, 'r')
gpx = gpxpy.parse(gpx_file)

Session = sessionmaker(bind=engine)
session = Session()

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            lat = point.latitude
            lon = point.longitude
            ele = point.elevation
            time = point.time

            track_point = TrackPoint(latitude=lat, longitude=lon, elevation=ele, time=time)
            session.add(track_point)

session.commit()
session.close()

