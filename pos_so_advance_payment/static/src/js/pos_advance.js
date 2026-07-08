odoo.define('pos_so_advance_payment.pos_so_advance_payment', function (require) {
"use strict";

	var module = require('point_of_sale.models');
    var core = require('web.core');
    var rpc = require('web.rpc');
	var screens = require('point_of_sale.screens');
    var PosPopWidget = require('point_of_sale.popups');
    var gui = require('point_of_sale.gui');
    var session = require('web.session');
    var QWeb = core.qweb;
    var _t = core._t;

    var _super_order = module.Order.prototype;
    module.Order = module.Order.extend({
        initialize: function() {
            _super_order.initialize.apply(this,arguments);
            this.so_notes = "";
            this.order_ref = "";
            this.partner_shiping_id = "";
            this.save_to_db();
        },
        export_as_JSON: function() {
            var json = _super_order.export_as_JSON.apply(this,arguments);
            json.so_notes = this.so_notes;
            json.partner_shiping_id = this.partner_shiping_id;
            return json;
        },
        export_for_printing:function() {
            var json = _super_order.export_for_printing.apply(this,arguments);
            json.so_notes = this.so_notes;
            json.order_ref = this.order_ref;
            json.partner_shiping_id = this.partner_shiping_id;
            return json
        },
        init_from_JSON: function(json) {
            _super_order.init_from_JSON.apply(this,arguments);
            this.so_notes = json.so_notes;
            this.order_ref = json.order_ref;
            this.partner_shiping_id = json.partner_shiping_id;
        },
    });

    var SaleOrderBillScreenWidget = screens.ReceiptScreenWidget.extend({
	    template: 'SaleOrderBillScreenWidget',
		    click_next: function(){
		    	var order = self.pos.get_order();
		    	order.finalize();
		        this.gui.show_screen('products');
		    },
		    click_back: function(){
		        this.gui.show_screen('products');
		    },
		    render_receipt: function(){
		        this._super();
		        this.$('.receipt-paymentlines').remove();
		        this.$('.receipt-change').remove();
		    },
		    print_web: function(){
		        window.print();
		    },
	});
	gui.define_screen({name:'saleOrderbill', widget: SaleOrderBillScreenWidget});


    var CreateSaleOrderPopupWidget = PosPopWidget.extend({
        template: 'CreateSaleOrderPopupWidget',
        events: _.extend({}, PosPopWidget.prototype.events,{
            'change #ptr_contacts': 'onchange_ptr_contacts',
            'change input[type=radio][name=radio_address]': 'onchange_address_radio'
        }),
        enable_disable_inputs: function(status){
            var self = this;
            self.$el.find('.street1').prop('disabled', status);
            self.$el.find('.street2').prop('disabled', status);
            self.$el.find('.add_city').prop('disabled', status);
            self.$el.find('.add_phone').prop('disabled', status);
            self.$el.find('.add_mobile').prop('disabled', status);
        },
        onchange_ptr_contacts: function(){
            var self = this;
            var contact_id = parseInt(this.$el.find('#ptr_contacts').val());
            this._rpc({
                model: 'res.partner',
                method: 'search_read',
                args: [[['id', '=', contact_id]],['id', 'name', 'street','street2', 'phone' ,'city', 'mobile']],
            }).then(function(partner_data){
                if (contact_id){
                    self.enable_disable_inputs(false);
                }
                self.$el.find('.street1').val(partner_data[0]['street'] ? partner_data[0]['street']: "");
                self.$el.find('.street2').val(partner_data[0]['street2'] ? partner_data[0]['street2']: "");
                self.$el.find('.add_city').val(partner_data[0]['city'] ? partner_data[0]['city']: "");
                self.$el.find('.add_phone').val(partner_data[0]['phone'] ? partner_data[0]['phone']: "");
                self.$el.find('.add_mobile').val(partner_data[0]['mobile'] ? partner_data[0]['mobile']: "");
            })
        },
        onchange_address_radio: function(){
            var radio_add_val = $("input[name='radio_address']:checked").val();
            var contact_id = parseInt(this.$el.find('#ptr_contacts').val());
            $("#error_msg").css("display", "none");
            $(".error_msg_delivery").css("display", "none");
            $(".error_msg_create").css("display", "none");
            if(radio_add_val == 'create_new_delivery'){
                $("#delivery_selection_row").css({'display':"none"});
                this.enable_disable_inputs(false);
                $("#new_contact_name").css({'display':"table-row"});
            }
            if(radio_add_val == 'use_ex_delivery'){
                $("#delivery_selection_row").css({'display':"table-row"});
                if (!contact_id){
                    this.enable_disable_inputs(true);
                }
                $("#new_contact_name").css({'display':"none"});
            }
        },
	    print_xml: function(){
	        var order = this.pos.get('selectedOrder');
	        if(order.get_orderlines().length > 0){
	            var receipt = order.export_for_printing();
	            receipt.bill = true;
	            this.pos.proxy.print_receipt(QWeb.render('SaleOrderBillReceipt',{
	                receipt: receipt, widget: this, pos: this.pos, order: order,
	            }));
	        }
	    },
        get_partners_contacts: function(){
            var self = this;
            var order = self.pos.get('selectedOrder');
            if(order.get_client() != null){
                var partner_id = order.get_client().id;                
                this._rpc({
                    model: 'res.partner',
                    method: 'search_read',
                    args: [[['parent_id', '=', partner_id],['type', '=', 'delivery']],['id', 'name', 'street', 'street2']],
                }).then(function(partner_data){
                    var delivery_contacts = $(QWeb.render('partner_delivery_address',{
                        contacts: partner_data,
                        adv_pay: self.pos.config.allow_advance_payment,
                        journal: self,
                        currency_symbol: self.pos.currency.symbol
                    }));
                    self.$('#sale_order_details').append(delivery_contacts);
                    if (partner_data.length > 0){
                        self.$('#use_ex_radio').prop("checked", true);
                        $("#delivery_selection_row").css({'display':"table-row"});
                        $("#new_contact_name").css({'display':"none"});
                        self.enable_disable_inputs(true);
                    }
                }).fail(function(error, event) {
                 if (parseInt(error.code, 10) === 200) {
                    // Business Logic Error, not a connection problem
                    self.gui.show_popup(
                        'error-traceback', {
                            'title': error.data.message,
                            'body': error.data.debug,
                        }
                    );
                } else {
                    self.gui.show_popup('error', {
                        'title': _t('Connection error'),
                        'body': _t(
                            'Can not execute this action because the POS' +
                            ' is currently offline'),
                    })
                }
            });
            }
        },
        renderElement: function(){
            this._super(); 
            var self= this;
            $(".print_quotation_bill").click(function(){
                var order = self.pos.get('selectedOrder');
                if(order.get_client() != null){
	                order.so_notes = $(".so_notes").val();
                    order.partner_shiping_id = parseInt($("#ptr_contacts").val());
	                if (!self.pos.config.iface_print_via_proxy) {
	                	self.save_and_print();
	                } else {
	                    self.save_order();
	                    self.print_xml();
	                }
	            }
	            else{
	            	alert("Customer is required for sale order. Please select customer first !!!!");
	            }
            });
            $(".save_quotation_bill").click(function(){
            	var order = self.pos.get('selectedOrder');
            	if(order.get_client() != null){
	            	order.so_notes = $(".so_notes").val();
                    var radio_add_val = $("input[name='radio_address']:checked").val();
                    if(radio_add_val == 'use_ex_delivery'){
                        order.partner_shiping_id = parseInt($("#ptr_contacts").val());
                    }
                    self.save_order();
	            }
	            else{
	            	alert("Customer is required for sale order. Please select customer first !!!!");
	            }
            });
        },
        prepare_sale_order_data: function(){
            var self = this;
            var order = self.pos.get('selectedOrder');
            var radio_add_val = $("input[name='radio_address']:checked").val();
            if(radio_add_val == 'use_ex_delivery' && ! order.partner_shiping_id){
                $("#error_msg").css("display", "table-row");
                $(".error_msg_delivery").css({"display":"block", "text-align": "center", "color": "red"});
                return false;
            }
            else if(radio_add_val == 'create_new_delivery' && !$(".c_name").val()){
                $("#error_msg").css("display", "table-row");
                $(".error_msg_create").css({"display":"block", "text-align": "center", "color": "red"});
                return false;
            }
            else if(self.pos.config.allow_advance_payment){
                if(parseFloat($(".adv_pay_value").val()) > order.get_subtotal()){
                    alert("Advance payment can't be greater than total payable amount.")
                    return false;
                }
                else
                {
                    self.order = self.pos.get_order();
                    var data = order.export_as_JSON();
                    var new_update_delivery_addr = {
                        'c_name': $(".c_name").val(),
                        'street': $(".street1").val(),
                        'street2': $(".street2").val(),
                        'city': $(".add_city").val(),
                        'phone': $(".add_phone").val(),
                        'mobile': $(".add_mobile").val(),
                        'parent_id': order.attributes.client.id,
                        'advance_pay': $(".adv_pay_value").val(),
                        'payment_journal':parseInt($("#payment_journal").val()),
                        'type': 'delivery'
                    }

                }    
            }
            else
            {
                self.order = self.pos.get_order();
                var data = order.export_as_JSON();
                var new_update_delivery_addr = {
                    'c_name': $(".c_name").val(),
                    'street': $(".street1").val(),
                    'street2': $(".street2").val(),
                    'city': $(".add_city").val(),
                    'phone': $(".add_phone").val(),
                    'mobile': $(".add_mobile").val(),
                    'parent_id': order.attributes.client.id,
                    'advance_pay': $(".adv_pay_value").val(),
                    'type': 'delivery'
                }

            }
            $.extend(data, new_update_delivery_addr);
            return data;
        },
        save_order:function(){
        	var self = this;
            var data = self.prepare_sale_order_data();
            if (data){
                rpc.query({
                    model: 'sale.order',
                    method: 'create_new_quotation',
                    args: [data],
                }).then(function(quotation_data){
		            self.order.finalize();
		            self.gui.show_popup('create-CompleteSaleOrder-popup',{'order_ref':quotation_data['result']});
		        },function(err,event){
		            event.preventDefault();
		            self.gui.show_popup('error',{
		                'title': _t('Error: Could not Save Changes'),
		                'body': _t('Your Internet connection is probably down.'),
		            });
		        });
            }
        },
        save_and_print:function(){
        	self = this;
			var data = self.prepare_sale_order_data();
            if (data){
                rpc.query({
                    model: 'sale.order',
                    method: 'create_new_quotation',
                    args: [data],
                }).then(function(quotation_data){
	        		self.order.order_ref = quotation_data['result'];
	                self.gui.show_screen('saleOrderbill');
		        },function(err,event){
		            event.preventDefault();
		            self.gui.show_popup('error',{
		                'title': _t('Error: Could not Save Changes'),
		                'body': _t('Your Internet connection is probably down.'),
		            });
		        });
            }
        },
        show: function(options){
            this.options = options || {};
            var self = this;
            this._super(options);
            this.get_partners_contacts();
        },
    });

    gui.define_popup({
        'name': 'create-saleorder-popup', 
        'widget': CreateSaleOrderPopupWidget,
    });

	var CreateCompleteSaleOrderPopupWidget = PosPopWidget.extend({
    	template: 'CreateCompleteSaleOrderPopupWidget',
        show: function(options){
            this.options = options || {};
            var self = this;
            this._super(options); 
            this.renderElement();
        },
    });

    gui.define_popup({
        'name': 'create-CompleteSaleOrder-popup', 
        'widget': CreateCompleteSaleOrderPopupWidget,
    });

    var CreateSaleOrderButton = screens.ActionButtonWidget.extend({
        template: 'CreateSaleOrderButton',
        button_click: function(){
        	if(this.pos.get_order().get_orderlines().length === 0){
        		alert("Please add some products to proceed.");
        	}
        	else{
                if(this.pos.get_order().attributes.client){

    			     this.gui.show_popup('create-saleorder-popup');
                }
                else{
                    alert("Please select the customer to proceed.");
                }
        	}
        },
    });

    screens.define_action_button(
    {
        'name': 'Create Sale Order',
        'widget': CreateSaleOrderButton,
        'condition': function(){
            return this.pos.config.allow_create_sale_order;
        }
    });
});
