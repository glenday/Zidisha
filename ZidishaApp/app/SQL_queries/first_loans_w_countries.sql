SELECT  l1.first_loan_date,
        b.created_at,
        l2.usd_amount,
        c.name AS country_name
        FROM (
            SELECT  borrower_id,
                    MIN(created_at) AS first_loan_date
                    FROM loans
                    GROUP BY borrower_id
                    ORDER BY first_loan_date
        ) AS l1
        JOIN loans AS l2
        ON l1.borrower_id = l2.borrower_id AND l1.first_loan_date = l2.created_at
        JOIN borrowers AS b
        ON b.id = l1.borrower_id
        JOIN countries AS c
        ON c.id = b.country_id