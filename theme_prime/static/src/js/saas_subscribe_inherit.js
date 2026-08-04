//Version 3


/* @odoo-module */

import "@website_mass_mailing/js/website_mass_mailing";
import publicWidget from "@web/legacy/js/public/public_widget";

// Now extend the existing widget
publicWidget.registry.subscribe.include({

    /**
     * Updates the visibility of the subscribe and subscribed buttons.
     * Override with conditional logic and null checks
     *
     * @param {boolean} isSubscriber
     */
    _updateSubscribeControlsStatus(isSubscriber) {
        const thanksWrapEl = this.el.querySelector('.js_subscribed_wrap');
        const subscribeWrapEl = this.el.querySelector('.js_subscribe_wrap');
        const subscribeBtnEl = this.el.querySelector('.js_subscribe_btn');
        const valueInputEl = this.el.querySelector('input.js_subscribe_value, input.js_subscribe_email');

        // Your custom condition - only execute for subscribers
        if (isSubscriber) {
            // Only manipulate elements if they exist
            if (subscribeBtnEl) {
                subscribeBtnEl.disabled = true;
            }
            if (subscribeWrapEl) {
                subscribeWrapEl.classList.add('d-none');
            }
            if (thanksWrapEl) {
                thanksWrapEl.classList.remove('d-none');
            }
            if (valueInputEl) {
                valueInputEl.disabled = true;
            }
        } else {
            // Handle non-subscriber case
            if (subscribeBtnEl) {
                subscribeBtnEl.disabled = false;
            }
            if (subscribeWrapEl) {
                subscribeWrapEl.classList.remove('d-none');
            }
            if (thanksWrapEl) {
                thanksWrapEl.classList.add('d-none');
            }
            if (valueInputEl) {
                valueInputEl.disabled = false;
            }

            // Turnstile logic for non-subscribers
            if (this._turnstile && window.top === window && subscribeBtnEl) {
                const el = this._turnstile.addTurnstile('website_mass_mailing_subscribe');
                if (el) {
                    this._turnstile.addSpinner(subscribeBtnEl);
                    el[0].classList.add('mt-3');
                    el.insertAfter(this.el);
                    this._turnstile.renderTurnstile(el);
                }
            }
        }
    },
});