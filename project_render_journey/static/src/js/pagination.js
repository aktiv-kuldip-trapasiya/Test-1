odoo.define('project_render_journey.pagination', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.SignUpForm = publicWidget.Widget.extend({
        selector: '.project_render_test',
        events: {
            'click .project_details': '_projectDetails',
            'click .task_chat': '_taskDetails',
            'click .3DDrawings': '_3DrawingsDetails',
            'click .MaterialsSelection': '_MaterialDetails',
            'click .ElectricalPlan': '_ElectricalPlanDetails',
            'click .Appliances': '_AppliancesDetails',
            'click .Lights': '_LightsDetails',
            'click .Picturescompletionwork': '_CompletionWorkDetails',
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _projectDetails: function (ev) {
            $("#project_information_div").removeClass('d-none')
            $("#task_information").addClass('d-none')
            $("#3DDrawings").addClass('d-none')
            $("#MaterialsSelection").addClass('d-none')
            $("#ElectricalPlan").addClass('d-none')
            $("#Appliances").addClass('d-none')
            $("#Lights").addClass('d-none')
        },
        _taskDetails: function (ev) {
            $("#project_information_div").addClass('d-none')
            $("#task_information").removeClass('d-none')
            $("#3DDrawings").addClass('d-none')
            $("#MaterialsSelection").addClass('d-none')
            $("#ElectricalPlan").addClass('d-none')
            $("#Appliances").addClass('d-none')
            $("#Lights").addClass('d-none')
        },
        _3DrawingsDetails: function (ev) {
            $("#project_information_div").addClass('d-none')
            $("#task_information").addClass('d-none')
            $("#3DDrawings").removeClass('d-none')
            $("#MaterialsSelection").addClass('d-none')
            $("#ElectricalPlan").addClass('d-none')
            $("#Appliances").addClass('d-none')
            $("#Lights").addClass('d-none')
        },
        _MaterialDetails: function (ev) {
            $("#project_information_div").addClass('d-none')
            $("#task_information").addClass('d-none')
            $("#3DDrawings").addClass('d-none')
            $("#MaterialsSelection").removeClass('d-none')
            $("#ElectricalPlan").addClass('d-none')
            $("#Appliances").addClass('d-none')
            $("#Lights").addClass('d-none')
        },
        _ElectricalPlanDetails: function (ev) {
            $("#project_information_div").addClass('d-none')
            $("#task_information").addClass('d-none')
            $("#3DDrawings").addClass('d-none')
            $("#MaterialsSelection").addClass('d-none')
            $("#ElectricalPlan").removeClass('d-none')
            $("#Appliances").addClass('d-none')
            $("#Lights").addClass('d-none')
        },
        _AppliancesDetails: function (ev) {
            $("#project_information_div").addClass('d-none')
            $("#task_information").addClass('d-none')
            $("#3DDrawings").addClass('d-none')
            $("#MaterialsSelection").addClass('d-none')
            $("#ElectricalPlan").addClass('d-none')
            $("#Appliances").removeClass('d-none')
            $("#Lights").addClass('d-none')
        },
        _LightsDetails: function (ev) {
            $("#project_information_div").addClass('d-none')
            $("#task_information").addClass('d-none')
            $("#3DDrawings").addClass('d-none')
            $("#MaterialsSelection").addClass('d-none')
            $("#ElectricalPlan").addClass('d-none')
            $("#Appliances").addClass('d-none')
            $("#Lights").removeClass('d-none')
        },
        _CompletionWorkDetails: function (ev) {
            $("#project_information_div").addClass('d-none')
            $("#task_information").addClass('d-none')
            $("#3DDrawings").addClass('d-none')
            $("#MaterialsSelection").addClass('d-none')
            $("#ElectricalPlan").addClass('d-none')
            $("#Appliances").addClass('d-none')
            $("#Lights").addClass('d-none')
            $("#Picturescompletionwork").removeClass('d-none')
        },
    });
});
