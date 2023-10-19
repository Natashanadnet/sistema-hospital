from website.forms import (
    AgregarPaciente,
    ActualizarPaciente,
    AgregarSignos,
    EditarSignos,
)
from flask import render_template, url_for, redirect, flash, Blueprint, request
from website.models import Paciente, Signos
from . import db
import datetime
import pytz


routes = Blueprint("routes", __name__)


@routes.route("/buscar", methods=["GET", "POST"])
def buscar():
    if request.method == "POST":
        seleccion = request.form["buscarpor"]
        if seleccion == "nom":
            entrada_paciente = (request.form["barraBuscar"]).title()
            lista_paciente = entrada_paciente.split()

            if len(lista_paciente) != 2:
                flash(
                    "Inserte el nombre del paciente seguido por el apellido",
                    category="danger",
                )
            elif len(lista_paciente) == 2:
                paciente = Paciente.query.filter_by(
                    nombre=lista_paciente[0], apellido=lista_paciente[1]
                ).first()

                if paciente:
                    return redirect(
                        url_for("routes.resultado", paciente=entrada_paciente)
                    )
                else:
                    flash(
                        f"El paciente {entrada_paciente} no se encuentra registrado",
                        category="danger",
                    )
        elif seleccion == "cod":
            campo = request.form["barraBuscar"]
            id_paciente = int(campo)
            paciente = Paciente.query.get(id_paciente)
            if paciente:
                return redirect(url_for("routes.ficha_pac", id=id_paciente))
            else:
                flash(
                    f"El paciente con código {campo} no se encuentra registrado",
                    category="danger",
                )
        else:
            flash(
                "Datos inválidos, selccione una opción antes de oprimir 'Buscar'",
                category="danger",
            )

    return render_template("buscar.html", title="Buscar Paciente", page="buscar")


@routes.route("/resultado/<paciente>", methods=["GET", "POST"])
def resultado(paciente):
    paciente = paciente
    lista_paciente = paciente.split()
    nombre = lista_paciente[0]
    apellido = lista_paciente[1]
    pacientes_con_nom = Paciente.query.filter_by(nombre=nombre, apellido=apellido)
    return render_template(
        "resultado.html", title="Resultado", pacientes=pacientes_con_nom
    )


@routes.route("/", methods=["GET", "POST"])
@routes.route("/lista")
def lista():
    pacientes = Paciente.query.all()
    return render_template(
        "lista.html", title="Listado", pacientes=pacientes, page="lista"
    )


@routes.route("/nuevo_pac", methods=["GET", "POST"])
def nuevo_pac():
    form = AgregarPaciente()
    if form.validate_on_submit():
        paciente = Paciente(
            nombre=(form.nombre.data).capitalize(),
            apellido=(form.apellido.data).capitalize(),
            fecha_nac=form.fecha_nac.data,
            num_ci=form.num_ci.data,
        )
        db.session.add(paciente)
        db.session.commit()
        flash(
            f"El paciente {(form.nombre.data).capitalize()} {(form.apellido.data).capitalize()} fue agregado.",
            category="success",
        )
        current_paciente = Paciente.query.filter_by(num_ci=form.num_ci.data).first()
        return redirect(url_for("routes.ficha_pac", id=current_paciente.id))
    return render_template(
        "nuevo_pac.html", title="Nuevo Paciente", form=form, page="nuevo"
    )


@routes.route("/ficha_pac/<id>", methods=["GET", "POST"])
def ficha_pac(id):
    form = AgregarSignos()
    paciente = Paciente.query.get(id)
    signos = Signos.query.filter_by(paciente_id=id)
    return render_template(
        "ficha_pac.html", title="Paciente", paciente=paciente, form=form, signos=signos
    )


@routes.route("/actualizar/<id>", methods=["GET", "POST"])
def actualizar(id):
    paciente = Paciente.query.get(id)
    form = ActualizarPaciente()
    if form.validate_on_submit():
        paciente.nombre = (form.nombre.data).capitalize()
        paciente.apellido = (form.apellido.data).capitalize()
        paciente.fecha_nac = form.fecha_nac.data
        paciente.num_ci = form.num_ci.data
        db.session.commit()
        flash("El paciente fue actualizado!", "success")
        return redirect(url_for("routes.ficha_pac", id=paciente.id))
    elif request.method == "GET":
        form.nombre.data = paciente.nombre
        form.apellido.data = paciente.apellido
        form.fecha_nac.data = paciente.fecha_nac
        form.num_ci.data = paciente.num_ci

    return render_template(
        "actualizar.html", title="actualizar", paciente=paciente, form=form
    )


@routes.route("/editar/<id>", methods=["GET", "POST"])
def editar(id):
    signo = Signos.query.get(id)
    paciente_id = signo.paciente_id
    form = EditarSignos()
    if form.validate_on_submit():
        signo.pres_art_sis = form.pres_art_sis.data
        signo.pres_art_dia = form.pres_art_dia.data
        signo.frec_car = form.frec_car.data
        db.session.commit()
        flash("El registro fue editado!", "success")
        return redirect(url_for("routes.ficha_pac", id=paciente_id))
    elif request.method == "GET":
        form.pres_art_sis.data = signo.pres_art_sis
        form.pres_art_dia.data = signo.pres_art_dia
        form.frec_car.data = signo.frec_car

        return render_template(
            "editar_registro.html", title="editar_registro", signo=signo, form=form
        )


@routes.route("/lista/<id>/delete", methods=["POST", "GET"])
def delete(id):
    paciente = Paciente.query.get(id)
    signos = Signos.query.filter_by(paciente_id=paciente.id)
    for registro in signos:
        db.session.delete(registro)
    db.session.delete(paciente)
    db.session.commit()
    flash("El paciente fue eliminado!", "success")

    return redirect(url_for("routes.lista"))


@routes.route("/ficha_pac/<id>/delete_registro", methods=["POST", "GET"])
def delete_registro(id):
    signo = Signos.query.get(id)
    paciente_id = signo.paciente_id
    db.session.delete(signo)
    db.session.commit()
    flash("El registro fue eliminado!", "success")
    return redirect(url_for("routes.ficha_pac", id=paciente_id))


@routes.route("/ficha_pac/<id>/agregar_sig", methods=["GET", "POST"])
def agregar_sig(id):

    paciente = Paciente.query.get(id)
    form = AgregarSignos()
    # para la hora actual:
    tz_info = pytz.timezone("America/Asuncion")
    dt = datetime.datetime.now(tz=tz_info)
    tiempo_actual = dt.replace(microsecond=0)

    if form.validate_on_submit():
        signo = Signos(
            pres_art_sis=form.pres_art_sis.data,
            pres_art_dia=form.pres_art_dia.data,
            frec_car=form.frec_car.data,
            fecha=tiempo_actual,
            paciente=paciente,
        )
        db.session.add(signo)
        db.session.commit()
        flash(
            f"El registro fue agregado.",
            category="success",
        )
        return redirect(url_for("routes.ficha_pac", id=paciente.id))


@routes.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("error404.html"), 404
