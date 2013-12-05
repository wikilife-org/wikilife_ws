

def add_uri_to_doc(app, what, name, obj, options, lines):
    if what is "class":
        lines.insert(0, "\n")
        lines.insert(0, ':magenta:`Base URI: ' + obj._uri + '`')
    if what is "method":
        method_name = name.split(".")[-1]
        lines.insert(0, "\n")
        lines.insert(0, "**Method: {}**".format(method_name.upper()))

    if (hasattr(obj, '_deprecated_since')):
        lines.insert(0, "")
        lines.insert(0, "This method is deprecated since {}".format(str(obj._deprecated_since)))
        lines.insert(0, "")
        lines.insert(0, ".. warning::")
        lines.insert(0, "")


def depythonify_doc(app, what, name, obj, options, signature, return_annotation):
    return (" ", "")


def setup(app):
    app.connect("autodoc-process-docstring", add_uri_to_doc)
    app.connect("autodoc-process-signature", depythonify_doc)
