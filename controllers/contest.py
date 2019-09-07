# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
def edit_contests():
    links = [lambda row: A('Problemas',_href=URL("contest","edit_problems_by_contest",args=[row.id], user_signature=True))]
    form = SQLFORM.grid(db.contest, links=links, maxtextlength=50, details=False)
    return dict(form=form)

# :contest_problem: contest_id, problem_id
@auth.requires_login()
def edit_problems_by_contest():
    contest_id = request.args(0)
    links = [lambda row: A('Descripción',_href=URL("contest","edit_problem",args=[row.problem_id], user_signature=True))]
    db.problems_by_contest.contest_id.readable = False
    query = db(db.problems_by_contest.contest_id == contest_id)

    form = SQLFORM.grid(query, links = links, maxtextlength=50, details=False)
    return dict(form=form)

@auth.requires_login()
def edit_problem():
    problem_id = request.args(0)
    form = SQLFORM(db.problem, problem_id, maxtextlength=50, deletable = False, details=False)
    return dict(form=form)
