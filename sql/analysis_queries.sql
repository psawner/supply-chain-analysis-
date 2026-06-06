USE supply_chain_analysis;

------------------------------------------------ Total Revenue
-- How much revenue it generates?
SELECT SUM(Revenue) AS Total_Revenue FROM supply_chain;

-- Warehouse Performance
SELECT
Warehouse,
COUNT(*) AS Orders,
ROUND(AVG(Lead_Time),2) AS Avg_Lead_Time,
ROUND(AVG(Stockout_Flag)*100,2) AS Stockout_Rate,
ROUND(AVG(Backorder_Flag)*100,2) AS Backorder_Rate,
ROUND(SUM(Revenue),2) AS Revenue
FROM supply_chain
GROUP BY Warehouse;

-- Category Revenue
SELECT
Product_Category,
ROUND(SUM(Revenue),2) AS Revenue
FROM supply_chain
GROUP BY Product_Category
ORDER BY Revenue DESC;

-- Top Suppliers by Lead Time
SELECT
Supplier_ID,
ROUND(AVG(Lead_Time),2) AS Avg_Lead_Time
FROM supply_chain
GROUP BY Supplier_ID
ORDER BY Avg_Lead_Time DESC
LIMIT 10;

-- Inventory Coverage
SELECT Product_Category, 
ROUND(AVG(Inventory_Coverage),2) AS Coverage 
FROM supply_chain GROUP BY Product_Category;

-- Which warehouse contributes most to company revenue?
SELECT
Warehouse,
ROUND(SUM(Revenue),2) AS Revenue
FROM supply_chain
GROUP BY Warehouse
ORDER BY Revenue DESC;

-- Which Warehouse Has Highest Inventory?
SELECT
Warehouse,
ROUND(AVG(Inventory_Level),2) AS Avg_Inventory
FROM supply_chain
GROUP BY Warehouse
ORDER BY Avg_Inventory DESC;


-- Which Warehouse Faces Most Stockouts?
SELECT
Warehouse,
ROUND(AVG(Stockout_Flag)*100,2) AS Stockout_Rate
FROM supply_chain
GROUP BY Warehouse
ORDER BY Stockout_Rate DESC;


-- Which Product Category Has Highest Demand?
SELECT
Product_Category,
SUM(Demand_Forecast) AS Total_Demand
FROM supply_chain
GROUP BY Product_Category
ORDER BY Total_Demand DESC;


-- Which Product Category Has Highest Revenue?
SELECT
Product_Category,
ROUND(SUM(Revenue),2) AS Revenue
FROM supply_chain
GROUP BY Product_Category
ORDER BY Revenue DESC;

-- Which Category Has Highest Backorders?
SELECT
Product_Category,
ROUND(AVG(Backorder_Flag)*100,2) AS Backorder_Rate
FROM supply_chain
GROUP BY Product_Category
ORDER BY Backorder_Rate DESC;

-- Which Category Has Highest Stockouts?
SELECT
Product_Category,
ROUND(AVG(Stockout_Flag)*100,2) AS Stockout_Rate
FROM supply_chain
GROUP BY Product_Category
ORDER BY Stockout_Rate DESC;

-- Demand vs Shipment by Category
SELECT
Product_Category,
SUM(Demand_Forecast) AS Total_Demand,
SUM(Shipment_Quantity) AS Total_Shipped
FROM supply_chain
GROUP BY Product_Category;

-- Categories With Largest Demand Gap
SELECT
Product_Category,
ROUND(AVG(Demand_Gap),2) AS Avg_Demand_Gap
FROM supply_chain
GROUP BY Product_Category
ORDER BY Avg_Demand_Gap DESC;

-- Revenue by Order Priority
SELECT
Order_Priority,
ROUND(SUM(Revenue),2) AS Revenue
FROM supply_chain
GROUP BY Order_Priority
ORDER BY Revenue DESC;

-- Lead Time by Order Priority
SELECT
Order_Priority,
ROUND(AVG(Lead_Time),2) AS Avg_Lead_Time
FROM supply_chain
GROUP BY Order_Priority;

-- Rank Warehouses by Revenue
SELECT
Warehouse,
ROUND(SUM(Revenue),2) AS Revenue,
RANK() OVER(ORDER BY SUM(Revenue) DESC) AS Revenue_Rank
FROM supply_chain
GROUP BY Warehouse;