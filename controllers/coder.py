import os
import datetime
@auth.requires_login()
def my_problems():
    my_problems = db(db.problem).select()
    return dict(my_problems=my_problems)

def echo():
    return "jQuery('#target').html(%s);" % repr(request.vars.name)

def echo3():
    print "hola en echo3"
    print request.vars
    to_stdout = "salida"
    return DIV("Message posted")
    #return "jQuery('#edit_stdout').html(%s);" % repr(request.vars.src_code)

def echo4():
    to_stdout = "salida2"
def echo2():
    print "hola"
    print request.vars.name
    return request.vars.name


def new_test_code():
    form = SQLFORM(db.src_test_files)
    print "hola"
    print request.args
    print request.vars
    if form.accepts(request, formname=None):
        print request.args
        print request.vars
        print form
    return "jQuery('#target2').html(%s);" % "hola corola"


@auth.requires_login()
def my_problem():

    problem_id = request.args(0)
    problem = db.problem(problem_id) or redirect(URL('index'))

    form_src = FORM('Nombre del archivo', INPUT(_name='src_code',_id='src_code', _type='hidden'), INPUT(_name='src_stdin',_id='src_stdin', _type='hidden'), INPUT(_name='prog_lang',_id='prog_lang', _type='hidden'), INPUT(_name='filename',_id='filename', requires = IS_NOT_EMPTY() ),  INPUT(_class='btn btn-primary',_type='submit'), formstyle='bootstrap4_inline')

    form_src.element(_type='submit')['_value'] = T("Enviar código")

    posts= db(db.post.problem_id == problem_id).select()
    form_post = SQLFORM.factory(Field('question', label='¿Quieres preguntar algo?, pregúntalo aquí', requires=IS_NOT_EMPTY()), table_name='dummy_question_table')
    
    # Revisar validacion del formulario del editor de codigo
    if form_src.validate():
        # Obtener el valor del campo oculto
        src_code = form_src.vars.src_code
        prog_lang =  form_src.vars.prog_lang
        filename =  form_src.vars.filename
        # Imprimir en la terminal el valor
        selected_output = db().select(db.exec_status.ALL).first()
        previously_sent = db((db.submission.user_id==auth.user_id) & (db.submission.problem_id == problem_id)).select().first()
        if previously_sent != None:
            accepted_on = previously_sent.accepted_on
        else:
            accepted_on = datetime.datetime.now()
        now = datetime.datetime.now()
        if (now - accepted_on ) >= datetime.timedelta(seconds=5*60*60):
            session.flash = 'Tus 5 horas han transcurrido, ya no puedes enviar más soluciones de este desafío.'
            redirect(URL('my_submissions'))


        #db(db.submission.id == form.vars.id).update(problem_id = problem_id, user_id = auth.user_id, output_id = selected_output, accepted_on = accepted_on, sended_on=now )

        idx = db.submission.insert(problem_id = problem_id, prog_lang_id= form_src.vars.prog_lang, filename = filename, src_code = src_code, output_id = selected_output, accepted_on = accepted_on, sended_on=now)
        redirect(URL('my_problems'))


    if form_post.process().accepted:
        db.post.insert(problem_id=problem_id,user_id=auth.user_id,question=form_post.vars.question)
        session.flash = 'Pregunta enviada'
        redirect(URL('my_submission'))


    return dict(problem=problem, form = "hola", form_src = form_src,  posts = posts, form_post = form_post)
