
def get_responder(request):
    user=request.user
    if user.department.leader.uid == user.uid:
        if user.department.name == 'Board of Directors':
            responder = None
        else:
            responder = user.department.manager
    else:
        responder = user.department.leader

    return responder