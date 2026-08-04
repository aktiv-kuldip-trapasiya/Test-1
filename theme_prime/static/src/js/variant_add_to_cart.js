//import { rpc } from "@web/core/network/rpc";
//
//$(document).on('click', '#oos-alert-ok', function () {
//    $('#oos-alert-popup').fadeOut(200);
//});
//
//function showOutOfStockPopup(message) {
//    $('#oos-alert-message').text(message);
//    $('#oos-alert-popup').fadeIn(200);
//}
//
//$(document).on('click', '.add-variant-to-cart', async function (ev) {
//    ev.preventDefault();
//    ev.stopPropagation();
//
//    const $btn = $(this);
//    const productId = parseInt($btn.data('product-id'));
//
//    if (!productId) return;
//
//    // quantity
//    let quantity = 1;
//    const $qtyInput = $btn.siblings('.variant-qty');
//    if ($qtyInput.length) {
//        quantity = parseInt($qtyInput.val(), 10) || 1;
//    }
//
//    $btn.prop('disabled', true);
//
//    // Step 1 — Get allow_oos
//    let allowOOS = false;
//    try {
//        allowOOS = await rpc("/shop/get_allow_oos", { product_id: productId });
//    } catch (err) {
//        console.error("Failed to fetch allow_out_of_stock_order status", err);
//    }
//
//    // Step 2 — Add to cart
//    rpc("/shop/cart/update_json", {
//        product_id: productId,
//        add_qty: quantity,
//    })
//        .then(result => {
//
//            const errorMessage =
//                result.notification_info?.warning ||
//                result.warning ||
//                "";
//
//            const stockError =
//                result.error === true ||
//                (
//                    errorMessage &&
//                    (errorMessage.includes("stuks op voorraad") ||
//                        errorMessage.includes("units are available"))
//                );
//
//            // Step 3 — If OOS allowed → ignore stock errors
//            if (allowOOS === true) {
//                console.log("OOS allowed → ignoring stock errors.");
//            }
//            else if (stockError) {
//                // Step 4 — Show popup when OOS not allowed
//                showOutOfStockPopup(errorMessage);
//                $btn.prop('disabled', false);
//                return;
//            }
//
//            // Step 5 — Update cart counter (if exists)
//            const $cartCounter = $('.o_cart_counter');
//            if ($cartCounter.length) {
//                $cartCounter.text(result.cart_quantity || 0);
//                console.log('[AddVariantToCart] Cart counter updated:', result.cart_quantity);
//            }
//
//            // Step 6 — Trigger event once
//            $(document).trigger('added_to_cart', {
//                product_id: productId,
//                quantity: quantity
//            });
//
//            // Step 7 — Show banner if function exists
//            if (typeof showSuccessBanner === "function") {
//                showSuccessBanner(
//                    `Added ${quantity} item${quantity > 1 ? 's' : ''} to cart!`
//                );
//            }
//
//            // Step 8 — Reload (only if theme requires it)
//            window.location.reload();
//
//            // Step 9 — Re-enable button
//            $btn.prop('disabled', false);
//
//        })
//        .catch(error => {
//            console.error(error);
//            showOutOfStockPopup("An error occurred while adding to cart.");
//            $btn.prop('disabled', false);
//        });
//});


