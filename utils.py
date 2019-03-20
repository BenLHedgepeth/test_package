
def set_redirect(fallback):
    
    next = request.args.get('next')
    try: 
        redirect_url = url_for(next)
    except BuildError:
        return redirect(fallback)
    return redirect(url_for(redirect_url))