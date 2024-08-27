
-- INSERT NEW LINES
INSERT INTO [dbo].[NewTable] (
    [Column1],
    [Column2],
    [Column3],
    [Column4],
    [Column5],
    [Column6]
)
SELECT
    delta.[Column1],
    delta.[Column2],
    delta.[Column3],
    delta.[Column4],
    delta.[Column5],
    delta.[Column6]
FROM [BronzeDatabase].[dbo].[DeltaTable] AS delta
LEFT JOIN [dbo].[NewTable] AS new
    ON delta.[Column1] = new.[Column1]
WHERE new.[Column1] IS NULL;

-- UPDATE EXISTING LINES
UPDATE [dbo].[NewTable] 
SET
    [Column1] = delta.[Column1],
    [Column2] = delta.[Column2],
    [Column3] = delta.[Column3],
    [Column4] = delta.[Column4],
    [Column5] = delta.[Column5],
    [Column6] = delta.[Column6]
FROM [BronzeDatabase].[dbo].[DeltaTable] AS delta
INNER JOIN [dbo].[NewTable] AS new
    ON delta.[Column1] = new.[Column1]
    AND delta.[Column2] = new.[Column2];
