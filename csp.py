import flask_talisman


def configure_csp(app):
    csp = dict(flask_talisman.GOOGLE_CSP_POLICY)
    csp["default-src"] = ['\'self\'', 'kit.fontawesome.com',
                          'ka-f.fontawesome.com', '*.googleusercontent.com']
    csp["script-src"] = ['\'self\'', 'kit.fontawesome.com']
    csp["style-src"] = ['\'self\'', '\'unsafe-inline\'', 'fonts.googleapis.com']
    csp['font-src'] = ['\'self\'', 'ka-f.fontawesome.com',
                       'themes.googleusercontent.com', '*.gstatic.com']
    flask_talisman.Talisman(app, content_security_policy=csp)
