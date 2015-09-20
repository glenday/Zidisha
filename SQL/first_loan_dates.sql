/*
SELECT COUNT(*)
	FROM(
SELECT	borrower_id,
		MIN(created_at) AS first_loan_date
		FROM loans
		GROUP BY borrower_id
		ORDER BY first_loan_date
		) AS d
*/
SELECT 	l1.borrower_id,
		l1.first_loan_date,
		l2.raised_percentage,
		l2.usd_amount
		FROM ( 
			SELECT	borrower_id,
					MIN(created_at) AS first_loan_date
					FROM loans
					GROUP BY borrower_id
					ORDER BY first_loan_date
		) AS l1
		JOIN loans AS l2
		ON l1.borrower_id = l2.borrower_id AND l1.first_loan_date = l2.created_at
		LIMIT 20
