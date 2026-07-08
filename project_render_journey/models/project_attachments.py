from odoo import fields, models, api


class Project3dImage(models.Model):
    _name = 'project.image'
    _description = "Product Image"
    _inherit = ['image.mixin']

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10, index=True)
    image_1920 = fields.Image(required=True)
    project_render_id = fields.Many2one("project.renders", string="Project Attachments")


class ProjectMaterialsImage(models.Model):
    _name = 'project.materials.image'
    _description = "Product Materials Image"
    _inherit = ['image.mixin']

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10, index=True)
    image_1920 = fields.Image(required=True)
    project_render_id = fields.Many2one("project.renders", string="Project Attachments")


class ProjectElectricPlanImage(models.Model):
    _name = 'project.electric.plan.image'
    _description = "Product Materials Image"
    _inherit = ['image.mixin']

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10, index=True)
    image_1920 = fields.Image(required=True)
    project_render_id = fields.Many2one("project.renders", string="Project Attachments")


class ProjectAppliancesImage(models.Model):
    _name = 'project.appliances.image'
    _description = "Product Appliances Image"
    _inherit = ['image.mixin']

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10, index=True)
    image_1920 = fields.Image(required=True)
    project_render_id = fields.Many2one("project.renders", string="Project Attachments")


class ProjectLightsImage(models.Model):
    _name = 'project.lights.image'
    _description = "Product Lights Image"
    _inherit = ['image.mixin']

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10, index=True)
    image_1920 = fields.Image(required=True)
    project_render_id = fields.Many2one("project.renders", string="Project Attachments")


class ProjectRenders(models.Model):
    _name = 'project.renders'
    _description = 'Project Renders'
    _rec_name = 'project_id'

    project_id = fields.Many2one("project.project", string="Project")
    name = fields.Char(string="Name", related='project_id.name')
    three_d_drawings = fields.Many2many("project.image",
                                        "three_drawing_attachment_rel",
                                        string="3D Drawings")
    materials_ids = fields.Many2many("project.materials.image",
                                     "materials_ids_attachment_rel",
                                     string="Project Materials")
    electrical_plan_ids = fields.Many2many("project.electric.plan.image",
                                           "electrical_plan_project_attachment_rel",
                                           string="Electrical Plans")
    appliances_ids = fields.Many2many("project.appliances.image",
                                      "appliances_project_attachment_rel",
                                      string="Appliances")
    lights_ids = fields.Many2many("project.lights.image",
                                  "appliances_attachment_rel",
                                  string="Lights")
