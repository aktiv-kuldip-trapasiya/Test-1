from odoo import fields, models, api


class ProjectJourneyImage(models.Model):
    _name = 'project.journey.image'
    _description = "Product Journey Image"
    _inherit = ['image.mixin']

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10, index=True)
    image_1920 = fields.Image(required=True)
    project_render_id = fields.Many2one("project.renders", string="Project Attachments")


class ProjectJourneyDefectList(models.Model):
    _name = 'project.journey.defect.list'
    _description = "Product Journey Defect List"
    _inherit = ['image.mixin']

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10, index=True)
    image_1920 = fields.Image(required=True)
    project_render_id = fields.Many2one("project.renders", string="Project Attachments")


class ProjectJourneyDefectAcknowledge(models.Model):
    _name = 'project.journey.defect.acknowledge'
    _description = "Product Journey Defect Acknowledge"
    _inherit = ['image.mixin']

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10, index=True)
    image_1920 = fields.Image(required=True)
    project_render_id = fields.Many2one("project.renders", string="Project Attachments")


class ProjectJourneyCalendarActivity(models.Model):
    _name = 'project.journey.calendar.activity'
    _description = "Product Journey Calendar Activity"
    _inherit = ['image.mixin']

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10, index=True)
    image_1920 = fields.Image(required=True)
    project_render_id = fields.Many2one("project.renders", string="Project Attachments")


class ProjectJourney(models.Model):
    _name = 'project.journey'
    _description = 'Project Renders'
    _rec_name = 'project_id'

    project_id = fields.Many2one("project.project", string="Project")
    name = fields.Char(string="Name", related='project_id.name')
    project_journey_images =\
        fields.Many2many("project.journey.image",
                         "project_journey_project_journey_image_rel",
                         string="Pictures completion work")

    project_journey_defect_list =\
        fields.Many2many("project.journey.defect.list",
                         "project_journey_project_journey_defect_list_rel",
                         string="Completion with follow up defects list")

    project_journey_defect_acknowledge =\
        fields.Many2many("project.journey.defect.acknowledge",
                         "project_journey_defect_acknowledge_rel",
                         string="Acknowledge defects")

    project_journey_calendar_activity =\
        fields.Many2many("project.journey.calendar.activity",
                         "project_journey_calendar_activity_rel",
                         string="Calendar Activities")
