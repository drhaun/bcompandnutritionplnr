from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    """Client model to store client information and test results"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    weight_kg = db.Column(db.Float)
    weight_lbs = db.Column(db.Float)
    height_cm = db.Column(db.Float)
    height_in = db.Column(db.Float)
    test_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # RMR specific data
    rmr_kcal_day = db.Column(db.Float)
    vo2_avg = db.Column(db.Float)
    vco2_avg = db.Column(db.Float)
    rer_avg = db.Column(db.Float)
    predicted_rmr = db.Column(db.Float)
    rmr_percent_predicted = db.Column(db.Float)
    fat_oxidation = db.Column(db.Float)
    carb_oxidation = db.Column(db.Float)
    protein_oxidation = db.Column(db.Float)
    
    # Body composition specific data
    body_fat_percent = db.Column(db.Float)
    lean_mass_kg = db.Column(db.Float)
    lean_mass_lbs = db.Column(db.Float)
    fat_mass_kg = db.Column(db.Float)
    fat_mass_lbs = db.Column(db.Float)
    water_percent1 = db.Column(db.Float)
    water_percent2 = db.Column(db.Float)
    water_percent3 = db.Column(db.Float)
    water_device1 = db.Column(db.String(50))
    water_device2 = db.Column(db.String(50))
    water_device3 = db.Column(db.String(50))
    water_liters1 = db.Column(db.Float)
    water_liters2 = db.Column(db.Float)
    water_liters3 = db.Column(db.Float)
    water_liters_avg = db.Column(db.Float)
    water_liters_final = db.Column(db.Float)
    specific_gravity = db.Column(db.Float)
    scan_device = db.Column(db.String(50))  # Fit3D or Styku
    
    def to_dict(self):
        """Convert client object to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'gender': self.gender,
            'weight_kg': self.weight_kg,
            'weight_lbs': self.weight_lbs,
            'height_cm': self.height_cm,
            'height_in': self.height_in,
            'test_date': self.test_date.strftime('%Y-%m-%d') if self.test_date else None,
            
            # RMR data
            'rmr_kcal_day': self.rmr_kcal_day,
            'vo2_avg': self.vo2_avg,
            'vco2_avg': self.vco2_avg,
            'rer_avg': self.rer_avg,
            'predicted_rmr': self.predicted_rmr,
            'rmr_percent_predicted': self.rmr_percent_predicted,
            'fat_oxidation': self.fat_oxidation,
            'carb_oxidation': self.carb_oxidation,
            'protein_oxidation': self.protein_oxidation,
            
            # Body composition data
            'body_fat_percent': self.body_fat_percent,
            'lean_mass_kg': self.lean_mass_kg,
            'lean_mass_lbs': self.lean_mass_lbs,
            'fat_mass_kg': self.fat_mass_kg,
            'fat_mass_lbs': self.fat_mass_lbs,
            'water_percent1': self.water_percent1,
            'water_percent2': self.water_percent2,
            'water_percent3': self.water_percent3,
            'water_device1': self.water_device1,
            'water_device2': self.water_device2,
            'water_device3': self.water_device3,
            'water_liters1': self.water_liters1,
            'water_liters2': self.water_liters2,
            'water_liters3': self.water_liters3,
            'water_liters_avg': self.water_liters_avg,
            'water_liters_final': self.water_liters_final,
            'specific_gravity': self.specific_gravity,
            'scan_device': self.scan_device,
            
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class RmrData(db.Model):
    """Model to store raw RMR data points"""
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    time_point = db.Column(db.String(10))  # e.g., "0:00", "0:14", etc.
    tidal_volume = db.Column(db.Float)
    respiratory_rate = db.Column(db.Float)
    vo2_ml_min = db.Column(db.Float)
    vo2_ml_kg_min = db.Column(db.Float)
    ve_vo2 = db.Column(db.Float)
    feo2 = db.Column(db.Float)
    vco2_ml_min = db.Column(db.Float)
    vco2_ml_kg_min = db.Column(db.Float)
    ve_vco2 = db.Column(db.Float)
    feco2 = db.Column(db.Float)
    rer = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert RMR data point to dictionary"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'time_point': self.time_point,
            'tidal_volume': self.tidal_volume,
            'respiratory_rate': self.respiratory_rate,
            'vo2_ml_min': self.vo2_ml_min,
            'vo2_ml_kg_min': self.vo2_ml_kg_min,
            've_vo2': self.ve_vo2,
            'feo2': self.feo2,
            'vco2_ml_min': self.vco2_ml_min,
            'vco2_ml_kg_min': self.vco2_ml_kg_min,
            've_vco2': self.ve_vco2,
            'feco2': self.feco2,
            'rer': self.rer,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class BodyCompositionData(db.Model):
    """Model to store body composition measurement data"""
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    scan_date = db.Column(db.DateTime)
    
    # 3D Scanner measurements
    measurement_type = db.Column(db.String(20))  # 'Fit3D' or 'Styku'
    measurement_name = db.Column(db.String(50))
    measurement_value = db.Column(db.Float)
    measurement_unit = db.Column(db.String(10))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert body composition data point to dictionary"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'scan_date': self.scan_date.strftime('%Y-%m-%d %H:%M:%S') if self.scan_date else None,
            'measurement_type': self.measurement_type,
            'measurement_name': self.measurement_name,
            'measurement_value': self.measurement_value,
            'measurement_unit': self.measurement_unit,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class UltrasoundData(db.Model):
    """Model to store body composition ultrasound data"""
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    date = db.Column(db.DateTime)
    
    # Ultrasound measurements
    site_name = db.Column(db.String(20))  # e.g., 'Chest', 'Waist', 'Thigh', etc.
    measurement_value = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert ultrasound data point to dictionary"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S') if self.date else None,
            'site_name': self.site_name, 
            'measurement_value': self.measurement_value,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
