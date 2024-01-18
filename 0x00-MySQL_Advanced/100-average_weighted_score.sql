-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;

    -- Calculate total weighted score and total weight for the user
    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO total_weighted_score, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = p_user_id;

    -- Update the average_score for the user
    IF total_weight > 0 THEN
        UPDATE users
        SET average_score = total_weighted_score / total_weight
        WHERE id = p_user_id;
    ELSE
        -- If total_weight is 0, set average_score to 0 to avoid division by zero
        UPDATE users
        SET average_score = 0
        WHERE id = p_user_id;
    END IF;
END //

DELIMITER ;
