# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    userdict = {}
    userrows = db(db.auth_user).select()
    for x in userrows:
        userdict[x.id] = x.first_name + " " + x.last_name
    a = 'active'
    rows = db.executesql("SELECT * FROM jobpost WHERE job_status = '"+a+"' ORDER BY id desc")
    #rows = db(db.jobpost.job_status=='active').select(orderby=~db.jobpost.id)
    if request.post_vars:
        r = db.executesql("SELECT if_cat_id FROM job_apply_data WHERE if_cat_id='"+request.post_vars.ifcat+"'")
        print(r)
        if len(r) == 0: 
            sql = "INSERT INTO job_apply_data(jobpost_id,if_cat_id,apply_date) VALUES('"+request.post_vars.jobpost_id+"','"+request.post_vars.ifcat+"','"+request.post_vars.post_date+"');"
            db.executesql(sql)
            response.flash = T('done')
            request.post_vars.if_cat_id = ""
        else :
            response.flash = T('alrady appled')
    else :
        response.flash = T('problem')


    return locals()

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
