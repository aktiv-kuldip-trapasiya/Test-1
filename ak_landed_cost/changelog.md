# Product Snoozing for Replenishment

### Technical Name: ak_landed_cost

[14.0.4.0.0] - 2025-06-30 | User Story 2: Actual Purchase Cost on Sales Order Line (Including retroactive landed cost and backorders)

    Introduced actual_purchase_price field on sale.order.line.

    Automatically computes the actual cost of goods delivered per line item.

    Based on associated stock.valuation.layer records from deliveries.

    Retroactively includes any landed costs applied to the related stock moves, even if applied post-invoice.

    Handles cases of partial deliveries and backorders by computing cost for the delivered quantity only.

    Takes into account the lot number used in the delivery to trace the exact valuation layer.

    Ensures accurate COGS and margin reporting at the sale order line level.

    User Story 2 : Actual Purchase Cost on Sales Order Line ( Including retroactive landed cost and backorders)
    1. Business Requirements
    The current "Cost" field on the sale order line in Odoo doesn't accurately represent the true cost of goods sold (COGS) when dealing with backorders, partial deliveries, and landed costs applied after the sale. This leads to inaccurate margin analysis. The business needs a reliable way to track and report the actual purchase cost, including all associated expenses, at the sale order line level for improved financial reporting.
    
    Objective: To ensure that the cost of goods sold (COGS) reported at the sale order line level accurately reflects the actual purchase price, including all associated landed costs and adjustments related to backorders and partial deliveries, for reliable financial and margin analysis.
    Modules Impacted:
    Sales
    Inventory
    Purchase
    Accounting
    2. Functional Specifications
    
    Behavior:
    A new field, actual_purchase_price, should be added to the sale.order.line model.
        
    This field should automatically calculate and display the true cost of the goods delivered for that specific sale order line.
    The calculation of actual_purchase_price must be based on the stock valuation layers (FIFO method) associated with the delivery of the items on that sale order line.
    actual_purchase_price should retroactively include any landed costs applied to the related purchase(s), even if these costs are recorded after the sale order or invoice creation.
    For sale order lines fulfilled by backordered products (where the purchase occurs after the sale), the actual_purchase_price should reflect the eventual purchase price and any associated landed costs.
    The actual_purchase_price should consider the lot number of the product 
    
    3. Success Criteria
    A new field, actual_purchase_price, exists on the sale.order.line.
    The actual_purchase_price accurately reflects the COGS, including the purchase price and all landed costs, based on the stock valuation layers of the delivered goods.
    The actual_purchase_price is updated retroactively when landed costs are applied after the sale or delivery.
    For sale order lines fulfilled by backordered products, the actual_purchase_price accurately reflects the purchase cost and landed costs incurred.
    In scenarios with partial deliveries, the actual_purchase_price reflects the cost of the specific inventory delivered for each part.
    Actual purchase price should be computed on the sale order line, based on the stock.valuation.layer records for the related deliveries

