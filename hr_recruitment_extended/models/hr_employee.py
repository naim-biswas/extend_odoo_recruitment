from odoo import models, fields, api


class Employee(models.Model):
    _inherit = 'hr.employee'

    emergency_contact_lines = fields.One2many('hr.applicant.emergency.contact.line', 'employee_id', string='Emergency Contacts')
    education_lines = fields.One2many('hr.applicant.education.line', 'employee_id', string='Educational Information')
