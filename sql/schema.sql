CREATE DATABASE supply_chain_analysis;
USE supply_chain_analysis;
CREATE TABLE supply_chain (
    Product_ID INT,
    Warehouse VARCHAR(10),
    Order_Date DATE,
    Shipment_Date DATE,
    Lead_Time INT,
    Demand_Forecast INT,
    Inventory_Level INT,
    Stockout_Flag INT,
    Backorder_Flag INT,
    Supplier_ID INT,
    Order_Quantity INT,
    Shipment_Quantity INT,
    Product_Category VARCHAR(50),
    Product_Price DECIMAL(10,2),
    Customer_ID INT,
    Order_Priority VARCHAR(20),
    Revenue DECIMAL(12,2),
    Inventory_Coverage DECIMAL(12,2),
    Demand_Gap INT
);
SELECT *FROM supply_chain;
SELECT COUNT(*)FROM supply_chain;