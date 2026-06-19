"""Utility helpers and Jinja2 filters."""


def register_template_filters(app):
    @app.template_filter('enumerate')
    def jinja_enumerate(iterable):
        return enumerate(iterable)

    @app.template_filter('abs')
    def jinja_abs(value):
        return abs(value)
