from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    project_attachment_counts = fields.Integer(
        string="Project Images",
        compute="_compute_project_attachment_counts")
    project_journey_counts = fields.Integer(
        string="Project Journey",
        compute="_compute_project_journey_counts")

    def _compute_project_attachment_counts(self):
        for rec in self:
            rec.project_attachment_counts =\
                self.env['project.renders'].search_count([
                    ('project_id', '=', rec.id)
                ])

    def _compute_project_journey_counts(self):
        for rec in self:
            rec.project_journey_counts =\
                self.env['project.journey'].search_count([
                    ('project_id', '=', rec.id)
                ])

    def project_attachment_tree_view(self):
        action = self.env.ref('project_render_journey.project_renders_action')
        view_id = self.env.ref(
            'project_render_journey.project_renders_form_view').id
        context = self._context.copy()
        context.update({'default_project_id': self.id})
        project_render = self.env['project.renders'].search(
            [('project_id', '=', self.id)], limit=1)
        action_dict = {
            'name': action.name,
            'view_type': 'form',
            'view_mode': action.view_mode,
            'views': [(view_id, 'form')],
            'res_model': action.res_model,
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': project_render.id if project_render else False,
            'target': 'current',
            'context': context,
        }
        return action_dict

    def project_journey_tree_view(self):
        """
            Open the project journey form view associated with
            the current project.

            This method retrieves the action and view details related
            to the project journey tree view, sets the default project ID
            in the context, and opens the project journey form view window.

            :return: A dictionary containing action details to open
            the project journey form view.
            :rtype: dict
        """
        action = self.env.ref('project_render_journey.project_journey_action')
        view_id = self.env.ref(
            'project_render_journey.project_journey_form_view').id
        context = self._context.copy()
        context.update({'default_project_id': self.id})
        project_journey = self.env['project.journey'].search(
            [('project_id', '=', self.id)], limit=1)
        action_dict = {
            'name': action.name,
            'view_type': 'form',
            'view_mode': action.view_mode,
            'views': [(view_id, 'form')],
            'res_model': action.res_model,
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': project_journey.id if project_journey else False,
            'target': 'current',
            'context': context,
        }
        return action_dict