//import { rpc } from "@web/core/network/rpc";
//$(document).on('click', '#oos-alert-ok', function() {
//    $('#oos-alert-popup').fadeOut(200);
//});
//function showOutOfStockPopup(message) {
//    $('#oos-alert-message').text(message);
//    $('#oos-alert-popup').fadeIn(200);
//}
//
//$(document).on('click', '.add-variant-to-cart', async function(ev) {
//    ev.preventDefault();
//    ev.stopPropagation();
//
//    const $btn = $(this);
//    const productId = parseInt($btn.data('product-id'));
//
//    if (!productId) return;
//
//    // Read quantity
//    let quantity = 1;
//    const $qtyInput = $btn.siblings('.variant-qty');
//    if ($qtyInput.length) {
//        quantity = parseInt($qtyInput.val(), 10) || 1;
//    }
//
//    $btn.prop('disabled', true);
//
//    // ⭐ STEP 1 — Check if product allows out-of-stock order
//    let allowOOS = false;
//    try {
//        allowOOS = await rpc("/shop/get_allow_oos", { product_id: productId });
//    } catch (err) {
//        console.error("Failed to fetch allow_out_of_stock_order status", err);
//    }
//
//    // ⭐ STEP 2 — Try Add To Cart
//    rpc("/shop/cart/update_json", {
//        product_id: productId,
//        add_qty: quantity,
//    }).then(result => {
//
//        const errorMessage = result.notification_info?.warning || result.warning || "";
//        const stockError = result.error === true ||
//            (errorMessage &&
//             (errorMessage.includes("stuks op voorraad") ||
//              errorMessage.includes("units are available")));
//
//        // ⭐ STEP 3 — If OOS is allowed → IGNORE stock errors
//        if (allowOOS === true) {
//            console.log("OOS allowed → ignoring errors, forcing add to cart.");
//        }
//        else if (stockError) {
//            // ⭐ STEP 4 — Stock error + OOS not allowed → Show popup
//            showOutOfStockPopup(errorMessage);
//            $btn.prop('disabled', false);
//            return;
//        }
//
// const $cartCounter = $('.o_cart_counter');
//        if ($cartCounter.length) {
//            $cartCounter.text(result.cart_quantity || 0);
//            console.log('[AddVariantToCart] Cart counter updated to', result.cart_quantity);
//        } else {
//            console.warn('[AddVariantToCart] Cart counter element not found on page.');
//        }
//
//        // Show success banner
//         $('.o_cart_counter').text(result.cart_quantity || 0);
//        $(document).trigger('added_to_cart', { product_id: productId, quantity: quantity });
//        console.log('[AddVariantToCart] Triggered added_to_cart event');
//
//        showSuccessBanner(`Added ${quantity} item${quantity > 1 ? 's' : ''} to cart!`);
//
//        $(document).trigger('added_to_cart', { product_id: productId, quantity: quantity });
//        console.log('[AddVariantToCart] Triggered added_to_cart event');
//
//        window.location.reload();
//
//        $btn.prop('disabled', false);
//        console.log('[AddVariantToCart] Button re-enabled');
//            }).catch(error => {
//        showOutOfStockPopup("An error occurred while adding to cart.");
//        $btn.prop('disabled', false);
//    });
////    }).catch(error => {
////        console.error('[AddVariantToCart] RPC error:', error);
////        const errorMessage = error.message || error.data?.message || 'An error occurred while adding to cart.';
////        showDangerBanner(errorMessage);
////        $btn.prop('disabled', false);
////        console.log('[AddVariantToCart] Button re-enabled after RPC failure');
////    });
////        // SUCCESS CASE
////        $('.o_cart_counter').text(result.cart_quantity || 0);
////        $(document).trigger('added_to_cart', { product_id: productId, quantity: quantity });
////        console.log('[AddVariantToCart] Triggered added_to_cart event');
////
////        $('#cart-success-banner')
////            .text(`Added ${quantity} item${quantity > 1 ? 's' : ''} to cart!`)
////            .fadeIn(300)
////            .delay(2000)
////            .fadeOut(300);
////
////        window.location.reload();
////        $btn.prop('disabled', false);
////
////    }).catch(error => {
////        showOutOfStockPopup("An error occurred while adding to cart.");
////        $btn.prop('disabled', false);
////    });
//});

import { rpc } from "@web/core/network/rpc";

function showSuccessBanner(message) {
    const $banner = $('#cart-success-banner');
    $banner.text(message).fadeIn(300);

    // Hide after 3 seconds
    setTimeout(() => {
        $banner.fadeOut(300);
    }, 3000);
}

