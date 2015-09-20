/*
Calculate the maximum number of invitees allowed using one month counts
*/
SELECT	year,
		month AS month,
		MAX(count_invites) AS max_invites,
		MAX(count_accepted) AS max_accepted,
		SUM(count_invites) AS total_invites,
		ROUND(SUM(count_accepted)/SUM(count_invites)*100) AS accept_rate
		FROM(
			SELECT	EXTRACT(YEAR FROM created_at) AS year,		-- year
					EXTRACT(MONTH FROM created_at) AS month,	-- month
					borrower_id,
					COUNT(borrower_id) AS count_invites,
					COUNT(invitee_id) AS count_accepted
					FROM borrower_invites
					GROUP BY year, month, borrower_id
		) sub
		GROUP BY year, month
