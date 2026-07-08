import json

from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class ModelName(http.Controller):
    _items_per_page = 20
    @http.route(['/project/render', '/project/render/page/<int:page>'],
                type="http", auth="user", website=True)
    def project_renders_list(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        # values = self._prepare_portal_layout_values()
        Project = request.env['project.project']
        domain = []

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
        domain += ['|', ('partner_id', '=', request.env.user.partner_id.id), ('user_id', '=', request.env.user.id)]

        # projects count
        project_count = Project.search_count(domain)
        # pager
        pager = portal_pager(
            url="/project/render",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=project_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        projects = Project.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_projects_history'] = projects.ids[:100]

        values = {
            'date': date_begin,
            'date_end': date_end,
            'projects': projects,
            'page_name': 'project',
            'default_url': '/project/render',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        }
        return request.render("project_render_journey.portal_my_projects", values)

    @http.route(['/project/render/<int:project_id>'], type="http", auth="user", website=True)
    def project_render(self, project_id=None, access_token=None, **kw):
        project = request.env['project.project'].sudo().browse(project_id)
        project_renders = request.env['project.renders'].sudo().search([('project_id', '=', project_id)])
        values = {
            'page_name': 'project_render',
            'project': project,
            'project_renders': project_renders,
            'default_url': '/project/render/',
        }
        return request.render("project_render_journey.portal_project_renders", values)

    @http.route(['/project/journey', '/project/journey/page/<int:page>'],
                type="http", auth="user", website=True)
    def project_journey_list(self, page=1, date_begin=None, date_end=None,
                            sortby=None, **kw):
        Project = request.env['project.project']
        domain = []

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
        domain += ['|', ('partner_id', '=', request.env.user.partner_id.id), ('user_id', '=', request.env.user.id)]

        # projects count
        project_count = len(request.env['project.journey'].sudo().search(
            []).mapped('project_id').filtered(
            lambda project: project.partner_id.id ==
                            request.env.user.partner_id.id or
                            project.user_id.id ==
                            request.env.user.id
        ))
        # pager
        pager = portal_pager(
            url="/project/journey",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=project_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        projects = Project.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_projects_history'] = projects.ids[:100]
        project_journey = request.env['project.journey'].sudo().search([]).mapped('project_id')
        common_projects = projects and project_journey

        values = {
            'date': date_begin,
            'date_end': date_end,
            'projects': common_projects,
            'page_name': 'project',
            'default_url': '/project/journey',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        }
        return request.render("project_render_journey.portal_my_projects_journey", values)

    @http.route(['/project/journey/<int:project_id>'], type="http", auth="user", website=True)
    def project_journey(self, project_id=None, access_token=None, **kw):
        project = request.env['project.project'].sudo().browse(project_id)
        project_journey = request.env['project.journey'].sudo().search([('project_id', '=', project_id)])
        values = {
            'page_name': 'project_journey',
            'project': project,
            'project_renders': project_journey,
            'default_url': '/project/journey/',
        }
        return request.render("project_render_journey.portal_project_journey", values)
