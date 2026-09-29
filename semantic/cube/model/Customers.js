cube(`Customers`, {
  sql: `SELECT * FROM customers_gold`,
  title: `Customers`,
  description: `One row per customer. Sales measures are sourced from the related completed-order Sales cube.`,

  measures: {
    customerCount: {
      type: `count`,
      description: `Count of customers.`
    }
  },

  dimensions: {
    customerId: {
      sql: `customer_id`,
      type: `string`,
      primaryKey: true
    },
    customerSegment: {
      sql: `customer_segment`,
      type: `string`
    },
    region: {
      sql: `region`,
      type: `string`
    },
    acquisitionChannel: {
      sql: `acquisition_channel`,
      type: `string`
    },
    acquisitionDate: {
      sql: `acquisition_date`,
      type: `time`
    },
    customerStatus: {
      sql: `customer_status`,
      type: `string`
    }
  }
});
