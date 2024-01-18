-- SQL script that creates a trigger that decreases the quantity of an item after adding a new order.
DELIMITER //;
CREATE TRIGGER after_insert_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
  -- Decrease the quantity of the item in the items table
  UPDATE items
  SET quantity = quantity - NEW.number
  WHERE name=NEW.item_name;
END;//
DELIMITER ;//