function showDangerBanner(message) {
    let $banner = $('#cart-danger-banner');
    if (!$banner.length) {
        $banner = $('<div id="cart-danger-banner" class="alert alert-danger" style="display: none; position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px; max-width: 500px;"></div>');
        $('body').append($banner);
    }
    $banner.text(message).fadeIn(300);
    setTimeout(() => {
        $banner.fadeOut(300);
    }, 5000);
}
$(document).on('click', '#oos-alert-ok', function() {
    $('#oos-alert-popup').fadeOut(200);
});
function showOutOfStockPopup(message) {
    $('#oos-alert-message').text(message);
    $('#oos-alert-popup').fadeIn(200);
}
$(document).on('click', '.add-variant-to-cart', function(ev) {
    ev.preventDefault();
    ev.stopPropagation();

    console.log('[AddVariantToCart] Button clicked');

    const $btn = $(this);
    const productId = parseInt($btn.data('product-id'));
    if (!productId) {
        console.error('[AddVariantToCart] Product ID missing on add to cart button.');
        return;
    }
    console.log('[AddVariantToCart] Product ID:', productId);

    const $qtyInput = $btn.siblings('.variant-qty');
//    let allowOOS = true;
//    try {
//        allowOOS = await rpc("/shop/get_allow_oos", { product_id: productId });
//    } catch (err) {
//        console.error("Failed to fetch allow_out_of_stock_order status", err);
//    }
    let quantity = 1;
    if ($qtyInput.length) {
        quantity = parseInt($qtyInput.val(), 10);
        if (isNaN(quantity) || quantity < 1) {
            console.warn('[AddVariantToCart] Invalid quantity input. Defaulting to 1.');
            quantity = 1;
        }
    } else {
        console.warn('[AddVariantToCart] Quantity input not found. Defaulting to 1.');
    }
    console.log('[AddVariantToCart] Quantity to add:', quantity);

    $btn.prop('disabled', true);
    console.log('[AddVariantToCart] Button disabled to prevent duplicate clicks');

    rpc("/shop/cart/update_json", {
        product_id: productId,
        add_qty: quantity,
    }).then(result => {
        console.log('[AddVariantToCart] RPC successful:', result);

        // Check if there's an error (stock validation failed)
        const hasError = result.error === true ||
                        (result.notification_info && result.notification_info.warning &&
                         (result.notification_info.warning.includes('stuks op voorraad') ||
                          result.notification_info.warning.includes('units are available')));

        const errorMessage = result.notification_info?.warning || result.warning || '';

        if (hasError && errorMessage) {
            // Stock validation error - show danger banner and don't reload
            console.warn('[AddVariantToCart] Stock validation error:', errorMessage);
            showOutOfStockPopup(errorMessage);
                $btn.prop('disabled', false);
                return;
//            showDangerBanner(errorMessage);
//            $btn.prop('disabled', false);
//            return;
        }
        const $cartCounter = $('.o_cart_counter');
        if ($cartCounter.length) {
            $cartCounter.text(result.cart_quantity || 0);
            console.log('[AddVariantToCart] Cart counter updated to', result.cart_quantity);
        } else {
            console.warn('[AddVariantToCart] Cart counter element not found on page.');
        }

        // Show success banner
        showSuccessBanner(`Added ${quantity} item${quantity > 1 ? 's' : ''} to cart!`);

        $(document).trigger('added_to_cart', { product_id: productId, quantity: quantity });
        console.log('[AddVariantToCart] Triggered added_to_cart event');

        window.location.reload();

        $btn.prop('disabled', false);
        console.log('[AddVariantToCart] Button re-enabled');
    }).catch(error => {
        console.error('[AddVariantToCart] RPC error:', error);
        const errorMessage = error.message || error.data?.message || 'An error occurred while adding to cart.';
        showDangerBanner(errorMessage);
        $btn.prop('disabled', false);
        console.log('[AddVariantToCart] Button re-enabled after RPC failure');
    });
});