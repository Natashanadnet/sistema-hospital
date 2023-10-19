from datetime import datetime, date
from . import db
from flask_login import UserMixin


class Paciente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    apellido = db.Column(db.String(120), nullable=False)
    fecha_nac = db.Column(db.Date, nullable=False)
    num_ci = db.Column(db.String(20), nullable=False)
    signos_vit = db.relationship(
        "Signos", backref="paciente", lazy=True
    )  # mayus post porque se refiere a la clase

    def __repr__(
        self,
    ):
        return f"Paciente ('{self.nombre}', '{self.apellido}')"


class Signos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pres_art_sis = db.Column(db.String(3), nullable=False)
    pres_art_dia = db.Column(db.String(3), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    frec_car = db.Column(db.String(3), nullable=False)
    paciente_id = db.Column(
        db.Integer, db.ForeignKey("paciente.id"), nullable=False
    )  # min el paciente porque se refiere a la tabla

    def __repr__(self):
        return f"Signos Vitales ('{self.pres_art_sis}', '{self.pres_art_dia}', '{self.frec_car}', '{self.fecha}')"
