/*
Calculate the rate that new loans are funded
*/
SELECT	subL.year,
		subL.month,
		subB.new_borrowers,
		subBL.max_loan,
		subL.num_loans_started,
		subBL.num_new_loans_started,
		ROUND(subBL.num_new_loans_started / subL.num_loans_started * 100) AS percent_new_loans,
		ROUND(subBL.num_new_loans_filled / subBL.num_new_loans_started * 100) AS new_loan_percent_filled,
		ROUND(subBL.newB_usd_requested / subL.total_usd_requested * 100) AS new_loan_percent_of_requested,
		ROUND(subL.num_loans_filled / subL.num_loans_started * 100) AS percent_filled,
		subL.total_usd_requested,
		ROUND(subL.total_usd_inflow / subL.total_usd_requested * 100) AS percent_of_requested
	FROM (	-- New loan data
		SELECT	EXTRACT(YEAR FROM created_at) AS year,		-- year
				EXTRACT(MONTH FROM created_at) AS month,	-- month
				COUNT(id) AS num_loans_started,				-- count of new loans per month
				COUNT(
					CASE WHEN raised_percentage = 100 THEN 1
					ELSE NULL
					END
					) AS num_loans_filled,
				ROUND(SUM( raised_percentage/100 * usd_amount )) AS total_usd_inflow,
				ROUND(SUM( usd_amount )) AS total_usd_requested
				FROM loans
				GROUP BY year, month
	) AS subL
	JOIN (	-- New borrower data
		SELECT	EXTRACT(YEAR FROM created_at) AS year,		-- year
				EXTRACT(MONTH FROM created_at) AS month,	-- month
				COUNT(id) AS new_borrowers					-- count of new borrowers per month
				FROM borrowers
				WHERE activation_status != 4	-- status of 4 means rejected
				GROUP BY year, month
	) AS subB
	ON subL.year = subB.year AND subL.month = subB.month
	JOIN (	-- First loan size data
		SELECT	EXTRACT(YEAR FROM l.first_loan_date) AS year,	-- year
				EXTRACT(MONTH FROM l.first_loan_date) AS month,	-- month
				COUNT(l.borrower_id) AS num_new_loans_started,		-- count of new loans per month
				COUNT(
					CASE WHEN l.raised_percentage = 100 THEN 1
					ELSE NULL
					END
					) AS num_new_loans_filled,
				ROUND(SUM( l.raised_percentage/100 * l.usd_amount )) AS newB_usd_inflow,
				ROUND(SUM( l.usd_amount )) AS newB_usd_requested,
				MAX(l.usd_amount) AS max_loan
				FROM ( -- Date of first loan for each borrower
					SELECT 	l1.borrower_id,
							l1.first_loan_date,
							l2.raised_percentage,
							l2.usd_amount
							FROM ( -- Create id and first loan date keys
								SELECT	borrower_id,
										MIN(created_at) AS first_loan_date
										FROM loans
										GROUP BY borrower_id
										ORDER BY first_loan_date
							) AS l1
							JOIN loans AS l2
							ON l1.borrower_id = l2.borrower_id AND l1.first_loan_date = l2.created_at
				) AS l
				GROUP BY year, month
	) AS subBL
	ON subL.year = subBL.year AND subL.month = subBL.month
		
		