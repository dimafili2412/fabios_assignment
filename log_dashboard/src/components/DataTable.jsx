import React from 'react';
import PropTypes from 'prop-types';
import { Box, Typography, useTheme, useMediaQuery } from '@mui/material';

const DataTable = ({ columns, data }) => {
    const theme = useTheme();
    const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));

    // Mobile layout stacked
    if (isSmallScreen) {
        return (
            <Box>
                {data.map((row, rowIndex) => (
                    <Box
                        key={rowIndex}
                        sx={{
                            mb: theme.spacing(2),
                            p: theme.spacing(2),
                            border: `1px solid ${theme.palette.divider}`,
                            borderRadius: theme.shape.borderRadius,
                        }}
                    >
                        {columns.map((col, colIndex) => (
                            <Typography key={colIndex} variant="subtitle2">
                                <strong>{col.header}:</strong> {col.renderCell ? col.renderCell(row) : row[col.field]}
                            </Typography>
                        ))}
                    </Box>
                ))}
            </Box>
        );
    }

    // Desktop layout table
    return (
        <Box component="table" sx={{ width: '100%', borderCollapse: 'collapse' }}>
            <Box component="thead">
                <Box
                    component="tr"
                    sx={{
                        display: 'flex',
                        fontWeight: theme.typography.fontWeightBold,
                        p: theme.spacing(1),
                        borderBottom: `2px solid ${theme.palette.divider}`,
                    }}
                >
                    {columns.map((col, index) => (
                        <Box key={index} component="th" sx={{ flex: 1, textAlign: 'left' }}>
                            <Typography variant="subtitle1">{col.header}</Typography>
                        </Box>
                    ))}
                </Box>
            </Box>
            <Box component="tbody">
                {data.map((row, rowIndex) => (
                    <Box
                        component="tr"
                        key={rowIndex}
                        sx={{
                            display: 'flex',
                            borderBottom: `1px solid ${theme.palette.divider}`,
                            p: theme.spacing(1),
                        }}
                    >
                        {columns.map((col, colIndex) => (
                            <Box key={colIndex} component="td" sx={{ flex: 1 }}>
                                <Typography variant="body2">{col.renderCell ? col.renderCell(row) : row[col.field]}</Typography>
                            </Box>
                        ))}
                    </Box>
                ))}
            </Box>
        </Box>
    );
};

DataTable.propTypes = {
    columns: PropTypes.arrayOf(
        PropTypes.shape({
            header: PropTypes.string.isRequired,
            field: PropTypes.string,
            renderCell: PropTypes.func,
        })
    ).isRequired,
    data: PropTypes.array.isRequired,
};

export default DataTable;
