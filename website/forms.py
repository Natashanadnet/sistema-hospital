from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from .models import Paciente, Signos
from flask_login import current_user
import datetime


class AgregarPaciente(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(min=2, max=20)])
    apellido = StringField(
        "Apellido", validators=[DataRequired(), Length(min=2, max=20)]
    )
    fecha_nac = DateField("Fecha de nacimiento", validators=[DataRequired()])
    num_ci = StringField(
        "Número de cedula", validators=[DataRequired(), Length(min=6, max=8)]
    )
    registrar = SubmitField("Agregar Paciente")

    def validate_num_ci(self, num_ci):
        paciente = Paciente.query.filter_by(num_ci=num_ci.data).first()
        if paciente:
            raise ValidationError(
                f"El paciente con el número de cedula {num_ci.data} ya existe"
            )

    def validate_fecha_nac(self, fecha_nac):
        fecha_nac = fecha_nac.data
        # fecha_nac_modi = datetime.datetime.strptime(fecha_nac, "%Y-%m-%d").date()
        if fecha_nac > datetime.date.today():  # no puede ser mayor que la fecha actual
            raise ValidationError("No puede nacer en el futuro!")


class ActualizarPaciente(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(min=2, max=20)])
    apellido = StringField(
        "Apellido", validators=[DataRequired(), Length(min=2, max=20)]
    )
    fecha_nac = DateField("Fecha de nacimiento", validators=[DataRequired()])
    num_ci = StringField(
        "Número de cedula", validators=[DataRequired(), Length(min=6, max=8)]
    )
    registrar = SubmitField("Actualizar")

    def validate_fecha_nac(self, fecha_nac):
        fecha_nac = fecha_nac.data
        # fecha_nac_modi = datetime.datetime.strptime(fecha_nac, "%Y-%m-%d").date()
        if fecha_nac > datetime.date.today():  # no puede ser mayor que la fecha actual
            raise ValidationError("No puede nacer en el futuro!")


class AgregarSignos(FlaskForm):
    pres_art_sis = StringField(
        "Presión arterial (SIS)", validators=[DataRequired(), Length(min=1, max=3)]
    )
    pres_art_dia = StringField(
        "Presión arterial (DIA)", validators=[DataRequired(), Length(min=2, max=3)]
    )
    frec_car = StringField(
        "Frecuencia cardiaca", validators=[DataRequired(), Length(min=2, max=3)]
    )

    registrar = SubmitField("Registrar")


class EditarSignos(FlaskForm):
    pres_art_sis = StringField(
        "Presión arterial (SIS)", validators=[DataRequired(), Length(min=1, max=3)]
    )
    pres_art_dia = StringField(
        "Presión arterial (DIA)", validators=[DataRequired(), Length(min=2, max=3)]
    )
    frec_car = StringField(
        "Frecuencia cardiaca", validators=[DataRequired(), Length(min=2, max=3)]
    )

    editar = SubmitField("Editar")
