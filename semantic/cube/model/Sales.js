cube(`Sales`, {
  sql: `SELECT * FROM sales_gold`,
  title: `Sales`,
  description: `Completed-order sales at one row per order line.`,

  measures: {
    grossSales: {
      sql: `gross_sales_amount`,
      type: `sum`,
      description: `Gross sales for completed order lines before discounts.`
    },
    discountAmount: {
      sql: `discount_amount`,
      type: `sum`,
      description: `Discount amount for completed order lines.`
    },
    netSales: {
      sql: `net_sales_amount`,
      type: `sum`,
      description: `Gross sales less discounts for completed order lines.`
    },
    netSalesGrandTotal: {
      sql: `${netSales}`,
      type: `sum`,
      multiStage: true,
      grain: { keepOnly: [] },
      public: false,
      description: `Internal grand total for customer contribution share.`
    },
    customerContributionShare: {
      sql: `1.0 * ${netSales} / NULLIF(${netSalesGrandTotal}, 0)`,
      type: `number`,
      multiStage: true,
      format: `percent`,
      description: `Completed net sales for the selected customer divided by total completed net sales.`
    },
    unitsSold: {
      sql: `quantity`,
      type: `sum`,
      description: `Units on completed order lines.`
    },
    orderLineCount: {
      type: `count`,
      description: `Count of completed order lines.`
    },
    orderCount: {
      sql: `order_id`,
      type: `count_distinct`,
      description: `Distinct completed orders; not an order-line count.`
    }
  },

  dimensions: {
    orderLineId: {
      sql: `order_line_id`,
      type: `string`,
      primaryKey: true,
      public: false
    },
    orderId: {
      sql: `order_id`,
      type: `string`,
      description: `Completed order identifier.`
    },
    customerId: {
      sql: `customer_id`,
      type: `string`
    },
    productId: {
      sql: `product_id`,
      type: `string`
    },
    orderDate: {
      sql: `order_date`,
      type: `time`
    },
    channel: {
      sql: `channel`,
      type: `string`
    }
  },

  joins: {
    Customers: {
      relationship: `belongsTo`,
      sql: `${CUBE}.customer_id = ${Customers}.customer_id`
    },
    Products: {
      relationship: `belongsTo`,
      sql: `${CUBE}.product_id = ${Products}.product_id`
    }
  }
});
