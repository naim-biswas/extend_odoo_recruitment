from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class EmergencyContactLine(models.Model):
    _name = 'hr.applicant.emergency.contact.line'
    _description = 'Emergency Contacts of Job Applicant'

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    name = fields.Char('Name')
    address = fields.Char('Address')
    phone = fields.Char('Phone')


class EducationLine(models.Model):
    _name = 'hr.applicant.education.line'
    _description = 'Educational Information of Job Applicant'

    applicant_id = fields.Many2one('hr.applicant', string='Applicant')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    institute = fields.Char('Institute')
    degree_id = fields.Many2one('hr.recruitment.degree', string='Degree')
    passing_year = fields.Integer('Passing Year')


class HRApplicant(models.Model):
    _inherit = 'hr.applicant'

    manager_id = fields.Many2one('hr.employee', 'Manager')
    emergency_contact_lines = fields.One2many('hr.applicant.emergency.contact.line', 'applicant_id', string='Emergency Contacts')
    education_lines = fields.One2many('hr.applicant.education.line', 'applicant_id', string='Educational Information')

    def create_employee_from_applicant(self):
        """ Create an hr.employee from the hr.applicants """
        employee = False
        for applicant in self:
            contact_name = False
            if applicant.partner_id:
                address_id = applicant.partner_id.address_get(['contact'])['contact']
                contact_name = applicant.partner_id.display_name
            else:
                if not applicant.partner_name:
                    raise UserError(_('You must define a Contact Name for this applicant.'))
                new_partner_id = self.env['res.partner'].create({
                    'is_company': False,
                    'type': 'private',
                    'name': applicant.partner_name,
                    'email': applicant.email_from,
                    'phone': applicant.partner_phone,
                    'mobile': applicant.partner_mobile
                })
                address_id = new_partner_id.address_get(['contact'])['contact']
            if applicant.partner_name or contact_name:
                employee = self.env['hr.employee'].create({
                    'name': applicant.partner_name or contact_name,
                    'job_id': applicant.job_id.id or False,
                    'job_title': applicant.job_id.name,
                    'address_home_id': address_id,
                    'department_id': applicant.department_id.id or False,
                    'address_id': applicant.company_id and applicant.company_id.partner_id
                            and applicant.company_id.partner_id.id or False,
                    'work_email': applicant.department_id and applicant.department_id.company_id
                            and applicant.department_id.company_id.email or False,
                    'work_phone': applicant.department_id and applicant.department_id.company_id
                            and applicant.department_id.company_id.phone or False,
                    'parent_id': applicant.manager_id.id or False,
                    'emergency_contact_lines': [(4, line.id) for line in self.emergency_contact_lines],
                    'education_lines': [(4, line.id) for line in self.education_lines]
                })

                applicant.write({'emp_id': employee.id})
                if applicant.job_id:
                    applicant.job_id.write({'no_of_hired_employee': applicant.job_id.no_of_hired_employee + 1})
                    applicant.job_id.message_post(
                        body=_('New Employee %s Hired') % applicant.partner_name if applicant.partner_name else applicant.name,
                        subtype="hr_recruitment.mt_job_applicant_hired")
                applicant.message_post_with_view(
                    'hr_recruitment.applicant_hired_template',
                    values={'applicant': applicant},
                    subtype_id=self.env.ref("hr_recruitment.mt_applicant_hired").id)

        employee_action = self.env.ref('hr.open_view_employee_list')
        dict_act_window = employee_action.read([])[0]
        dict_act_window['context'] = {'form_view_initial_mode': 'edit'}
        dict_act_window['res_id'] = employee.id
        return dict_act_window



